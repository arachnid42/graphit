# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package "python3 -c 'import numpy'" 'python3-numpy' "
apt-get install -y python3-numpy
"