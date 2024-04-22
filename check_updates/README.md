# Plugin for Monitoring Software Updates Count

OS Supported: Ubuntu, Centos
## Plugin Installation

Quick installation
If you're using Linux servers, use the Oracle plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:
```
wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/installer/Site24x7CheckUpdatesPluginInstaller.sh && sudo bash Site24x7CheckUpdatesPluginInstaller.sh
```

### Manual Plugin Installation
---
##### Linux 

- Create a directory "check_updates".

- Download the file "check_updates.py" and place it under the "check_updates" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/check_updates.py
  
  
- Execute the script manually using the below command to check for valid JSON output.

		python3 check_updates.py

- Move the directory "check_updates" into the Site24x7 Linux Agent plugin directory - `/opt/site24x7/monagent/plugins/check_updates`
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured

- Installed Packages Count
- Upgrades Available For Installed Packages
- Security Updates
- Packages to be Updated
