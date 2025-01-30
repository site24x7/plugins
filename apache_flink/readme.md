# Apache Flink Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Quick installation

If you're using Linux servers, use the Apache Flink plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/apache_flink/installer/Site24x7ApacheFlinkPluginInstaller.sh && sudo bash Site24x7ApacheFlinkPluginInstaller.sh
```

## Standard Plugin Installation

- Create a directory named `apache_flink`.
  
```bash
mkdir apache_flink
cd apache_flink/
```
      
- Download below files and place it under the "apache_flink" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/apache_flink/apache_flink.py && sed -i "1s|^.*|#! $(which python3)|" apache_flink.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/apache_flink/apache_flink.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 apache_flink.py --host localhost --port 8081
```

- Provide your apache_flink configurations in apache_flink.cfg file.

```bash
[Flink]
host= "localhost"
port= "8081"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "apache_flink" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv apache_flink /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "apache_flink" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Apache Flink Monitoring Metrics

| **Metric Name**                      | **Description**                                                                                      |
|--------------------------------------|------------------------------------------------------------------------------------------------------|
| Total Jobs                           | The total number of jobs currently being managed by the Flink server.                               |
| Total Tasks Running                  | The total number of tasks currently in the running state.                                           |
| Total Tasks Canceling                | The total number of tasks currently in the canceling state.                                         |
| Total Tasks Canceled                 | The total number of tasks that have been canceled.                                                  |
| Total Tasks                          | The total number of tasks, including all states (running, canceling, canceled, etc.).               |
| Total Tasks Created                  | The total number of tasks created by the Flink server.                                              |
| Total Tasks Scheduled                | The total number of tasks currently in the scheduled state.                                         |
| Total Tasks Deploying                | The total number of tasks currently in the deploying state.                                         |
| Total Tasks Reconciling              | The total number of tasks currently in the reconciling state.                                       |
| Total Tasks Finished                 | The total number of tasks that have been successfully completed.                                    |
| Total Tasks Initializing             | The total number of tasks currently in the initializing state.                                      |
| Total Tasks Failed                   | The total number of tasks that have failed.                                                         |
| Blob Server Port                     | The port used for the blob server.                                                                  |
| TaskManager Memory Process Size      | The memory size allocated to the TaskManager process.                                       |
| TaskManager Bind Host                | The IP address or hostname that the TaskManager binds to.                                           |
| JobManager Execution Failover Strategy | The failover strategy used for job execution in the JobManager.                                    |
| JobManager RPC Address               | The address of the JobManager RPC server.                                                           |
| JobManager Memory Off-Heap Size      | The size of off-heap memory allocated to the JobManager.                                    |
| JobManager Memory JVM Overhead Min   | The minimum JVM overhead memory allocated to the JobManager.                                |
| JobManager Memory Process Size       | The total memory size allocated to the JobManager process.                                  |
| Web Temporary Directory              | The temporary directory used for the Flink web dashboard.                                           |
| JobManager RPC Port                  | The port used for the JobManager RPC server.                                                        |
| Query Server Port                    | The port used for the query server.                                                                 |
| REST Bind Address                    | The IP address or hostname that the REST API binds to.                                              |
| JobManager Bind Host                 | The IP address or hostname that the JobManager binds to.                                            |
| Default Parallelism                  | The default parallelism level used for Flink jobs.                                                  |
| TaskManager Number of Task Slots     | The number of task slots available per TaskManager.                                                 |
| REST Address                         | The IP address or hostname of the REST API.                                                         |
| JobManager Memory JVM Metaspace Size | The size of JVM metaspace memory allocated to the JobManager.                               |
| JobManager Memory Heap Size          | The size of heap memory allocated to the JobManager.                                        |
| JobManager Memory JVM Overhead Max   | The maximum JVM overhead memory allocated to the JobManager.                                |
| JVM Version                          | The version of the JVM used by the Flink server.                                                    |
| JVM Architecture                     | The architecture of the JVM.                                                          |
| Refresh Interval                     | The refresh interval (in milliseconds) for monitoring metrics.                                      |
| Timezone Name                        | The name of the timezone in which the Flink server is running.                                      |
| Timezone Offset                      | The timezone offset from UTC.                                                            |
| Flink Version                        | The version of Apache Flink currently running on the server.                                        |
| Flink Revision                       | The revision of the Flink source code used in the current deployment.                               |


![Image](https://github.com/user-attachments/assets/e09b24a3-0674-4b3c-ac32-27044b3eec4b)
