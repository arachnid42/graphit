# cd to import directory
cd /vagrant/vconf
source provision_helper.sh

install_package 'sass' "
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 &&
\curl -sSL https://get.rvm.io | bash -s stable &&
source /usr/local/rvm/scripts/rvm &&
rvm group add rvm vagrant &&
rvm fix-permissions &&
rvm install ruby-2.1.8 &&
rvm use ruby-2.1.8 &&
gem install sass
"
