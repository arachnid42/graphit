# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package "python3 -c 'from flask import *'" 'flask' "
pip3 install Flask
"