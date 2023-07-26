
Plugin for Apache Mesos Monitoring
==================================

Apache Mesos is an open source cluster manager that handles workloads in a distributed environment through dynamic resource sharing and isolation. Mesos is suited for the deployment and management of applications in large-scale clustered environments.

Configure the host, port, username and password in the python plugin to get the metrics monitored in the Site24x7 Servers


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "mesos_agent"

- Download the below files and place it under the "mesos_agent" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mesos_agent/mesos_agent.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mesos_agent.py script.

- Edit the mesos_agent.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python mesos_agent.py
  #### Linux

- Place the "mesos_agent" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/mesos_agent

  #### Windows 

- Move the folder "mesos_agent" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\mesos_agent


Metrics monitored 
=================

- master_slave_registrations - #Number of agents that were able to cleanly re-join the cluster and connect back to the master after the master is disconnected.
- master_master_slave_reregistrations - #Number of agent re-registrations
- master_slave_removals - #Number of agent removed for various reasons, including maintenance
- master_slave_shutdowns_scheduled - #Number of agents which have failed their health check and are scheduled to be removed. 
- master_slave_shutdowns_canceled - #Number of cancelled agent shutdowns. 
- master_slave_shutdowns_completed - #Number of agents that failed their health check.
- master_slaves_active - #Number of active agents
- master_slaves_connected - #Number of connected agents	
- master_slaves_disconnected - #Number of disconnected agents
- master_slaves_inactive - #Number of inactive agents
