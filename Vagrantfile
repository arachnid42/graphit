# setting a path to provision scripts
PROV_BASE = "#{File.dirname(__FILE__)}/vconf/"

# scripts that have to be executable
EXEC_FLAG_SCRIPTS = ["startup.sh", "run_tests.sh", "flask_init.py", "git_push_enc.sh", "git_pull_enc.sh"]

# prioritized set of provision scripts to run
PROV_SCRIPTS = ["install_pip", "install_flask", "install_sqlite3", "install_peewee", "install_sass", "install_jq", "install_numpy", 'install_git']

# default location for a bash script that would add envvars and aliases to the guest
env_mod_file = '/etc/profile.d/env_mod.sh'

Vagrant.configure(2) do |config|

  # remove it when deploying
  config.vm.provider "virtualbox" do |v|
    # release full power of a host
    v.cpus = 4
    v.memory = 12288
    v.customize ["modifyvm", :id, "--cpuexecutioncap", "70"]
  end

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

  # making all the necessary scripts executable
  EXEC_FLAG_SCRIPTS.each do |script|
    env_mod_cmds << "echo 'sudo chmod +x #{script}' >> #{env_mod_file} &&"
  end

  # writing environment modifications to the guest
  config.vm.provision "cust_env_setup", type: "shell", inline: env_mod_cmds.chomp(' &&')

  # setting port forwarding to view the website in host browser
  config.vm.network "forwarded_port", guest: 5000, host: 5000
end