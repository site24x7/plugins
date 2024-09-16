Plugin for monitoring the NFS (Network File System)
==============================================

This plugin monitors the performance metrics of NFS mount point status, the IP address of server and client, mount points of server and client, and disk utilization of NFS on the server.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


## Plugin installation

##### Linux 

- Create a directory `nfs`.

- Open a terminal inside the nfs folder and execute the below-mentioned commands to download the plugin files.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/nfs/nfs.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/nfs/nfs.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the nfs.py script.
	
- The plugin will automatically identify and monitor all NFS mounts present on the server.

- Increase the plugin version in the nfs.cfg file, if you need to add mounts to monitor after plugin registration.

- Execute the below command with appropriate arguments to check for the valid JSON output.  

		python3 nfs.py 
  
- Move the directory `nfs` under the Site24x7 Linux Agent plugin directory : 

		mv nfs /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and the user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


## Metrics Captured

Name		        | 	Description
---         		|  	 ---
Mount Permission 	|	Mount permmision for the client to the mount point.
Mount From 		|	Mount point path on the client, which is connected to the CIFS Server.
Available size 		|	Available size in gigabytes (GB) represents the amount of free space left on the disk.
Disk Usage 		|	The percentage of the disk space that is currently in use.
Total Size 		|	The total size in gigabytes (GB) represents the total storage capacity of the disk.
Used Size		|	The used size in gigabytes (GB) indicates the amount of disk space that is currently being utilized.
NFS Version 		|	Version of the CIFS installed in the Client.
