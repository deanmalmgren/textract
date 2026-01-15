#!/usr/bin/env bash
# Test GitHub Actions workflows locally using Act
# Usage: ./scripts/test-with-act.sh [job-name] [options]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo -e "${RED}Error: 'act' is not installed${NC}"
    echo "Install with: brew install act"
    echo "Or see: https://github.com/nektos/act#installation"
    exit 1
fi

# Default values
JOB_NAME="${1:-test}"
WORKFLOW_FILE=".github/workflows/ci_pipeline.yml"

# Check if workflow file exists
if [[ ! -f "$WORKFLOW_FILE" ]]; then
    echo -e "${RED}Error: Workflow file not found: $WORKFLOW_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}Running Act for job: $JOB_NAME${NC}"
echo -e "${YELLOW}Note: Windows jobs are not supported by Act${NC}"
echo ""

# Run act with the specified job
# --matrix allows us to run specific matrix combinations
# Use -l to list all jobs first
if [[ "$JOB_NAME" == "list" ]]; then
    echo -e "${GREEN}Available jobs and matrix combinations:${NC}"
    act -l -W "$WORKFLOW_FILE"
    exit 0
fi

# Run specific matrix combinations
# For ubuntu with Python 3.9
if [[ "$JOB_NAME" == "test-ubuntu-3.9" ]]; then
    act -j test \
        --matrix os:ubuntu-latest \
        --matrix python-version:3.9 \
        -W "$WORKFLOW_FILE"
    exit 0
fi

# For ubuntu with Python 3.14
if [[ "$JOB_NAME" == "test-ubuntu-3.14" ]]; then
    act -j test \
        --matrix os:ubuntu-latest \
        --matrix python-version:3.14 \
        -W "$WORKFLOW_FILE"
    exit 0
fi

# For macOS with Python 3.9
if [[ "$JOB_NAME" == "test-macos-3.9" ]]; then
    act -j test \
        --matrix os:macos-latest \
        --matrix python-version:3.9 \
        -W "$WORKFLOW_FILE"
    exit 0
fi

# For macOS with Python 3.14
if [[ "$JOB_NAME" == "test-macos-3.14" ]]; then
    act -j test \
        --matrix os:macos-latest \
        --matrix python-version:3.14 \
        -W "$WORKFLOW_FILE"
    exit 0
fi

# Default: run all linux jobs (fast)
if [[ "$JOB_NAME" == "test" ]]; then
    echo -e "${YELLOW}Running Ubuntu jobs only (fastest)${NC}"
    act -j test \
        --matrix os:ubuntu-latest \
        -W "$WORKFLOW_FILE"
    exit 0
fi

# Run specific job by name
act -j "$JOB_NAME" -W "$WORKFLOW_FILE"
