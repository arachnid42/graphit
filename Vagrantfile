# setting a path to provision scripts
PROV_BASE = "#{File.dirname(__FILE__)}/vconf/"
STARTUP_SCRIPT = 'startup.sh'
RUN_TESTS_SCRIPT = 'run_tests.sh'

# prioritized set of provision scripts to run
PROV_SCRIPTS = ["install_pip", "install_flask", "install_sqlite3", "install_peewee", "install_sass", "install_jq", "install_numpy", 'install_git', "install_nodejs", "install_npm", "install_d3"]

# default location for a bash script that would add envvars and aliases to the guest
env_mod_file = '/etc/profile.d/env_mod.sh'

Vagrant.configure(2) do |config|

  # using amd64 Ubuntu 14.04 as a base box
  config.vm.box = "ubuntu/trusty64"

  # fixing annoying 'stdin: is not a tty' error
  # as seen at http://foo-o-rama.com/vagrant--stdin-is-not-a-tty--fix.html
  config.vm.provision "fix_no_tty", type: "shell" do |s|
    s.privileged = false
    s.inline = "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile"
  end

  # running a system update to refresh an apt-get packages list etc.
  config.vm.provision "system_update", type: "shell", path: PROV_BASE+'system_update.sh'

  # running a set of provision scripts to prepare a vbox
  PROV_SCRIPTS.each do |pscript|
    config.vm.provision pscript, type: "shell", path: PROV_BASE+'packages/'+pscript+'.sh'
  end

  # initializing string for writing environment modifications
  env_mod_cmds = "echo -n > #{env_mod_file} && "

  # cd to a project directory during vagrant ssh
  env_mod_cmds << "echo 'cd /vagrant' >> #{env_mod_file} &&"

  # making startup script executable
  env_mod_cmds << "echo 'sudo chmod +x #{STARTUP_SCRIPT}' >> #{env_mod_file} &&"

  # making tests script executable
  env_mod_cmds << "echo 'sudo chmod +x #{RUN_TESTS_SCRIPT }' >> #{env_mod_file} &&"

  # making flask_init.py executable
  env_mod_cmds << "echo 'sudo chmod +x flask_init.py' >> #{env_mod_file}"

  # writing environment modifications to the guest
  config.vm.provision "cust_env_setup", type: "shell", inline: env_mod_cmds

  # setting port forwarding to view the website in host browser
  config.vm.network "forwarded_port", guest: 5000, host: 5000
end