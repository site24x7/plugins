Plugin for Monitoring File metadata
===================================

### PreRequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin uses "os" python module.
	
### Plugin installation
---
##### Linux 

- Create a directory "file_monitoring" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/file_monitoring

- Download the file "file_monitoring.py" and place it under the "file_monitoring" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/file_monitoring/file_monitoring.py
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured
---

size - size of the file in KB

read_access - read access enabled 

write_access - write access enabled 

execution_access - execution access enabled 

last_access_time - last file accessed time

last_modified_time - last file modified time

time_since_last_accessed - hours before the file was accessed last 

time_since_last_modified - hours before the file was modified last 
