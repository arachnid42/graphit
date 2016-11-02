# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package 'jq' "
apt-get install -y jq
"