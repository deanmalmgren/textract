#!/bin/bash

# these additional packages are required to make the virtual machine
# have a similar environment to travis-ci before we install anything
# else.  See Vagrantfile for details on how this could be done better
# if its a problem.
# http://docs.travis-ci.com/user/languages/python/#Travis-CI-Uses-Isolated-virtualenvs
sudo apt-get update -qq
sudo apt-get install -y python-pip python-dev build-essential

# install pep8 for testing
sudo pip install pep8

# make sure the PYTHONPATH and PATH variables are properly configured
# for the vagrant user. Always change into the /vagrant directory on
# the virtual machine to make it easy to start developing
cat << EOF > /home/vagrant/.bash_profile
export PATH=/vagrant/bin:$PATH
export PYTHONPATH=/vagrant:$PYTHONPATH
cd /vagrant
EOF
