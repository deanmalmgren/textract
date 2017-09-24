#!/usr/bin/env bash

# the pocketsphinx dependency requires swig during pip installation
# swig might be difficult to install in some environments
#
# this script install a fake pocketsphinx dependency - which allow to easily install without the swig dependency
#
# for more details and discussion, see:
# * https://github.com/deanmalmgren/textract/issues/159
# * https://github.com/deanmalmgren/textract/pull/160

# TEMPDIR is used as the fake pocketsphinx package directory, it will be removed
TEMPDIR=`mktemp -d`

# fake pocketsphinx version, we get it from requirements files
VERSION="${FAKE_POCKETSPHINX_VERSION:-`cat requirements/* | grep 'pocketsphinx==' | cut -c15-`}"


# create a fake setup.py and install it
echo "from setuptools import setup; setup(\
        name='pocketsphinx', \
        version='${VERSION}'\
     )" > "${TEMPDIR}/setup.py"
"${FAKE_POCKETSPHINX_PIP:-pip}" install "${TEMPDIR}/"

# cleanup
rm -rf "${TEMPDIR}"
