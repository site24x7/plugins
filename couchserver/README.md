Plugin for Couchbase Monitoring
===========

Couchbase is an open source database software which has a document-oriented NoSQL architecture. Install and use our Couchbase monitoring tool and get detailed insights into database activity and health.

Get to know how to configure the Couchbase plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Couchbase servers.

Learn more https://www.site24x7.com/plugins/couchbase-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "couchserver"

- Download the below files and place it under the "couchserver" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/couchserver/couchserver.py


- Edit the couchserver.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python couchserver.py
  #### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the couchserver.py script.
  
- Place the "couchserver" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/couchserver

  #### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

- Move the folder "couchserver" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\couchserver
