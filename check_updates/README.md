# Plugin for Monitoring Software Updates Count

OS Supported : Ubuntu

### Plugin installation
---
##### Linux 

- Create a directory "check_updates" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/check_updates
- Download the file "check_updates" and place it under the "check_updates" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/check_updates.py
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configuration

- Plugin fetches software update count from the file "/var/lib/update-notifier/updates-available"
  
  If it is different kindly specify the same in FILE_PATH of check_updates.py.


### Metrics Captured

- packages_to_be_updated
- security_updates 
