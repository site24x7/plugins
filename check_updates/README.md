# Plugin for Monitoring Software Updates Count

OS Supported: Ubuntu, Centos
## Plugin Installation

### Automatic Plugin Installation
---
Download the below file.
```
wget https://raw.githubusercontent.com/site24x7/plugins/suraj/check_updates/InstallSite24x7CheckUpdates.py && sed -i "1s|^.*|#! $(which python3)|" install_site24x7_check_updates.py
```

Execute the file using the below command.
```
./InstallSite24x7CheckUpdates.py
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
