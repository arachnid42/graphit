# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package "python3 -c 'import pymssql'" 'python3-pymssql' "
sudo apt-get install -y freetds-dev &&
sudo pip3 install pymssql
"