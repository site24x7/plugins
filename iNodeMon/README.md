Plugin for iNode Monitoring
=============================

iNode is a data structure in a Unix-style file system which stores the attributes and disk block locations of the object's data. Install and use our iNode monitoring tool and get detailed insights into server activity and health.

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.

- To monitor additional inodes, the user can edit line number 19 by adding inodes separated by commas.Example as follows,

		Filesystem={"tmpfs","/dev/root"} 

Get to know how to configure the iNode plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of iNode servers.

Learn more https://www.site24x7.com/plugins/inode-monitoring.html

### Plugin Installation  

- Create a directory named "iNodeMon"

- Download the files and place it under the "iNodeMon" directory.
	```
  	wget https://raw.githubusercontent.com/site24x7/plugins/master/iNodeMon/iNodeMon.py
 	```

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the iNodeMon.py script.
  
- Execute the below command with appropriate arguments to check for the valid JSON output:

      python iNodeMon.py 
