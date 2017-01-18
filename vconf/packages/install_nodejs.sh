# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package 'nodejs' "
apt-get install -y nodejs
"