#!/bin/bash

# this script runs a few functional tests to make sure that everything
# is working properly. on error in any subcommands, it should not quit
# and finally exit with a non-zero exit code if any of the commands
# failed

# get the directory of this script and use it to correctly find the
# examples directory
# http://stackoverflow.com/a/9107028/564709
BASEDIR=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)

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
    # manipulate the list of arguments passed to this function via
    # http://stackoverflow.com/a/10308353/564709
    args=("$@")
    test_checksum=${args[-1]}
    unset args[${#args[@]}-1]

    # run textract on an example document and make sure the md5sum is
    # the same as what we expect
    echo running textract "${args[@]}"...
    textract "${args[@]}" -o dummy.txt
    update_status $? 'textract failed!'
    # cat dummy.txt
    local_checksum=$(md5sum dummy.txt | awk '{print $1}')
    rm -f dummy.txt

    # hack to compute checksum of resulting archive since tarballs of
    # files with the same content are apparently not guaranteed to
    # have the same md5 hash
    if [ "${local_checksum}" != "${test_checksum}" ]; then
        red "ERROR--CHECKSUM FOR TEST '$@' DOES NOT MATCH"
        red "    local checksum=${local_checksum}"
        red "     test checksum=${test_checksum}"
	update_status 1 ""
    fi
}

# run a few examples to make sure the checksums match what they are
# supposed to. if you update an example, be sure to update the
# checksum by just running this script and determining what the
# correct checksum is
validate_example ${BASEDIR}/docx/i_heart_word.docx 35b515d5e9d68af496f9233eb81547be
validate_example ${BASEDIR}/pptx/i_love_powerpoint.pptx a5bc9cbe9284d4c81c1106a8137e4a4d
validate_example ${BASEDIR}/doc/i_heart_word.doc 8c6b87285e7d5498cff369fe4536a54b
validate_example ${BASEDIR}/pdf/i_heart_pdfs.pdf 06719d714211174a3851ac4cee880fe1
validate_example -m pdfminer ${BASEDIR}/pdf/i_heart_pdfs.pdf d4377783e5fbde756d3a195bfd103be0
validate_example ${BASEDIR}/txt/little_bo_peep.txt 1c5fb4478d84c3b3296746e491895ada
validate_example ${BASEDIR}/html/snow-fall.html a90fa8b2bc9dc84673466ddc30fed497
validate_example ${BASEDIR}/html/what-we-do.html 1fb0263bf62317365cb30246d9e094be
validate_example ${BASEDIR}/eml/example.eml cb59a5fad8ed8b849e15d53449b1de3f
validate_example ${BASEDIR}/ps/example.ps bdd41be3e24d7ded69be1e5732f7c8fc
validate_example ${BASEDIR}/json/json_is_my_best_friend.json dc0503f1b5a213d67cc08829b12df99e
validate_example ${BASEDIR}/odt/i_heart_odt.odt f64b15c1acf5cebb1a91896221696da7
validate_example ${BASEDIR}/jpg/i_heart_jpegs.jpg 74b5fcffef2aa3e284dccc0cca577d47
validate_example ${BASEDIR}/gif/i_heart_gifs.gif 0b37ec3f7b0f13d5897b93ef079a97c7
validate_example ${BASEDIR}/png/i_heart_pngs.png 302242ffea5998b8456f596d35fc8150
validate_example ${BASEDIR}/xls/a_good_example.xls b3d50046311c740b14edd91a8320ff1c
validate_example ${BASEDIR}/xlsx/another_good_example.xlsx 5b3df3c382d4fd4ff87d8773ba16d54c
validate_example ${BASEDIR}/epub/testing_epub.epub d41d8cd98f00b204e9800998ecf8427e

# exit with the sum of the status
exit ${EXIT_CODE}
