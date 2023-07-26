Plugin for VoltDB Monitoring
=============================

VoltDB is an in-memory operational database which uses a share-nothing architecture to achieve database parallelism. Troubleshoot all your database performance issues using key metrics presented as detailed graphs and data.

Get to know how to configure the Oracle VoltDB plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of VoltDB servers.

Learn more https://www.site24x7.com/plugins/voltdb-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "voltdb_memory"

- Download the below files and place it under the "voltdb_memory" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/voltdb_memory/voltdb_memory.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the voltdb_memory.py script.

- Edit the voltdb_memory.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python voltdb_memory.py
  #### Linux

- Place the "voltdb_memory" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/voltdb_memory

  #### Windows 

- Move the folder "voltdb_memory" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\voltdb_memory
