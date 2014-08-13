#!/usr/bin/env bash

# Run this to create an up-to-date Docker container and run tests.

docker build -t textract/ubuntu12.04 . && docker run --rm -v $(pwd)/..:/textract/ textract/ubuntu12.04
