# Plugin for Monitoring Software Updates Count on amazonlinux


### Plugin installation
---
 
- Create a directory "check_updates_amazonlinux" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/check_updates_amazonlinux
- Download the file "check_updates_amazonlinux.py" and place it under the "check_updates_amazonlinux" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates_amazonlinux/check_updates_amazonlinux.py
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured

- #### packages_to_be_updated
             No.of packages needs to be updated.
- #### security_updates 
             No.of security packages, needs to be updated.

