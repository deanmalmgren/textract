#!/bin/bash


# This needs to work both for vagrant provisioning and for Travis
# builds in a python virtualenv, each of which have different current
# working directories when this script is called.
cd $(dirname $0)/..
base=$(pwd)

# Install all of the dependencies required in the examples.
# http://docs.travis-ci.com/user/installing-dependencies/#Installing-Ubuntu-packages
apt-get update -qq
sed 's/\(.*\)\#.*/\1/' < $base/requirements/debian | xargs apt-get install -y --fix-missing
