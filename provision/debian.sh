#!/bin/bash

# This needs to work both for Vagrant provisioning and for Travis
# builds in a Python virtualenv, each of which have different current
# working directories when this script is called. When run in Vagrant, the
# script is copied to /tmp and executed from there, passing the original
# path as the first argument. So deal with that.
if [ "$1" == "" ]; then
    # normal
    cd $(dirname $0)/..
else
    # run from /tmp by Vagrant.
    cd $1
fi
base=$(pwd)

# Install all of the dependencies required in the examples.
# http://docs.travis-ci.com/user/installing-dependencies/#Installing-Ubuntu-packages
apt-get update -qq
sed 's/\(.*\)\#.*/\1/' < $base/requirements/debian | xargs apt-get install -y --fix-missing
