Plugin for Systemd Monitoring 
==============================================

Systemd is a suite of basic building blocks for a Linux system. It provides a system and service manager that runs as PID and starts the rest of the system.

Follow the below steps to configure the Systemd plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Systemd.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
		

### Plugin installation
---
##### Linux 

- Create a folder "systemd" under Site24x7 Linux Agent plugin directory : 

      Linux            ->   /opt/site24x7/monagent/plugins/systemd

---

- Download the file in "systemd" folder and place it under the "systemd" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/systemd/systemd.py

- Execute the below command with appropriate arguments to check for the valid json output.  

		python systemd.py


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


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
