
Plugin for Apache Mesos Monitoring
===========

Apache Mesos is an open source cluster manager that handles workloads in a distributed environment through dynamic resource sharing and isolation. Mesos is suited for the deployment and management of applications in large-scale clustered environments.

Configure the host, port, username and password in the python plugin to get the metrics monitored in the Site24x7 Servers

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "mesos_messages"

- Download the below files and place it under the "mesos_messages" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mesos_messages/mesos_messages.py


- Edit the mesos_messages.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python mesos_messages.py
  #### Linux
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mesos_messages.py script.
- Place the "mesos_messages" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/mesos_messages

  #### Windows 

- Move the folder "mesos_messages" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\mesos_messages


Metrics monitored 
===========
```
messages_deactivate_framework
messages_decline_offers
messages_executor_to_framework
messages_exited_executor
messages_framework_to_executor
messages_kill_task
messages_launch_tasks
messages_operation_status_update

messages_reconcile_operations
messages_reconcile_tasks
messages_register_framework
messages_register_slave
messages_reregister_framework
messages_reregister_slave
messages_deactivate_framework
messages_resource_request

messages_revive_offers
messages_status_update
messages_suppress_offers
messages_unregister_framework

messages_unregister_slave
messages_update_slave
messages_status_update_acknowledgement
messages_operation_status_update_acknowledgement
```
