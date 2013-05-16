# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|

  config.vm.box = "CentOS_64_i386"
  config.vm.box_url = "http://developer.nrel.gov/downloads/vagrant-boxes/CentOS-6.4-i386-v20130309.box"

  config.vm.network :forwarded_port, guest: 8000, host: 8080
  config.vm.network :forwarded_port, guest: 8090, host: 8090
  config.vm.share_folder "src/"
  config.vm.provision :puppet
end
