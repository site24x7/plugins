# Plugin for Monitoring Software Updates Count

OS Supported: Ubuntu, Centos

### Plugin installation
---
##### Linux 

- Create a directory "check_updates".

- Download the file "check_updates.sh" and place it under the "check_updates" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/check_updates.sh
  
  
- Execute the script manually using the below command to check for valid JSON output.

		bash check_updates.sh

- Move the directory "check_updates" into the Site24x7 Linux Agent plugin directory - `/opt/site24x7/monagent/plugins/check_updates`
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured

- packages_to_be_updated
- security_updates 
