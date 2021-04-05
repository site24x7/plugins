Plugin for monitoring the NFS (Network File System)
==============================================

This plugin monitors the performance metrics of NFS mount point status, IP address of server and client, mount points of server and client, disk utilization of NFS on server.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---
##### Linux 

- Create a directory "nfs" under Site24x7 Linux Agent plugin directory : 

      Linux (Root)      ->   /opt/site24x7/monagent/plugins/nfs
      Linux (Non Root)  ->   /home/<user_name>/site24x7/monagent/plugins/nfs

- Open a terminal inside the nfs folder created on the above step and execute the below mentioned commands to download the plugin files.

	  wget https://raw.githubusercontent.com/mrkksparrow/plugins/master/nfs/nfs.py
	  wget https://raw.githubusercontent.com/mrkksparrow/plugins/master/nfs/nfs.cfg
	  wget https://raw.githubusercontent.com/mrkksparrow/plugins/master/nfs/nfs_check.sh
	
- Configure the mount point to be monitored in the nfs.cfg file, as mentioned below.

	  [display_name]
	  mount_folder = “<your_mount_folder_path>”

- Execute the below command with appropriate arguments to check for the valid json output.  

		python nfs.py --mount_folder=<your_mount_folder_path>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured
---
	client_ip_address -> IP Address of the client connected to the NFS Server

	mount_permission -> Mount permmision for the client to the mount point 

	mount_point -> Mount point path on the client, which is connected to the NFS Server.

	server_ip_address -> IP Address of the server connected with the NFS Client

	shared_directory -> The path to the directory which is shared by the NFS Server

	disk_usage -> Percentage of the space used on the NFS Server

	nfs_version -> Version of the NFS installed in the Client
