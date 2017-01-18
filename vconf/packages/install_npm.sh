# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package 'npm' "
apt-get install -y npm
"