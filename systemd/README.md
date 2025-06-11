Plugin for Monitoring Systemd 
==============================================

Systemd is a suite of basic building blocks for a Linux system. It provides a system and service manager that runs as PID and starts the rest of the system.

Follow the below steps to configure the Systemd plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Systemd.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
		

### Plugin installation

- Just execute below command to download and install the systemd plugin

		  mkdir -p systemd && wget https://raw.githubusercontent.com/site24x7/plugins/master/systemd/systemd.py && wget https://raw.githubusercontent.com/site24x7/plugins/master/systemd/systemd.cfg && mv systemd.py systemd.cfg systemd

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the systemd.py script.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python systemd.py
		
- Move the folder "systemd" under Site24x7 Linux Agent plugin directory : 

		Linux            ->   /opt/site24x7/monagent/plugins/


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---
	activating_unit -> metric calculates the total number of activating units. [unit]

	active_unit -> metric calculates the total number of active units. [unit]

	deactivating_unit -> metric calculate the total number of monitored units. [unit]

	failed_unit -> metric calculate the total number of failed units. [unit]

	inactive_unit -> metric calculate the total number of inactive units. [unit]

	loaded_unit -> metric calculate the total number of loaded units. [unit]
	
	monitored_unit -> metric calculate the total number of monitored units. [unit]

	systemd_version -> metric shows the systemd version running in the server. [version]

	systemd_uptime -> metric calculate the update of the systemd in the server. [time]

	total_unit -> metric calculate the total number of units in systemd. [unit]
