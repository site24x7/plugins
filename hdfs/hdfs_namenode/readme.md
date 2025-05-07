# HDFS NameNode Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `hdfs_namenode`.
  
```bash
mkdir hdfs_namenode
cd hdfs_namenode/
```
      
- Download below files and place it under the "hdfs_namenode" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/hdfs/hdfs_namenode/hdfs_namenode.py && sed -i "1s|^.*|#! $(which python3)|" hdfs_namenode.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/hdfs/hdfs_namenode/hdfs_namenode.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python hdfs_namenode.py --host "hostname" --port "port"
```

- Provide your HDFS NameNode configurations in hdfs_namenode.cfg file.

### For Linux

```bash
[global_configurations]
use_agent_python=1

[hdfs]
host=localhost
port=9870
```

### For Windows

```bash
[HDFS]
host="localhost"
port="9870"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "hdfs_namenode" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv hdfs_namenode /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "hdfs_namenode" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## HDFS NameNode Server Monitoring Plugin Metrics

### Summary

| **Metric Name**           | **Description**                                              |
|---------------------------|--------------------------------------------------------------|
| Fatal Logs                | Number of fatal log entries.                                 |
| Error Logs                | Number of error log entries.                                 |
| Warning Logs              | Number of warning log entries.                               |
| Total Logs Info           | Total number of informational log entries.                   |
| Total CPU                 | CPU usage of the process.                                |
| Total Memory              | Total physical memory of the system.                 |
| Free Memory               | Free physical memory available.                      |
| Heap Memory Committed     | Amount of heap memory committed.                     |
| Heap Memory Used          | Heap memory currently in use.                        |
| Non-Heap Memory Committed | Amount of non-heap memory committed.                 |
| Non-Heap Memory Used      | Non-heap memory currently in use.                    |

### Threads

| **Metric Name**             | **Description**                                                |
|-----------------------------|----------------------------------------------------------------|
| New Threads                 | Number of threads in 'new' state.                              |
| Runnable Threads            | Number of actively running threads.                            |
| Blocked Threads             | Threads blocked waiting for a monitor.                         |
| Waiting Threads             | Threads waiting indefinitely.                                  |
| Terminated Threads          | Number of terminated threads.                                  |

### Storage

| **Metric Name**                     | **Description**                                               |
|------------------------------------|---------------------------------------------------------------|
| Total Capacity                     | Total storage capacity of the HDFS cluster.           |
| Used Capacity                      | Storage used across the cluster.                      |
| Remaining Capacity                 | Free/available storage space in the cluster.          |
| Estimated Capacity Lost Total      | Estimated lost capacity due to disk failures.         |
| Total Volume Failures              | Total number of failed volumes across DataNodes.              |

### Blocks

| **Metric Name**                     | **Description**                                               |
|------------------------------------|---------------------------------------------------------------|
| Total Blocks                       | Total number of blocks in the filesystem.                     |
| Total Files                        | Total number of files in the filesystem.                      |
| Corrupted Blocks                   | Number of corrupt blocks detected.                            |
| Missing Blocks                     | Number of missing blocks.                                     |
| Pending Deletion Blocks            | Blocks pending deletion.                                      |
| Pending Replication Blocks         | Blocks waiting to be replicated.                              |
| Scheduled Replication Blocks       | Blocks currently scheduled for replication.                   |
| Under Replicated Blocks            | Blocks that are under the desired replication factor.         |
| Total Load                         | Total active connections to the NameNode.                     |
| Fs Lock Queue Length               | Current lock queue length in the filesystem.                  |
| Maximum Objects                    | Maximum number of objects (files + blocks) allowed.           |

### DataNode

| **Metric Name**                     | **Description**                                               |
|------------------------------------|---------------------------------------------------------------|
| Dead Data Nodes                    | Number of dead/unresponsive DataNodes.                        |
| Decommissioning Dead Data Nodes    | Dead DataNodes being decommissioned.                          |
| Decommissioning Live Data Nodes    | Live DataNodes being decommissioned.                          |
| Total Decommissioning Data Nodes   | Total decommissioning DataNodes.                              |
| Total Live Data Nodes              | Number of live DataNodes in the cluster.                      |
| Total Stale Data Nodes             | Number of stale (delayed heartbeat) DataNodes.                |

## Sample Image

![image](https://github.com/user-attachments/assets/eb78cd7c-abef-45e2-990a-1c5e32515c70)
