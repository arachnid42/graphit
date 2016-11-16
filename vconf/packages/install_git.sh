# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package 'git' "
apt-get install -y git
"
