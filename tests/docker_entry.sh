#!/usr/bin/env bash

# This script gets called from within the
# Docker container.

cd "$(dirname "$0")" && make && pytest && cd -
