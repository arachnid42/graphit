# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package 'npm list -g | grep d3' 'd3' "
npm install -g d3
"
