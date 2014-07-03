#!/bin/bash

# this script runs a few functional tests to make sure that everything
# is working properly. on error in any subcommands, it should not quit
# and finally exit with a non-zero exit code if any of the commands
# failed

# get the directory of this script and use it to correctly find the
# examples directory
# http://stackoverflow.com/a/9107028/564709
BASEDIR=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
EXAMPLE_ROOT=$BASEDIR/../examples

# annoying problem that md5 (OSX) and md5sum (Linux) are not the same
# in coreutils
which md5 > /dev/null
if [ $? -ne 0 ]; then
    md5 () {
	md5sum $1 | awk '{print $1}'
    }
fi

# formatting functions
red () { 
    echo $'\033[31m'"$1"$'\033[0m'
}

# function to update exit code and throw error if update value is
# non-zero
EXIT_CODE=0
update_status () {
    if [[ $1 -ne 0 ]]; then
	red "$2"
    fi
    EXIT_CODE=$(expr ${EXIT_CODE} + $1)
}

# function for running test on a specific example to validate that the
# checksum of results is consistent
validate_example () {
    example=$1
    test_checksum=$2

    # run textract on an example document and make sure the md5sum is
    # the same as what we expect
    local_checksum=$(textract $example | md5sum | awk '{print $1}')

    # hack to compute checksum of resulting archive since tarballs of
    # files with the same content are apparently not guaranteed to
    # have the same md5 hash
    if [ "${local_checksum}" != "${test_checksum}" ]; then
        red "ERROR--CHECKSUM OF ${example} DOES NOT MATCH"
        red "    local checksum=${local_checksum}"
        red "     test checksum=${test_checksum}"
	update_status 1 ""
    fi
}

# download data if it doesn't already exist



# run a few examples to make sure the checksums match what they are
# supposed to. if you update an example, be sure to update the
# checksum by just running this script and determining what the
# correct checksum is
validate_example hello-world.docx 040bf35be21ac0a3d6aa9ff4ff25df24

# exit with the sum of the status
exit ${EXIT_CODE}
