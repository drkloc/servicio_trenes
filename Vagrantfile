# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "centos6.4_64"
  config.vm.box_url = "http://developer.nrel.gov/downloads/vagrant-boxes/CentOS-6.4-x86_64-v20130309.box"

  config.vm.network :forwarded_port, guest: 80, host: 8080

  config.vm.synced_folder "servicio_trenes_socketio/", "/opt/apps/trenes/socketio"
  config.vm.synced_folder "servicio_trenes_stream_n_rpc/", "/opt/apps/trenes/stream_n_rpc"

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "manifests"
    puppet.manifest_file = "default.pp"
    puppet.module_path = 'manifests/modules'
    puppet.options = "--verbose --debug"
  end
end
