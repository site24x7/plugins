
Plugin for Apache Mesos Monitoring
===========

Apache Mesos is an open source cluster manager that handles workloads in a distributed environment through dynamic resource sharing and isolation. Mesos is suited for the deployment and management of applications in large-scale clustered environments.

Configure the host, port, username and password in the python plugin to get the metrics monitored in the Site24x7 Servers


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "mesos_stats"

- Download the below files and place it under the "mesos_stats" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mesos_stats/mesos_stats.py


- Edit the mesos_stats.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python mesos_stats.py
  #### Linux
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mesos_stats.py script.
- Place the "mesos_stats" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/mesos_stats

  #### Windows 

- Move the folder "mesos_stats" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\mesos_stats


Metrics monitored 
===========
```
cpus_percent
cpus_total
cpus_used
disk_percent
disk_total
disk_used
gpus_percent
gpus_total
gpus_used
mem_percent
mem_total
mem_used
mem_free_bytes
mem_total_bytes
load_1min
load_5min
load_15min
http_cache_hits
uptime_secs
invalid_status_updates
valid_status_updates
logs_ensemble_size
logs_recovered
queued_operations
registry_size_bytes
state_fetch_ms
state_store_ms
```
