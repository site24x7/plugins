# Apache Spark Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `apache_spark`.
  
```bash
mkdir apache_spark
cd apache_spark/
```
      
- Download below files and place it under the "apache_spark" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/apache_spark/apache_spark.py && sed -i "1s|^.*|#! $(which python3)|" apache_spark.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/apache_spark/apache_spark.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 apache_spark.py --host localhost --port 4040
```

- Provide your apache_spark configurations in apache_spark.cfg file.

```bash
[apache_spark]
host= "localhost"
port= "4040"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "apache_spark" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv apache_spark /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "apache_spark" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Apache Spark Server Monitoring Plugin Metrics

| **Metrics**                                      | **Description**                                                                                           |
|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `Blockmanager Disk Diskspaceused_Mb`                | Amount of disk space used by the block manager in megabytes.                                              |
| `Blockmanager Memory Maxmem_Mb`                     | Maximum memory available to the block manager in megabytes.                                               |
| `Blockmanager Memory Maxoffheapmem_Mb`              | Maximum off-heap memory available to the block manager in megabytes.                                      |
| `Blockmanager Memory Maxonheapmem_Mb`               | Maximum on-heap memory available to the block manager in megabytes.                                       |
| `Blockmanager Memory Memused_Mb`                    | Total memory used by the block manager in megabytes.                                                      |
| `Blockmanager Memory Offheapmemused_Mb`             | Off-heap memory used by the block manager in megabytes.                                                   |
| `Blockmanager Memory Onheapmemused_Mb`              | On-heap memory used by the block manager in megabytes.                                                    |
| `Blockmanager Memory Remainingmem_Mb`               | Remaining memory available for use by the block manager in megabytes.                                     |
| `Blockmanager Memory Remainingoffheapmem_Mb`        | Remaining off-heap memory available for use in megabytes.                                                 |
| `Blockmanager Memory Remainingonheapmem_Mb`         | Remaining on-heap memory available for use in megabytes.                                                  |
| `Dagscheduler Job Activejobs`                       | Number of active jobs in the DAG scheduler.                                                               |
| `Dagscheduler Job Alljobs`                          | Total number of jobs tracked by the DAG scheduler.                                                        |
| `Dagscheduler Stage Failedstages`                   | Number of failed stages in the DAG scheduler.                                                             |
| `Dagscheduler Stage Runningstages`                  | Number of stages currently running in the DAG scheduler.                                                  |
| `Dagscheduler Stage Waitingstages`                  | Number of stages currently waiting to be scheduled in the DAG scheduler.                                  |
| `Executormetrics Directpoolmemory`                  | Memory allocated directly from the pool in bytes.                                                         |
| `Executormetrics Jvmheapmemory`                     | Memory used by the JVM heap in bytes.                                                                     |
| `Executormetrics Jvmoffheapmemory`                  | Memory used by the JVM outside the heap in bytes.                                                         |
| `Executormetrics Majorgccount`                      | Count of major garbage collection events.                                                                 |
| `Executormetrics Majorgctime`                       | Time spent in major garbage collection events in seconds.                                                 |
| `Executormetrics Mappedpoolmemory`                  | Memory mapped directly to the pool in bytes.                                                              |
| `Executormetrics Minorgccount`                      | Count of minor garbage collection events.                                                                 |
| `Executormetrics Minorgctime`                       | Time spent in minor garbage collection events in seconds.                                                 |
| `Executormetrics Offheapexecutionmemory`            | Off-heap memory used for execution in bytes.                                                              |
| `Executormetrics Offheapstoragememory`              | Off-heap memory used for storage in bytes.                                                                |
| `Executormetrics Offheapunifiedmemory`              | Unified off-heap memory usage in bytes.                                                                   |
| `Executormetrics Onheapexecutionmemory`             | On-heap memory used for execution in bytes.                                                               |
| `Executormetrics Onheapstoragememory`               | On-heap memory used for storage in bytes.                                                                 |
| `Executormetrics Onheapunifiedmemory`               | Unified on-heap memory usage in bytes.                                                                    |
| `Executormetrics Processtreejvmrssmemory`           | JVM process tree RSS memory in bytes.                                                                     |
| `Executormetrics Processtreejvmvmemory`             | JVM process tree virtual memory in bytes.                                                                 |
| `Executormetrics Processtreeotherrssmemory`         | Non-JVM process tree RSS memory in bytes.                                                                 |
| `Executormetrics Processtreeothervmemory`           | Non-JVM process tree virtual memory in bytes.                                                             |
| `Executormetrics Processtreepythonrssmemory`        | Python process tree RSS memory in bytes.                                                                  |
| `Executormetrics Processtreepythonvmemory`          | Python process tree virtual memory in bytes.                                                              |
| `Executormetrics Totalgctime`                       | Total garbage collection time in seconds.                                                                 |
| `Jvmcpu Jvmcputime`                                 | Total CPU time used by the JVM in nanoseconds.                                                            |
| `Livelistenerbus Queue Appstatus Size`              | Size of the application status queue in the live listener bus.                                            |
| `Livelistenerbus Queue Executormanagement Size`     | Size of the executor management queue in the live listener bus.                                           |
| `Livelistenerbus Queue Shared Size`                 | Size of the shared queue in the live listener bus.                                                        |
| `Executor Filesystem File Largeread_Ops`            | Number of large read operations on the local filesystem.                                                  |
| `Executor Filesystem File Read_Bytes`              | Total bytes read from the local filesystem.                                                               |
| `Executor Filesystem File Read_Ops`                | Total read operations on the local filesystem.                                                            |
| `Executor Filesystem File Write_Bytes`             | Total bytes written to the local filesystem.                                                              |
| `Executor Filesystem File Write_Ops`               | Total write operations on the local filesystem.                                                           |
| `Executor Filesystem Hdfs Largeread_Ops`           | Number of large read operations on HDFS.                                                                  |
| `Executor Filesystem Hdfs Read_Bytes`              | Total bytes read from HDFS.                                                                               |
| `Executor Filesystem Hdfs Read_Ops`                | Total read operations on HDFS.                                                                            |
| `Executor Filesystem Hdfs Write_Bytes`             | Total bytes written to HDFS.                                                                              |
| `Executor Filesystem Hdfs Write_Ops`               | Total write operations on HDFS.                                                                           |
| `Executor Threadpool Activetasks`                  | Number of active tasks in the executor thread pool.                                                       |
| `Executor Threadpool Completetasks`                | Number of completed tasks in the executor thread pool.                                                    |
| `Executor Threadpool Currentpool_Size`             | Current size of the executor thread pool.                                                                 |
| `Executor Threadpool Maxpool_Size`                 | Maximum size of the executor thread pool.                                                                 |
| `Executor Threadpool Startedtasks`                 | Total number of tasks started in the executor thread pool.                                                |
| `Hiveexternalcatalog Filecachehits`                | Number of hits in the Hive external catalog file cache.                                                   |
| `Hiveexternalcatalog Filesdiscovered`              | Number of files discovered by the Hive external catalog.                                                  |
| `Hiveexternalcatalog Hiveclientcalls`              | Number of calls made to the Hive client by the external catalog.                                          |
| `Hiveexternalcatalog Parallellistingjobcount`      | Number of parallel listing jobs in the Hive external catalog.                                             |
| `Hiveexternalcatalog Partitionsfetched`            | Number of partitions fetched by the Hive external catalog.                                                |
| `Livelistenerbus Numeventsposted`                  | Total number of events posted to the live listener bus.                                                   |
| `Livelistenerbus Queue Appstatus Numdroppedevents` | Number of events dropped in the application status queue.                                                 |
| `Livelistenerbus Queue Executormanagement Numdroppedevents` | Number of events dropped in the executor management queue.                                     |
| `Livelistenerbus Queue Shared Numdroppedevents`    | Number of events dropped in the shared queue.                                                             |
| `Executor Bytesread`                               | Total bytes read by the executor.                                                                         |
| `Executor Byteswritten`                            | Total bytes written by the executor.                                                                      |
| `Executor Cputime`                                 | Total CPU time used by the executor.                                                                      |
| `Executor Deserializecputime`                     | CPU time used for deserializing tasks by the executor.                                                    |
| `Executor Deserializetime`                         | Total time spent deserializing tasks.                                                                     |
| `Executor Diskbytesspilled`                        | Total bytes spilled to disk by the executor.                                                              |
| `Executor Jvmgctime`                               | JVM garbage collection time in milliseconds.                                                              |
| `Executor Memorybytesspilled`                     | Total bytes spilled to memory by the executor.                                                            |
| `Executor Recordsread`                             | Total number of records read by the executor.                                                             |
| `Executor Recordswritten`                          | Total number of records written by the executor.                                                          |
| `Executor Resultserializationtime`                 | Time taken to serialize task results by the executor.                                                     |
| `Executor Resultsize`                              | Size of the serialized task results.                                                                      |
| `Executor Runtime`                                 | Total runtime of the executor.                                                                            |
| `Executor Shufflebyteswritten`                    | Total bytes written during shuffle operations.                                                            |
| `Executor Shufflecorruptmergedblockchunks`         | Number of corrupted merged block chunks encountered during shuffle.                                       |
| `Executor Shufflefetchwaittime`                   | Time spent waiting to fetch shuffle data.                                                                 |
| `Executor Shufflelocalblocksfetched`              | Number of shuffle blocks fetched locally.                                                                 |
| `Executor Shufflelocalbytesread`                  | Total bytes read locally during shuffle operations.                                                       |
| `Executor Shufflemergedfetchfallbackcount`         | Number of fallback fetches during shuffle merged fetch operations.                                        |
| `Executor Shufflemergedlocalblocksfetched`        | Number of shuffle merged blocks fetched locally.                                                          |
| `Executor Shufflemergedlocalbytesread`            | Total bytes read locally during shuffle merged operations.                                                |
| `Executor Shufflemergedlocalchunksfetched`        | Number of shuffle merged chunks fetched locally.                                                          |
| `Executor Shufflemergedremoteblocksfetched`       | Number of shuffle merged blocks fetched remotely.                                                         |
| `Executor Shufflemergedremotebytesread`           | Total bytes read remotely during shuffle merged operations.                                               |
| `Executor Shufflemergedremotechunksfetched`       | Number of shuffle merged chunks fetched remotely.                                                         |
| `Executor Shufflemergedremotereqsduration`        | Total duration of remote shuffle merged fetch requests.                                                   |
| `Executor Shufflerecordsread`                     | Total number of records read during shuffle operations.                                                   |
| `Executor Shufflerecordswritten`                  | Total number of records written during shuffle operations.                                                |
| `Executor Shuffleremoteblocksfetched`             | Number of shuffle blocks fetched remotely.                                                                |
| `Executor Shuffleremotebytesread`                 | Total bytes read remotely during shuffle operations.                                                      |
| `Executor Shuffleremotebytesreadtodisk`           | Total bytes read remotely to disk during shuffle operations.                                              |
| `Executor Shuffleremotereqsduration`              | Total duration of remote shuffle fetch requests.                                                          |
| `Executor Shuffletotalbytesread`                  | Total bytes read during shuffle operations.                                                               |
| `Executor Shufflewritetime`                       | Time spent writing shuffle data.                                                                          |
| `Executor Succeededtasks`                         | Number of tasks successfully executed by the executor.                                                    |


## Sample ScreenShot
![Screenshot from 2024-11-19 15-26-41](https://github.com/user-attachments/assets/ebeda0c3-3638-4a94-a164-cb4185431113)

