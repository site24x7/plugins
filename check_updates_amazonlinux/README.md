# Plugin for Monitoring Software Updates Count on amazonlinux


### Plugin installation
---
 
- Create a directory "check_updates_amazonlinux".

- Download the file "check_updates_amazonlinux.py" and place it under the "check_updates_amazonlinux" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates_amazonlinux/check_updates_amazonlinux.py
		
- Execute the script manually using below command to check for valid json output.

		pyhton check_updates_amazonlinux.py
		
- Move the directory "check_updates_amazonlinux" under the Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/check_updates_amazonlinux
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured

- #### Packages_to_be_updated
            The number of packages that need to be updated.
- #### Security_updates 
            The number of security packages that need to be updated.
