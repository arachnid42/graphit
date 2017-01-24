# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package 'sqlite3' "
apt-get install -y sqlite3
"
