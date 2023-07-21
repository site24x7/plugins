# Plugin for Monitoring Software Updates Count

OS Supported : Ubuntu , Centos

### Plugin installation
---
##### Linux 

- Create a directory "check_updates".

- Download the file "check_updates.py" and place it under the "check_updates" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/check_updates.py
  
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the check_updates.py script.
  
- Execute the script manually using below command to check for valid json output.

		python check_updates.py

- Move the directory "check_updates" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/check_updates
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configuration

##### Ubuntu
 
- Plugin fetches software update count from the file "/var/lib/update-notifier/updates-available"
  
  If it is different kindly specify the same in FILE_PATH of check_updates.py.
 
##### Centos

- Plugin needs "yum-plugin-security" package to get the count of software updates.

  If not installed kindly install using command "yum -y install yum-plugin-security"


### Metrics Captured

- packages_to_be_updated
- security_updates 
