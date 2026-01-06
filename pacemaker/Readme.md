# Pacemaker cluster monitoring

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

## Plugin Installation  

## Linux

- Create a directory named `pacemaker`.
  
	```bash
	mkdir pacemaker
 	cd pacemaker/
  	```
 
- Download all the files under the `pacemaker` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/pacemaker/pacemaker.cfg
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

The plugin will be using Site24x7 Linux agent Python.

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Metrics Captured

### Cluster Summary

Name		        	             | 	Description
---         			             |   	---
Cluster Name                   |  The name of the cluster
Stack                          |  Shows the underlying cluster software components
Current DC                     |  Current Designated Coordinator node with version and partition status
Last Updated                   |  Timestamp when the cluster status was last refreshed
Last Change                    |  Timestamp of the last cluster configuration change
Nodes Configured               |  Total number of nodes configured in the cluster
Online Nodes                   |  Number of nodes that are currently online
Offline Nodes                  |  Number of nodes that are currently offline
Resource Instances Configured  |  Total number of managed resources configured

### Daemon Status

Name                           | 	Description
---         			       |   	---
Corosync                       |  Status of Corosync service
Pacemaker                      |  Status of Pacemaker service
Pacemaker_Remote               |  Status of Pacemaker Remote service
Pcsd                           |  Status of PCS daemon service

### Quorum Information

Name		        	       | 	Description
---         			       |   	---
Expected Votes                 |  Total number of votes possible in the cluster
Highest Expected               |  Maximum possible votes in current configuration
Total Votes                    |  Current total voting power
Quorum                         |  Minimum votes needed for cluster operation
Flags                          |  Quorum status flags

### Nodes Table

Displays individual node information in a tabular format:

Field                          | 	Description
---         			       |   	---
Name                           |  Name of the cluster node
Status                         |  Current status of the node

### Resources Table

Displays individual resource information in a tabular format:

Field                          | 	Description
---         			       |   	---
Name                           |  Name of the resource
State                          |  Current operational state of the resource

#### Sample Images:

