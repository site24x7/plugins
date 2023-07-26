
Plugin for Apache Mesos Monitoring
===========

Apache Mesos is an open source cluster manager that handles workloads in a distributed environment through dynamic resource sharing and isolation. Mesos is suited for the deployment and management of applications in large-scale clustered environments.

Configure the host, port, username and password in the python plugin to get the metrics monitored in the Site24x7 Servers


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "mesos_create_operations"

- Download the below files and place it under the "mesos_create_operations" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mesos_create_operations/mesos_create_operations.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mesos_create_operations.py script.

- Edit the mesos_create_operations.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python mesos_create_operations.py
  #### Linux

- Place the "mesos_create_operations" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/mesos_create_operations

  #### Windows 

- Move the folder "mesos_create_operations" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\mesos_create_operations


Metrics monitored 
===========

- dropped
- error
- failed
- finished
- gone_by_operator
- recovering
- total
- unreachable
- disk_dropped
- disk_error
- disk_failed
- disk_finished
- disk_gone_by_operator
- disk_pending
- disk_recovering
- disk_total
- disk_unreachable
