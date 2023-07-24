Plugin for Samba Monitoring
=============================

Samba is an open Source/free Software suite that provides seamless file and print services to SMB/CIFS clients. Install and use our Samba monitoring tool and get detailed insights into server activity and health. Learn how the plugin works.

Get to know how to configure the Samba plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Samba servers.

Learn more https://www.site24x7.com/plugins/samba-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.

### Plugin Installation  

- Create a directory named "samba"

- Download the below files and place it under the "samba" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/samba/samba.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the samba.py script.

- Edit the samba.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python samba.py
  #### Linux

- Place the "samba" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/samba

  #### Windows 

- Move the folder "samba" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\samba
