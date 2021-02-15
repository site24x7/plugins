Plugin for monitoring the process availability 
==============================================

This plugin monitors if the specified process is running in the current machine and alert it as down and return the number of processes. If no specified process is running, it will alert as up.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "subprocess" python library. This module is used to execute the ps command and get data


### Plugin installation
---
##### Linux 

- Create a directory "process_availability" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/process_availability

- Download all the files in "process_availability" folder and place it under the "process_availability" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/process_availability/process_availability.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/process_availability/process_availability.cfg
	
- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python process_availability.py --process="java" --plugin_version="1" --heartbeat="True"


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations
---
	process = Process to be monitored.
	plugin_version = 1
	heartbeat = True

### Metrics Captured
---
	process_name - Name of the process being monitored. 
	process_running - Total number of process running 			
