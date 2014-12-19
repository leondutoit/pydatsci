
Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 9009, host: 9009
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2048"]
    vb.customize ["modifyvm", :id, "--cpus", "2"]
  end

$script = <<BOOTSTRAP
sudo apt-get update
sudo apt-get -y install git gcc emacs
sudo apt-get update
sudo apt-get install -y python-pip python-dev libyaml-dev g++ sqlite3
sudo apt-get install -y automake python-setuptools python-software-properties
sudo pip install numpy pandas flask ipython
BOOTSTRAP

  config.vm.provision :shell, :inline => $script
end
