
Plugin for Zombies Process Monitoring
=====================================

Calculate the number of "zombie" processes created in the server using this plugin.

Learn more about the plugin installation steps and the various performance metrics that you can monitor here - https://www.site24x7.com/plugins/zombie-process-monitoring.html
## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


## Plugin Installation  

- Create a directory named `zombies`.

	```bash
 	mkdir zombies
 	cd zombies
 	```

- Download the below files and place it under the `zombies` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/zombies/zombies.cfg
	wget https://raw.githubusercontent.com/site24x7/plugins/master/zombies/zombies.py && sed -i "1s|^.*|#! $(which python3)|" zombies.py
	```

- Edit the zombies.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

	```bash
	python zombies.py
	```
 
- Place the `zombies` folder under Site24x7 Linux Agent plugin directory : 

	```bash
	mv zombies /opt/site24x7/monagent/plugins/
 	```

## Metrics Captured
---

| Metric                        | Description                                                                 |
|-------------------------------|------------------------------------------------------------------------------|
| zombies                       | Total number of zombie (defunct) processes currently active in the system.  |
| Unique Users with Zombies     | Number of unique users who own zombie processes.                            |
| Unique Parent Commands        | Number of unique parent processes that spawned zombie processes.            |
| Longest Running Zombie (Elapsed) | Elapsed time of the longest-running zombie process.                     |
| zombie_process_details         | Detailed information of each zombie process including PID, PPID, User, Elapsed time, State, Command, and Parent Command. |

## Sample Image
<img width="1627" height="925" alt="image" src="https://github.com/user-attachments/assets/707d41fa-8c80-4df4-bb6a-22f5cd641763" />
