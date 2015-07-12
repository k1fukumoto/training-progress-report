ENV['VAGRANT_DEFAULT_PROVIDER'] = 'vmware_appcatalyst'
 
nodes = [
  { hostname: 'tpr-01', box: 'vmware/photon' },
]
 
Vagrant.configure('2') do |config|
 
  # Configure our boxes with 1 CPU and 384MB of RAM
  config.vm.provider 'vmware_appcatalyst' do |v|
    v.cpus = '1'
    v.memory = '384'
  end
 
  # Go through nodes and configure each of them.j
  nodes.each do |node|
    config.vm.define node[:hostname] do |node_config|
      node_config.vm.box = node[:box]
      node_config.vm.hostname = node[:hostname]
    end
  end
  
  config.vm.synced_folder "./", "/srv"

#  config.vm.provision "shell", inline: "docker run -d -p 8080:8080 k1fukumoto/training-progress-report"
end
