Plugin for monitoring the NFS (Network File System)
==============================================

This plugin monitors the performance metrics of NFS mount point status, IP address of server and client, mount points of server and client, disk utilization of NFS on server.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---
##### Linux 

- Create a directory "nfs".

- Open a terminal inside the nfs folder created on the above step and execute the below mentioned commands to download the plugin files.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/nfs/nfs.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/nfs/nfs.cfg
		wget https://raw.githubusercontent.com/site24x7/plugins/master/nfs/nfs_check.sh

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the nfs.py script.
	
- Configure the mount point to be monitored in the nfs.cfg file, as mentioned below.

		[display_name]
		mount_folder = “<your_mount_folder_path>,<your_mount_folder_path1>”
		plugin_version = 1

- Enter the Folder paths inside the " " quotation marks separated by commas ','.

- Increase the plugin version if you need to add folders after plugin registration.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python nfs.py --mount_folder=<your_mount_folder_path>,<your_mount_folder_path1>
  


- Move the directory "nfs" under Site24x7 Linux Agent plugin directory : 

		Linux       ->   /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---
	Folder 1,2,etc,. Mount Permission -> Mount permmision for the client to the mount point 

	Folder 1,2,etc,. Mount Point -> Mount point path on the client, which is connected to the NFS Server.

	Folder 1,2,etc,. Server IP Address -> IP Address of the server connected with the NFS Client

	Folder 1,2,etc,. Shared Directory -> The path to the directory which is shared by the NFS Server

	<Folder Name> Disk Usage -> Percentage of the space used on the NFS Server

	nfs Version -> Version of the NFS installed in the Client

	Folder 1,2,etc,. Status -> Domain name of the NFS Server
