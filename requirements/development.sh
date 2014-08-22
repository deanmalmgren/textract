#!/bin/bash

# this script sets up some additional configurations that are
# convenient during development only

# make sure the PYTHONPATH and PATH variables are properly configured
# for the vagrant user. Always change into the /vagrant directory on
# the virtual machine to make it easy to start developing
cat << EOF > /home/vagrant/.bash_profile
export PATH=/vagrant/bin:$PATH
export PYTHONPATH=/vagrant:$PYTHONPATH
cd /vagrant
EOF

# setup global tab completion on the flo command
# https://github.com/kislyuk/argcomplete#activating-global-completion
activate-global-python-argcomplete --dest /etc/bash_completion.d/
