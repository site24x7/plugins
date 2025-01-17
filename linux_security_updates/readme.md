# Plugin for Monitoring Software Updates Count

OS Supported: Ubuntu, Centos, AlmaLinux, Red Hat Enterprise Linux
## Plugin Installation

Quick installation
If you're using Linux servers, use the linux_security_updates plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_updates/installer/Site24x7LinuxSecurityUpdatesPluginInstaller.sh && sudo bash Site24x7LinuxSecurityUpdatesPluginInstaller.sh
```

### Manual Plugin Installation
---
##### Linux 

- Just execute below command to download and install the linux_security_updates plugin.
  
	```bash
 	mkdir -p linux_security_updates && wget https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_updates/linux_security_updates.py && sed -i "1s|^.*|#! $(which python3)|" linux_security_updates.py && wget https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_updates/linux_security_updates.cfg && mv linux_security_updates.py linux_security_updates.cfg linux_security_updates
	```

- Move the directory "linux_security_updates" into the Site24x7 Linux Agent plugin directory.

	```
	mv linux_security_updates /opt/site24x7/monagent/plugins/
	```

  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured

- Installed Packages Count
- Upgrades Available For Installed Packages
- Security Updates
- Packages to be Updated
- Reboot Required for packages
- Reboot Required Packages Count

### Package details  
  Site24x7 web client > linux_security_updates plugin monitor > select AppLog tab > User can choose logtype as "Linux Pending Security Updates" to check the details of packages which have been not updated. 
