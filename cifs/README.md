Plugin for monitoring the CIFS (Common Internet File System)
==============================================

This plugin monitors the performance metrics of CIFS mount point status, IP address of server, mount points of server and client, disk utilization of CIFS on server.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


## Plugin installation

- Create a directory `cifs`.
  
	```bash
	mkdir cifs
	cd cifs/
	```
  
- Download the files and place it under the `cifs` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/cifs/cifs.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/cifs/cifs.cfg
	```
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the cifs.py script.
	
- Configure the mount point to be monitored in the cifs.cfg file, as mentioned below.

	```bash
	[mounts]
	plugin_version = "1"
	```

- The plugin will automatically identify and monitor all CIFS mounts present on the server.

- Increase the plugin version if you need to add mounts to monitor after plugin registration.

- Execute the below command with appropriate arguments to check for the valid json output.  

	```bash
	python cifs.py
	```	
- Move the directory `cifs` under Site24x7 Linux Agent plugin directory :

	```bash
	mv cifs /opt/site24x7/monagent/plugins/
	```

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


## Metrics Captured

Name		        | 	Description
---         		|  	 ---
Mount Permission 	|	Mount permmision for the client to the mount point.
Mount From 		|	Mount point path on the client, which is connected to the CIFS Server.
Available size 		|	Available size in gigabytes (GB) represents the amount of free space left on the disk.
Disk Usage 		|	The percentage of the disk space that is currently in use.
Total Size 		|	The total size in gigabytes (GB) represents the total storage capacity of the disk.
Used Size		|	The used size in gigabytes (GB) indicates the amount of disk space that is currently being utilized.
Cifs Version 		|	Version of the CIFS installed in the Client.
