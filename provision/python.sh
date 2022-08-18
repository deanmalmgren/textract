#!/bin/bash

# This needs to work for vagrant, Travis builds, and Docker builds.
# in a python virtualenv. in the virtual machine provisioning,
# we're passing the directory this should be run from. in travis-ci,
# its run from the root of the repository.
if [ "$#" -eq 1 ]; then
     cd $1
fi

# upgrade pip so we can use wheel downloads
pip install -U pip

# Install the requirements for this package as well as this module.
pip install -r requirements/python-dev
pip install -r requirements/python-doc
