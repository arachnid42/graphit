# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package 'pip3' "
apt-get install -y python3-pip
"