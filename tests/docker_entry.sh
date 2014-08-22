#!/usr/bin/env bash

# This script gets called from within the
# Docker container.

cd $SRC
python setup.py install
./tests/run.py
