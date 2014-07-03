# -*- mode: ruby -*-
# vi: set ft=ruby :

# if there are any problems with these required gems, vagrant
# apparently has its own ruby environment (which makes sense). To
# install these gems (iniparse, for example), you need to run
# something like:
#
# [unix]$ vagrant package install iniparse
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
    override_config.vm.box = "precise32"
    override_config.vm.box_url = "http://files.vagrantup.com/precise32.box"
    override_config.vm.network :forwarded_port, guest: 8000, host: 8000
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
    provision_script(server_config, "provision/travis-mock.sh")

    # these are the same provisioning steps that are done on travis-ci
    # as on the virtual machine
    provision_script(server_config, "provision/debian.sh")
    provision_script(server_config, "provision/python.sh")

    # these provisioning steps are only done locally as a convenience
    # for setting up a useful development environment
    provision_script(server_config, "provision/development.sh")
  end

end
