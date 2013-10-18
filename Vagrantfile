# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "centos64"
  config.vm.box_url = "http://developer.nrel.gov/downloads/vagrant-boxes/CentOS-6.4-x86_64-v20130309.box"

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "manifests"
    puppet.manifest_file = "default.pp"
    puppet.module_path = 'manifests/modules'
    puppet.options = "--verbose --debug"
    puppet.facter = {
      "source" => "/vagrant",
      "ip" => "192.168.1.216",
      "debug" => "false",
    }
  end
end
