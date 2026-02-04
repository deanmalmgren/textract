#!/usr/bin/env bash

# Run this to create an up-to-date Docker container and run tests.

cd $(dirname $0)/..
base=$(pwd)

image="textract/ubuntu20.04"

# Note: For speed, the image won't be automatically rebuilt. If the dependencies
# change and the existing image is outdated, just delete it with:
# docker rmi <image name>
docker images | grep $image || docker build -t $image -f tests/Dockerfile .
docker run --rm -v $base:/home/textract/src $image
