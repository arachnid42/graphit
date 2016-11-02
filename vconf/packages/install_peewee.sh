# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package "python3 -c 'import peewee'" 'peewee' "
pip3 install peewee
"
