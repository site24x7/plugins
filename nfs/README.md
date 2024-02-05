Plugin for monitoring the NFS (Network File System)
==============================================

This plugin monitors the performance metrics of NFS mount point status, the IP address of server and client, mount points of server and client, and disk utilization of NFS on the server.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---
##### Linux 

- Create a directory "nfs".

- Open a terminal inside the nfs folder created in the above step and execute the below-mentioned commands to download the plugin files.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/nfs/nfs.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/nfs/nfs.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the nfs.py script.
	
- Configure the mount point to be monitored in the nfs.cfg file, as mentioned below.

		[display_name]
		mount_folder = “/mnt/backup”

- Execute the below command with appropriate arguments to check for the valid JSON output.  

		python nfs.py --mount_folder= “mount_folder_path-1"
  
- Move the directory "nfs" under the Site24x7 Linux Agent plugin directory : 

		Linux       ->   /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and the user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---
	
**Mount Permission:** Mount permission for the client to the mount point.

**Server IP Address:** IP Address of the server connected with the NFS Client.

**Shared Directory:** The path to the directory is shared by the NFS Server.

**Disk Usage:** 
Percentage of the space used on the NFS Server.

**NFS Version:** 
The version of the NFS installed in the Client.

**Total Size:**
Total allocated size on the NFS server.

**Used Size:**
Total used size on the NFS server.

**Avail Size:**
Total Available size in the NFS server.
