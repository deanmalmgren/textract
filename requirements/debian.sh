#!/bin/bash

# this needs to work both for vagrant provisioning and for travis
# builds in a python virtualenv. in the virtual machine provisioning,
# we're passing the directory this should be run from. in travis-ci,
# its run from the root of the repository.
base=$(dirname $0)

# install all of the dependencies required in the examples
# http://docs.travis-ci.com/user/installing-dependencies/#Installing-Ubuntu-packages
apt-get update -qq
sed 's/\(.*\)\#.*/\1/' < $base/debian | xargs apt-get install -y --fix-missing
