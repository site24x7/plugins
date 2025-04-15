# HBase Region Server Monitoring
                                                                                              
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

- Create a directory named `hbase_regionserver`.
  
```bash
mkdir hbase_regionserver
cd hbase_regionserver/
```
      
- Download below files and place it under the "hbase_regionserver" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/hbase_regionserver/hbase_regionserver.py && sed -i "1s|^.*|#! $(which python3)|" hbase_regionserver.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/hbase_regionserver/hbase_regionserver.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python hbase_regionserver.py --host "hostname" --port "port"
```

- Provide your HBase configurations in hbase_regionserver.cfg file.

```bash
[HBase]
host="localhost"
port="16030"
log_file_path= "/var/log/*hbase*/*.log , /opt/*hbase*/logs/*.log*, /*hbase*/*log*/*.log, C:\\*hbase*\\logs\\*.log*, C:\\Program Files\\*hbase*\\logs\\*.log*"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "hbase_regionserver" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv hbase_regionserver /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "hbase_regionserver" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## HBase Region Server Monitoring Plugin Metrics

| **Metric Name**                    | **Description**                                                 |
|-----------------------------------|-----------------------------------------------------------------|
| Free Physical Memory Size         | Amount of free physical memory on the system.                   |
| Free Swap Space Size              | Amount of free swap space available.                            |
| Total Physical Memory Size        | Total physical memory of the system.                            |
| Total Swap Space Size             | Total swap space available.                                     |
| Committed Virtual Memory Size     | Committed virtual memory size.                                  |
| Store File Count                  | Number of store files.                                          |
| Store File Size                   | Total size of all store files.                                  |
| Memstore Size                     | Memory used by Memstore.                                        |
| Put Count                         | Total number of put operations.                                 |
| Delete Count                      | Total number of delete operations.                              |
| Increment Count                   | Total number of increment operations.                           |
| Append Count                      | Total number of append operations.                              |
| HLog File Count                   | Number of HLog files.                                           |
| HLog File Size                    | Total size of HLog files.                                       |
| Compactions Completed Count       | Total number of completed compactions.                          |
| Num Bytes Compacted Count         | Number of bytes compacted during compactions.                   |
| Num Files Compacted Count         | Number of files compacted during compactions.                   |
| Spec Version              | Version of the Java Virtual Machine Specification.      |
| Spec Name                 | Name of the Java Virtual Machine Specification.         |
| Spec Vendor               | Vendor of the JVM specification.                        |
| VM Name                   | Name of the JVM (e.g., OpenJDK 64-Bit Server VM).       |
| VM Vendor                 | Vendor of the JVM.                                      |
| VM Version                | Version of the JVM.                                     |
| Hostname                  | Hostname of the system where HBase is running.          |
| Library Path              | Library path used by the JVM.                           |
| Boot Class Path           | Boot class path used by the JVM.                        |

### Inter-Process Communication

| **Metric Name**                   | **Description**                                                |
|----------------------------------|----------------------------------------------------------------|
| IPC Queue Size                   | Current size of the IPC queue.                                 |
| IPC Calls In General Queue       | Number of pending calls in the general IPC queue.              |
| IPC Calls In Replication Queue   | Number of pending calls in the replication IPC queue.          |
| IPC Calls In Priority Queue      | Number of pending calls in the priority IPC queue.             |
| IPC Open Connections             | Number of active IPC connections.                              |
| IPC Active Handlers              | Number of IPC request handlers currently active.               |
| IPC Total Call Time Max          | Maximum time taken by any IPC call.                            |
| IPC Total Call Time Mean         | Average time taken by IPC calls.                               |
| IPC Total Call Time Median       | Median time taken by IPC calls.                                |
| IPC Total Call Time 99th Percentile | 99th percentile of IPC call times.                          |
| Sent Data                        | Total data sent from the server over IPC.                      |
| Received Data                    | Total data received by the server over IPC.                    |
| Out Of Order Scanner Exception   | Count of out-of-order scanner exceptions.                      |
| Unknown Scanner Exception        | Count of unknown scanner exceptions.                           |
| Region Too Busy Exception        | Count of region-too-busy exceptions.                           |

---

### JVM

| **Metric Name**                   | **Description**                                                |
|----------------------------------|----------------------------------------------------------------|
| Mem Non Heap Used                | Non-heap memory currently used by the JVM.                     |
| Mem Non Heap Committed           | Non-heap memory committed for the JVM.                         |
| Mem Non Heap Max                 | Maximum non-heap memory available to the JVM.                  |
| Mem Heap Used                    | Heap memory currently used by the JVM.                         |
| Mem Heap Committed               | Heap memory committed for the JVM.                             |
| Mem Heap Max                     | Maximum heap memory available to the JVM.                      |
| Mem Max                          | Total maximum memory available to the JVM.                     |
| GC Count ParNew                  | Number of ParNew garbage collection events.                    |
| GC Time ParNew                   | Total time spent in ParNew GC events.                          |
| GC Count CMS                     | Number of CMS garbage collection events.                       |
| GC Time CMS                      | Total time spent in CMS GC events.                             |
| GC Count                         | Total number of garbage collection events.                     |
| GC Time                          | Total time spent on garbage collection.                        |

---

### Thread

| **Metric Name**                   | **Description**                                                |
|----------------------------------|----------------------------------------------------------------|
| Threads New                      | Number of threads in NEW state.                                |
| Threads Runnable                 | Number of threads in RUNNABLE state.                           |
| Threads Blocked                  | Number of threads in BLOCKED state.                            |
| Threads Waiting                  | Number of threads in WAITING state.                            |
| Threads Timed Waiting            | Number of threads in TIMED_WAITING state.                      |
| Threads Terminated               | Number of threads in TERMINATED state.                         |

---

### Table Operations

| **Metric Name**                   | **Description**                                                |
|----------------------------------|----------------------------------------------------------------|
| Total Tables                     | Total number of tables hosted.                                 |
| Total Table Size                 | Combined size of all tables.                                   |
| Total Read Request Count         | Total number of read requests.                                 |
| Total Write Request Count        | Total number of write requests.                                |
| Total Request Count              | Total number of requests (read + write).                       |

---

### Operations Latency

| **Metric Name**                   | **Description**                                                |
|----------------------------------|----------------------------------------------------------------|
| Get Operations                   | Total number of Get operations performed.                      |
| Get Min                          | Minimum latency for Get operations.                            |
| Get Max                          | Maximum latency for Get operations.                            |
| Get Mean                         | Average latency for Get operations.                            |
| Get Median                       | Median latency for Get operations.                             |
| Scan Operations                  | Total number of Scan operations performed.                     |
| Scan Next Min                    | Minimum latency for Scan Next operations.                      |
| Scan Next Max                    | Maximum latency for Scan Next operations.                      |
| Scan Next Mean                   | Average latency for Scan Next operations.                      |
| Scan Next Median                 | Median latency for Scan Next operations.                       |

![image](https://github.com/user-attachments/assets/52d11d8c-3448-4811-a314-1df4adc6f299)

![image](https://github.com/user-attachments/assets/9a9979f1-3393-498f-84ac-175117e094c0)

## HBase Logs

![image](https://github.com/user-attachments/assets/6ba776f5-4759-43a9-a793-ff8d35a665e0)
