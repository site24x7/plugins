
Plugin for Apache Mesos Monitoring
=================================

Apache Mesos is an open source cluster manager that handles workloads in a distributed environment through dynamic resource sharing and isolation. Mesos is suited for the deployment and management of applications in large-scale clustered environments.

Configure the host, port, username and password in the python plugin to get the metrics monitored in the Site24x7 Servers



## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "mesos_master"

- Download the below files and place it under the "mesos_master" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mesos_master/mesos_master.py


- Edit the mesos_master.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python mesos_master.py
  #### Linux
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mesos_master.py script.
- Place the "mesos_master" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/mesos_master

  #### Windows 

- Move the folder "mesos_master" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\mesos_master


Metrics monitored 
=================

- dropped_messages
- elected
- event_queue_dispatches
- event_queue_http_requests
- event_queue_messages
- frameworks_active
- frameworks_connected
- frameworks_disconnected
- frameworks_inactive
