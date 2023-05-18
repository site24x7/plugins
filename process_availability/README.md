Plugin for monitoring the process availability 
==============================================

This plugin monitors if the specified process is running in the current machine and alert it as down and return the number of processes. If no specified process is running, it will alert as up.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "subprocess" python library. This module is used to execute the ps command and get data


### Plugin installation
---
##### Linux 

- Create a directory "process_availability".

- Download all the files in "process_availability" folder and place it under the "process_availability" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/process_availability/process_availability.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/process_availability/process_availability.cfg
	
- Configure the keys to be monitored, in "process_availability.cfg" as mentioned below.

		[java]
		host="java"
		plugin_version="1"
		heartbeat="True"

- Execute the below command with appropriate arguments to check for the valid json output.  

		python process_availability.py --process="java" --plugin_version="1" --heartbeat="True"
		
- Move the directory "process_availability" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Captured
---
	process_name - Name of the process being monitored. 
	process_running - Total number of process running 			
