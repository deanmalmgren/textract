#!/usr/bin/env bash

# Run this to create an up-to-date Docker container and run tests.

docker build -t milo/textract . && docker run -v /home/shawn/projects/textract:/textract/ milo/textract
