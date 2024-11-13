Plugin for monitoring the NFS (Network File System)
==============================================

This plugin monitors the performance metrics of NFS mount point status, the IP address of server and client, mount points of server and client, and disk utilization of NFS on the server.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


## Plugin installation

##### Linux 

- Create a directory `nfs`.

	```bash
	mkdir nfs
	cd nfs/
	```

- Inside the nfs folder and execute the below commands to download the plugin files.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/nfs/nfs.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/nfs/nfs.cfg
	```
 
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the nfs.py script.
	
- The plugin will automatically identify and monitor all NFS mounts present on the server.

- Execute the below command with appropriate arguments to check for the valid JSON output.  

	```bash
	python3 nfs.py 
  	```
- Move the directory `nfs` under the Site24x7 Linux Agent plugin directory : 

	```bash
	mv nfs /opt/site24x7/monagent/plugins/
	```
 
The agent will automatically execute the plugin within five minutes and the user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

#### Note:
To add mount points after the registration of the plugin, increase the version of the plugin in nfs.cfg file, as mentioned below.

```bash
[mounts]
plugin_version = "2"
```

## Metrics Captured

Name		        | 	Description
---         		|  	 ---
Mount Permission 	|	Mount permmision for the client to the mount point.
Mount From 		|	Mount point path on the client, which is connected to the CIFS Server.
Available size 		|	Available size in gigabytes (GB) represents the amount of free space left on the disk.
Disk Usage 		|	The percentage of the disk space that is currently in use.
Total Size 		|	The total size in gigabytes (GB) represents the total storage capacity of the disk.
Used Size		|	The used size in gigabytes (GB) indicates the amount of disk space that is currently being utilized.
NFS Version 		|	Version of the NFS installed in the Client.
