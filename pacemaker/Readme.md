# Pacemaker cluster monitoring

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

## Plugin Installation  
- Create a directory named `pacemaker`.
  
	```bash
	mkdir pacemaker
 	cd pacemaker/
  	```
 
- Download all the files under the `pacemaker` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/pacemaker/pacemaker.py
	```

- Execute the below command with appropriate arguments to check for the valid JSON output:

	```bash
	python pacemaker.py
	```

- Move the `pacemaker` directory to the Site24x7 Linux Agent plugin directory: 

	```bash
	mv pacemaker /opt/site24x7/monagent/plugins/
	```
 
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Metrics Captured

Name		        	             | 	Description
---         			             |   	---
Cluster Name                   |  The Name of the Cluster
Stack                          |  Shows the underlying cluster software components
Nodes Configured               |  Total number of nodes in the cluster
Online Nodes                   |  No of nodes that are online
offline Nodes                  |  No of nodes that are offline
Resource Instances Configured  |  Total number of managed resources
Resource Status                |  Current operational state of each resource
Service Metrics                |  Current state of the services
Expected Votes                 |  Total number of votes possible in the cluster
Highest Expected               |  Maximum possible votes in current configuration
Total Votes                    |  Current total voting power
Quorum                         |  Minimum votes needed for cluster operation
Flag                           | Configuration of the cluster
Node Status                    |  Shows the current state of each node.

#### Sample Images:

![image](https://github.com/user-attachments/assets/2c222708-bd12-441f-8216-a18b96367646)
![image](https://github.com/user-attachments/assets/57e01ce4-a0ad-43e8-a5f0-363b76527601)
![image](https://github.com/user-attachments/assets/e85ba0fd-0cd0-4d95-a4ac-957a5293523b)


