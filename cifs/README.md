Plugin for monitoring the CIFS (Common Internet File System)
==============================================

This plugin monitors the performance metrics of CIFS mount point status, IP address of server, mount points of server and client, disk utilization of CIFS on server.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---
##### Linux 

- Create a directory "cifs" under Site24x7 Linux Agent plugin directory : 

      Linux       ->   /<site24x7_installation_directory>/site24x7/monagent/plugins/cifs

- Open a terminal inside the nfs folder created on the above step and execute the below mentioned commands to download the plugin files.

	  wget https://raw.githubusercontent.com/mrkksparrow/plugins/master/cifs/cifs.py
	  wget https://raw.githubusercontent.com/mrkksparrow/plugins/master/cifs/cifs.cfg
	  wget https://raw.githubusercontent.com/mrkksparrow/plugins/master/cifs/cifs_check.sh
	
- Configure the mount point to be monitored in the cifs.cfg file, as mentioned below.

	  [display_name]
	  mount_folder = “<your_mount_folder_path>”

- Execute the below command with appropriate arguments to check for the valid json output.  

		python cifs.py --mount_folder=<your_mount_folder_path>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured
---
	mount_permission -> Mount permmision for the client to the mount point 

	mount_point -> Mount point path on the client, which is connected to the CIFS Server.

	server_ip_address -> IP Address of the server connected with the CIFS Client

	shared_directory -> The path to the directory which is shared by the CIFS Server

	disk_usage -> Percentage of the space used on the CIFS Server

	cifs_version -> Version of the CIFS installed in the Client

	domain -> Domain name of the CIFS Server
