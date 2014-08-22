# -*- mode: ruby -*-
# vi: set ft=ruby :

# If there are any problems with the required gems, vagrant
# has its own ruby environment. To install the gems (iniparse, 
# for example), you need to run:
#
# $ vagrant plugin install iniparse
#
# For more details, check out: 
# https://docs.vagrantup.com/v2/cli/plugin.html

require 'iniparse'

Vagrant.configure("2") do |config|
  
  # preliminaries
  root_dir = File.dirname(__FILE__)
  
  #################################################### VIRTUALBOX PROVIDER SETUP
  # global configuration on the virtualbox provider. for all available
  # options, see http://www.virtualbox.org/manual/ch08.html
  virtualbox_server_name = "dev"
  config.vm.provider :virtualbox do |vb, override_config|
    vb.gui = false
    # http://stackoverflow.com/a/17126363/892506
    vb.customize ["modifyvm", :id, "--ioapic", "on"] 
    vb.customize ["modifyvm", :id, "--cpus", "2"]
    vb.customize ["modifyvm", :id, "--memory", "2048"]
    override_config.vm.box = "precise64"
    override_config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  end
 
  # steps for provisioning so that these provisioning steps are
  # properly executed in this virtual machine and also on travis-ci
  def provision_script(config, script_path)
    config.vm.provision "shell" do |s|
      s.path = script_path
      s.args = "/vagrant"
    end
  end


  ################################################################# LOCAL SERVER
  config.vm.define virtualbox_server_name do |server_config|
    server_config.vm.hostname = virtualbox_server_name

    # NOTE: this is a tentative hack. the way to properly do this
    # would be to use the official ci-environments
    # http://docs.travis-ci.com/user/ci-environment/, which are built
    # using chef recipes from here
    # https://github.com/travis-ci/travis-cookbooks/
    provision_script(server_config, "requirements/travis-mock.sh")

    # these are the same provisioning steps that are done on travis-ci
    # as on the virtual machine
    provision_script(server_config, "requirements/debian.sh")
    provision_script(server_config, "requirements/python.sh")

    # these provisioning steps are only done locally as a convenience
    # for setting up a useful development environment
    provision_script(server_config, "requirements/development.sh")
  end

end
