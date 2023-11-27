Plugin for monitoring the CIFS (Common Internet File System)
==============================================

This plugin monitors the performance metrics of CIFS mount point status, IP address of server, mount points of server and client, disk utilization of CIFS on server.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---
##### Linux 

- Create a directory "cifs".

- Open a terminal inside the nfs folder created on the above step and execute the below mentioned commands to download the plugin files.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/cifs/cifs.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/cifs/cifs.cfg
		wget https://raw.githubusercontent.com/site24x7/plugins/master/cifs/cifs_check.sh
  
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the cifs.py script.
	
- Configure the mount point to be monitored in the cifs.cfg file, as mentioned below.

		[display_name]
		mount_folder = “<your_mount_folder_path>,<your_mount_folder_path1>”
		plugin_version = 1
	  
- Enter the Folder paths inside the " " separated by commas ','.

- Increase the plugin version if you need to add folders after plugin registration.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python cifs.py --mount_folder=<your_mount_folder_path>,<your_mount_folder_path1>
		
- Move the directory "cifs" under Site24x7 Linux Agent plugin directory :

		Linux       ->   /opt/site24x7/monagent/plugins/cifs


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured
---
	Folder 1,2,etc,. Mount Permission -> Mount permmision for the client to the mount point 

	Folder 1,2,etc,. Mount Point -> Mount point path on the client, which is connected to the CIFS Server.

	Folder 1,2,etc,. Server IP Address -> IP Address of the server connected with the CIFS Client

	Folder 1,2,etc,. Shared Directory -> The path to the directory which is shared by the CIFS Server

	<Folder Name> Disk Usage -> Percentage of the space used on the CIFS Server

	Cifs Version -> Version of the CIFS installed in the Client

	Folder 1,2,etc,. Status -> Domain name of the CIFS Server
