#!/usr/bin/env bash
# Evaluates the built docker image by running the same files as the test suite
# to verify that the installation and PATH all work as expected
#
# Usage:
#   scripts/docker_smoke_test.sh                 # builds ghcr.io/deanmalmgren/textract:smoke-test locally
#   scripts/docker_smoke_test.sh some/image:tag   # tests an already-built or pulled image

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

IMAGE="${1:-}"
if [[ -z "$IMAGE" ]]; then
    IMAGE="textract:smoke-test"
    docker build -t "$IMAGE" .
fi

# doc needs LibreOffice, which the image doesn't include by default (see
# installation.rst). mp3/ogg/wav are tested via the offline sphinx method
# instead of the network-dependent Google default (same reason the pytest
# suite skips the Google methods under SKIP_NETWORK_TESTS).
SKIP_EXTENSIONS=(doc)
SPHINX_EXTENSIONS=(mp3 ogg wav)

failures=()
tested=0

for fixture in tests/*/raw_text.*; do
    [[ "$fixture" == *.txt ]] && continue
    ext_dir=$(dirname "$fixture")
    ext=$(basename "$ext_dir")

    skip=false
    for skip_ext in "${SKIP_EXTENSIONS[@]}"; do
        [[ "$ext" == "$skip_ext" ]] && skip=true
    done
    "$skip" && continue

    method_args=()
    expected="$ext_dir/raw_text.txt"
    for sphinx_ext in "${SPHINX_EXTENSIONS[@]}"; do
        if [[ "$ext" == "$sphinx_ext" ]]; then
            method_args=(--method sphinx)
            expected="$ext_dir/raw_text-m=sphinx.txt"
        fi
    done
    [[ -f "$expected" ]] || continue

    tested=$((tested + 1))
    stderr_file=$(mktemp)
    actual=$(docker run --rm -v "$REPO_ROOT/tests:/data:ro" "$IMAGE" "${method_args[@]}" "/data/$ext/raw_text.$ext" 2>"$stderr_file") || {
        echo "FAIL $ext: textract exited non-zero"
        cat "$stderr_file"
        rm -f "$stderr_file"
        failures+=("$ext")
        continue
    }
    rm -f "$stderr_file"

    normalized_actual=$(printf '%s' "$actual" | tr -s '[:space:]' ' ' | sed -e 's/^ *//' -e 's/ *$//')
    normalized_expected=$(tr -s '[:space:]' ' ' <"$expected" | sed -e 's/^ *//' -e 's/ *$//')

    if [[ "$normalized_actual" == "$normalized_expected" ]]; then
        echo "PASS $ext"
    else
        echo "FAIL $ext: output does not match $expected"
        diff <(echo "$normalized_actual") <(echo "$normalized_expected") || true
        failures+=("$ext")
    fi
done

echo
echo "$tested extensions tested, ${#failures[@]} failed"
if [[ ${#failures[@]} -gt 0 ]]; then
    echo "Failed: ${failures[*]}"
    exit 1
fi
