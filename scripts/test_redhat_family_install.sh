#!/usr/bin/env bash
# One-off probe of textract's system-dependency install story on RHEL-family
# distros that GitHub Actions has no hosted runner for (see issue #486). Not
# wired into CI: this is meant to be run locally against Docker to gather
# evidence for docs/installation.rst, not to gate merges.
#
# For each distro image, spins up a container, enables the repos it needs,
# dnf-installs the same functional set of packages
# .github/actions/setup/action.yml installs on Ubuntu, pip-installs textract
# from this checkout, and runs a handful of fixture extractions (including
# one exercising mp3, since that's the package most likely to differ).
#
# Usage:
#   scripts/test_redhat_family_install.sh                  # all distros below
#   scripts/test_redhat_family_install.sh rockylinux9 ubi9  # just these keys

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT" || exit 1

# key -> "image|epel setup command (or empty)|extra repo enable command (or empty)|python binary to use"
#
# The distro's default `python3` is below textract's requires-python floor
# (3.9 on EL9/UBI9, 3.6 on EL8) and pillow has no wheel for it, so each entry
# names a newer interpreter package available from AppStream/EPEL to build a
# venv with instead.
declare -A DISTROS=(
    # python3.12 on EL8 (AppStream) links against a newer libexpat than the
    # base OS ships and fails with `undefined symbol:
    # XML_SetBillionLaughsAttackProtectionMaximumAmplification` as soon as pip
    # (via ensurepip) imports xmlrpc.client; python3.11 doesn't hit this.
    [rockylinux8]="rockylinux:8|dnf install -y epel-release|dnf config-manager --set-enabled powertools|python3.11"
    [rockylinux9]="rockylinux:9|dnf install -y epel-release|dnf config-manager --set-enabled crb|python3.13"
    [almalinux9]="almalinux:9|dnf install -y epel-release|dnf config-manager --set-enabled crb|python3.13"
    [centos-stream9]="quay.io/centos/centos:stream9|dnf install -y epel-release|dnf config-manager --set-enabled crb|python3.13"
    [ubi9]="registry.access.redhat.com/ubi9/ubi:latest|dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm||python3"
)

TARGETS=("$@")
[[ ${#TARGETS[@]} -eq 0 ]] && TARGETS=("${!DISTROS[@]}")

RESULTS_DIR="$(mktemp -d)"
echo "Logs: $RESULTS_DIR"

PROBE_SCRIPT='
set -uo pipefail
step() { label="$1"; shift; echo "=== $label ==="; if "$@"; then echo "--- OK: $label ---"; else echo "--- FAIL: $label (exit $?) ---"; fi; }

step "dnf install epel" bash -c "$EPEL_CMD"
if [[ -n "$EXTRA_REPO_CMD" ]]; then
    step "enable extra repo" bash -c "$EXTRA_REPO_CMD"
fi
# unrtf isolated from the required set: it is missing from some EPEL releases
# and dnf aborts the whole transaction (installing nothing, not even the
# unrelated packages) if any one package in the list is unresolvable.
step "install required system packages" dnf install -y \
    "$PYTHON_BIN" "$PYTHON_BIN"-devel "$PYTHON_BIN"-pip gcc \
    libxml2-devel libxslt-devel libjpeg-turbo-devel swig \
    tesseract sox ghostscript poppler-utils libreoffice-writer
step "install unrtf (.rtf support)" dnf install -y unrtf
step "create venv" "$PYTHON_BIN" -m venv /opt/venv
source /opt/venv/bin/activate
step "pip install textract from checkout" pip install --no-cache-dir "/workspace[pocketsphinx]"
step "textract --help" textract --help
step "extract pdf fixture" textract /workspace/tests/pdf/raw_text.pdf
step "extract mp3 fixture (sphinx, offline)" textract --method sphinx /workspace/tests/mp3/raw_text.mp3
step "extract doc fixture (libreoffice)" textract /workspace/tests/doc/raw_text.doc
step "extract rtf fixture (unrtf)" textract /workspace/tests/rtf/raw_text.rtf
'

overall_status=0
for key in "${TARGETS[@]}"; do
    entry="${DISTROS[$key]:-}"
    if [[ -z "$entry" ]]; then
        echo "Unknown distro key: $key (known: ${!DISTROS[*]})" >&2
        overall_status=1
        continue
    fi
    IFS='|' read -r image epel_cmd extra_repo_cmd python_bin <<<"$entry"
    log_file="$RESULTS_DIR/$key.log"
    echo
    echo "##### $key ($image) #####"
    if docker run --rm -v "$REPO_ROOT:/workspace:ro" \
        -e "EPEL_CMD=$epel_cmd" -e "EXTRA_REPO_CMD=$extra_repo_cmd" -e "PYTHON_BIN=$python_bin" \
        "$image" bash -c "$PROBE_SCRIPT" >"$log_file" 2>&1; then
        :
    fi
    # unanchored: a fixture's own extracted text (e.g. a PDF's trailing form
    # feed) can precede the marker on its line without a newline between them
    grep -E -- '--- (OK|FAIL):' "$log_file" | sed -E 's/.*(--- (OK|FAIL):.*)/[KEY] \1/;s/KEY/'"$key"'/'
    if grep -q -- '--- FAIL:' "$log_file"; then
        overall_status=1
    fi
    echo "Full log: $log_file"
done

echo
echo "Summary written to $RESULTS_DIR; overall exit $overall_status"
exit $overall_status
