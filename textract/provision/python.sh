#!/bin/bash

# This needs to work for vagrant, Travis builds, and Docker builds.
# in a python virtualenv. in the virtual machine provisioning,
# we're passing the directory this should be run from. in travis-ci,
# its run from the root of the repository.
if [ "$#" -eq 1 ]; then
     cd $1
fi


# Install the requirements for this package as well as this module.
pip install -r requirements/python
pip install .

# Install the requirements for this package in development
pip install -r requirements/python-dev
