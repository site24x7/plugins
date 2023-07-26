Plugin for CouchDB Monitoring
===========

Apache CouchDB is open source database software which has a document-oriented NoSQL architecture. Install and use our CouchDB monitoring tool and get detailed insights into database activity and health.

Get to know how to configure the CouchDB plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of CouchDB servers.

Learn more https://www.site24x7.com/plugins/couchdb-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "couchdb"

- Download the below files and place it under the "couchdb" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/couchdb/couchdb.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the couchdb.py script.

- Edit the couchdb.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python couchdb.py
  #### Linux

- Place the "couchdb" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/couchdb

  #### Windows 

- Move the folder "couchdb" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\couchdb
