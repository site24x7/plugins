# Plugin for Monitoring Software Updates Count

OS Supported: Ubuntu, Centos
## Plugin Installation

Quick installation
If you're using Linux servers, use the check_updates plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/installer/Site24x7CheckUpdatesPluginInstaller.sh && sudo bash Site24x7CheckUpdatesPluginInstaller.sh
```

### Manual Plugin Installation
---
##### Linux 

- Just execute below command to download and install the check_update plugin.
  
	```bash
 	mkdir -p check_updates && wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/check_updates.py && sed -i "1s|^.*|#! $(which python3)|" check_updates.py && wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/check_updates.cfg && mv check_updates.py check_updates.cfg check_updates
	```

- Move the directory "check_updates" into the Site24x7 Linux Agent plugin directory.

	```
	mv check_updates /opt/site24x7/monagent/plugins/
	```

  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured

- Installed Packages Count
- Upgrades Available For Installed Packages
- Security Updates
- Packages to be Updated

### Package details  
  Site24x7 web client > check_update plugin monitor > select AppLog tab > User can choose logtype as "Linux Pending Updates" to check the details of packages which have been not updated. 
