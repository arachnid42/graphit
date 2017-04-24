# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package "tsql -C" 'freetds' "
sudo apt-get install -y freetds-dev freetds-bin
"
