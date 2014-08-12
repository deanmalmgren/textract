#!/bin/bash

# this needs to work both for vagrant provisioning and for travis
# builds in a python virtualenv. in the virtual machine provisioning,
# we're passing the directory this should be run from. in travis-ci,
# its run from the root of the repository.
if [ "$#" -eq 1 ]; then
    cd $1
    base=$(pwd)
else
    # get the base directory name of this file so it works in
    # travis-ci environment http://stackoverflow.com/a/11114547/564709
    sudo apt-get install -y realpath
    base="/requirements/"
fi

# install all of the dependencies required in the examples
# http://docs.travis-ci.com/user/installing-dependencies/#Installing-Ubuntu-packages
sudo apt-get update -qq
sed 's/\(.*\)\#.*/\1/' < $base/debian | xargs sudo apt-get install -y --fix-missing
