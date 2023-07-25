Plugin for Zookeeper Monitoring
=============================

Apache Zookeeper is a distributed hierarchical key-value store, which is used to provide a distributed configuration service, synchronization service, and naming registry for large distributed systems. Install and use our Zookeeper monitoring tool and get detailed insights into system activity and health.

Get to know how to configure the Zookeeper plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Zookeeper servers.

Learn more https://www.site24x7.com/plugins/zookeeper-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "zookeeper"

- Download the below files and place it under the "zookeeper" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/zookeeper/zookeeper.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the zookeeper.py script.

- Edit the zookeeper.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python zookeeper.py
  #### Linux

- Place the "zookeeper" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/zookeeper

  #### Windows 

- Move the folder "zookeeper" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\zookeeper
