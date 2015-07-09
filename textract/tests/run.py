#!/usr/bin/env python

"""Run the test suite that is specified in the .travis.yml file
"""

import os
import subprocess

import yaml

from textract.colors import green, red

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def run_test(command):
    wrapped_command = "cd %s && %s" % (root_dir, command)
    pipe = subprocess.Popen(
        wrapped_command, shell=True,
    )
    pipe.wait()
    if pipe.returncode == 0:
        print(green("TEST PASSED"))
    else:
        print(red("TEST FAILED"))
    return pipe.returncode

# load the script tests from the .travis.yml file
with open(os.path.join(root_dir, '.travis.yml')) as stream:
    travis_yml = yaml.load_all(stream.read())
config = travis_yml.next()
tests = config['script']

# run the tests
if isinstance(tests, (str, unicode)):
    returncode = run_test(tests)
elif isinstance(tests, (list, tuple)):
    returncode = 0
    for test in tests:
        returncode += run_test(test)

if returncode == 0:
    print(green("ALL TESTS PASSED"))
else:
    print(red("SOME TESTS FAILED, SEE ABOVE"))
