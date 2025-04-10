# HBase Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Quick installation

If you're using Linux servers, use the HBase plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/hbase/installer/Site24x7HBasePluginInstaller.sh && sudo bash Site24x7HBasePluginInstaller.sh
```
## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Plugin Installation  

- Create a directory named `hbase`.
  
```bash
mkdir hbase
cd hbase/
```
      
- Download below files and place it under the "hbase" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/hbase/hbase.py && sed -i "1s|^.*|#! $(which python3)|" hbase.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/hbase/hbase.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python hbase.py --host "hostname" --port "port"
```

- Provide your HBase configurations in hbase.cfg file.

```bash
[HBase]
host="localhost"
port="16010"
log_file_path= "/var/log/*hbase*/*.log , /opt/*hbase*/logs/*.log*, /*hbase*/*log*/*.log, C:\\*hbase*\\logs\\*.log*, C:\\Program Files\\*hbase*\\logs\\*.log*"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "hbase" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv hbase /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "hbase" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## HBase Server Monitoring Plugin Metrics

| **Metric Name**                   | **Description**                                                |
|-----------------------------------|----------------------------------------------------------------|
| Hostname                          | Hostname of the HBase master instance.                         |
| Regions Servers                   | Number of active region servers in the cluster.                |
| Dead Region Servers               | Number of dead or unresponsive region servers.                 |
| Cluster Requests                  | Total number of requests processed by the cluster.             |
| Merge Plan Count                  | Number of region merge plans executed.                         |
| Split Plan Count                  | Number of region split plans executed.                         |
| Average Load                      | Average number of regions per region server.                   |
| Free Physical Memory Size         | Amount of free physical memory.                                |
| Free Swap Space Size              | Amount of free swap space.                                     |
| Total Physical Memory Size        | Total physical memory of the system.                           |
| Total Swap Space Size             | Total swap space of the system.                                |
| Committed Virtual Memory Size     | Amount of committed virtual memory.                            |
| VM Name                     | Name of the Java Virtual Machine implementation.               |
| VM Vendor                   | Vendor of the Java Virtual Machine.                            |
| VM Version                  | Version of the Java Virtual Machine.                           |
| Boot Class Path             | Boot class path used by the JVM.                               |
| Library Path                | Native library path used by the JVM.                           |
| Spec Name                   | Name of the JVM specification.                                 |
| Spec Vendor                 | Vendor of the JVM specification.                               |
| Spec Version                | Version of the JVM specification.       

## Assignment Manager

| **Metric Name**             | **Description**                                                |
|-----------------------------|----------------------------------------------------------------|
| Rit Oldest Age              | Age of the oldest Region-In-Transition (RIT).                  |
| Rit Count                   | Total number of Regions in Transition.                         |
| Rit Count Over Threshold    | Count of RITs exceeding the configured threshold.              |
| Rit Duration Min            | Minimum duration of a RIT.                                     |
| Rit Duration Max            | Maximum duration of a RIT.                                     |
| Rit Duration Mean           | Average duration of RITs.                                      |
| Rit Duration Median         | Median duration of RITs.                                       |


## Inter-Process Communication
| **Metric Name**                      | **Description**                                                |
|--------------------------------------|----------------------------------------------------------------|
| IPC Queue Size                       | Size of the IPC queue.                                         |
| IPC Calls In General Queue           | Number of calls in the general IPC queue.                      |
| IPC Calls In Replication Queue       | Number of calls in the replication IPC queue.                  |
| IPC Calls In Priority Queue          | Number of calls in the priority IPC queue.                     |
| IPC Open Connections                 | Total number of open IPC connections.                          |
| IPC Active Handlers                  | Number of active handlers processing IPC requests.             |
| IPC Total Call Time Max              | Maximum total call time for IPC requests.                      |
| IPC Total Call Time Mean             | Mean total call time for IPC requests.                         |
| IPC Total Call Time Median           | Median total call time for IPC requests.                       |
| IPC Total Call Time 99th Percentile  | 99th percentile of total call time for IPC requests.           |
| Sent Data | Total data sent (bytes). |
| Received Data | Total data received (bytes). |
| Out Of Order Scanner Exception | Count of out-of-order scanner exceptions. |
| Unknown Scanner Exception | Count of unknown scanner exceptions. |
| Region Too Busy Exception | Count of region-too-busy exceptions. |

## JVM

| **Metric Name**             | **Description**                                                |
|-----------------------------|----------------------------------------------------------------|
| Mem Non Heap Used           | Amount of non-heap memory used.                                |
| Mem Non Heap Committed      | Amount of committed non-heap memory.                           |
| Mem Non Heap Max            | Maximum non-heap memory available.                             |
| Mem Heap Used               | Amount of heap memory used.                                    |
| Mem Heap Committed          | Amount of committed heap memory.                               |
| Mem Heap Max                | Maximum heap memory available.                                 |
| Mem Max                     | Maximum total memory available.                                |
| GC Count ParNew             | Number of garbage collections using the ParNew collector.      |
| GC Time ParNew              | Total time spent in ParNew garbage collection.                 |
| GC Count CMS                | Number of garbage collections using the CMS collector.         |
| GC Time CMS                 | Total time spent in CMS garbage collection.                    |
| GC Count                    | Total number of garbage collection operations.                 |
| GC Time                     | Total time spent on garbage collection.                        |

## Thread
| **Metric Name**             | **Description**                                                |
|-----------------------------|----------------------------------------------------------------|
| Threads New                 | Number of threads in the 'new' state.                          |
| Threads Runnable            | Number of threads currently running.                           |
| Threads Blocked             | Number of threads blocked waiting for a monitor.              |
| Threads Waiting             | Number of threads in the 'waiting' state.                      |
| Threads Timed Waiting       | Number of threads in the 'timed waiting' state.                |
| Threads Terminated          | Number of threads that have been terminated.                   |

### HLog

| **Metric Name** | **Description** |
|------------------|-----------------|
| HLog Split Time Mean | Mean time to split HLog. |
| HLog Split Time Min | Minimum time to split HLog. |
| HLog Split Time Max | Maximum time to split HLog. |
| HLog Split Time Num Operations | Number of HLog split time operations. |
| HLog Split Size Mean | Mean size of HLog splits. |
| HLog Split Size Min | Minimum size of HLog splits.|
| HLog Split Size Max | Maximum size of HLog splits. |
| HLog Split Size Num Operations | Number of HLog split size operations. |

![image](https://github.com/user-attachments/assets/781d1808-2f19-4bb2-90ae-dde0a505c925)

![image](https://github.com/user-attachments/assets/8f46af69-cdda-4cbe-a488-b6c14e7c055c)

## HBase Logs
![image](https://github.com/user-attachments/assets/2022bb8c-b12c-4939-910d-6e3c4e1bcf18)
