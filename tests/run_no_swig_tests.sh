#!/usr/bin/env bash

# test installation of textract without swig
# exits with correct return code which can be used to connect to CI
# see provision/fake-pocketsphinx.sh for more details

if [ ! -f "tests/Dockerfile.no-swig" ]; then
    echo "you should run this script from project root directory:"
    echo "tests/run_no_swig_tests.sh"
    exit 1
fi

if ! docker build -f "tests/Dockerfile.no-swig" . -t textract/no-swig; then
    echo "failed to build textract/no-swig docker image"
    exit 1
fi

# docker image has old textract version which didn't require swig
if [ "`docker run textract/no-swig --version 2>&1`" != "textract 1.5.0" ]; then
    echo "old textract version is not as expected: '${OLD_TEXTRACT_VERSION}'"
    exit 1
fi

# upgrade textract to version 1.6.1
# this is expected to fail - due to missing swig dependency
if docker run --entrypoint bash textract/no-swig -c "pip install --upgrade textract"; then
    echo "succeeded to install new textract without swig, and without fake pocketsphinx"
    exit 1
fi

# use the provision/fake-pocketsphinx.sh script to install the fake pocketsphinx
if ! docker run --entrypoint bash textract/no-swig -c "/provision/fake-pocketsphinx.sh && pip install --upgrade textract"; then
    echo "failed to install fake pocketsphinx"
    exit 1
fi

# TODO: add some tests here to make sure textract works correctly works without swig

echo "Success!"
exit 0
