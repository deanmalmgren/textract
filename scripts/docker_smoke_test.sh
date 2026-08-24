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

# mp3/ogg/wav default to Google's network speech API (same reason the pytest
# suite skips them under SKIP_NETWORK_TESTS); the offline sphinx method needs
# pocketsphinx, which isn't installed in the image. doc needs LibreOffice,
# which the image doesn't include by default (see installation.rst).
SKIP_EXTENSIONS=(doc mp3 ogg wav)

failures=()
tested=0

for fixture in tests/*/raw_text.*; do
    [[ "$fixture" == *.txt ]] && continue
    ext_dir=$(dirname "$fixture")
    ext=$(basename "$ext_dir")
    expected="$ext_dir/raw_text.txt"
    [[ -f "$expected" ]] || continue

    skip=false
    for skip_ext in "${SKIP_EXTENSIONS[@]}"; do
        [[ "$ext" == "$skip_ext" ]] && skip=true
    done
    "$skip" && continue

    tested=$((tested + 1))
    stderr_file=$(mktemp)
    actual=$(docker run --rm -v "$REPO_ROOT/tests:/data:ro" "$IMAGE" "/data/$ext/raw_text.$ext" 2>"$stderr_file") || {
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
