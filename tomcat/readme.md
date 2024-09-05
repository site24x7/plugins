# Tomcat Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Provide the appropriate roles to the Tomcat user. To do this, follow the steps below:

	#### Linux

	- Navigate to below directory.

		`/opt/tomcat/conf`
		
	- Open the tomcat-users.xml file.

	- Add the below roles to the user.

		`<user username="user" password="user" roles="manager-gui,admin-gui"/>`  
    		`<user username="user" password="user" roles="manager-script"/>`
  		
	- Restart the tomcat server.
		
	#### Windows

	- Navigate to the below directory.  

		`<tomcat_dowloaded_directory>\conf`
		
	- Open the tomcat-users.xml file.
 	-  Add the below roles to the user.

		`<user username="user" password="user" roles="manager-gui,admin-gui"/>`  
  		`<user username="user" password="user" roles="manager-script"/>`

- Restart the Tomcat server after the above changes.
---

## Quick installation

If you're using Linux servers, use the Tomcat plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/tomcat/Installer/Site24x7tomcatPluginInstaller.sh && sudo bash Site24x7TomcatPluginInstaller.sh
```
## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Plugin Installation  

- Create a directory named `tomcat`.
  
```bash
mkdir tomcat
cd tomcat/
```
      
- Download below files and place it under the "tomcat" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/tomcat/tomcat.py && sed -i "1s|^.*|#! $(which python3)|" tomcat.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/tomcat/tomcat.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python tomcat.py --host "hostname" --port "port" --username "username" --password "password"
```

- Provide your Tomcat configurations in tomcat.cfg file.

```bash
[tomcat]
host = "localhost"
port = "8080"
username = "admin"
password = "admin"
plugin_version = "1"
logs_enabled = "true"
log_type_name = "Tomcat Access Logs"
log_file_path = "/opt/*tomcat*/logs/*access*.txt"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "tomcat" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv tomcat /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "tomcat" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

# Tomcat Server Monitoring Plugin Metrics

| **Metric Name**                           | **Description**                                                                |
|-------------------------------------------|--------------------------------------------------------------------------------|
| Available Memory                          | The amount of memory currently available for use by the Tomcat server.          |
| Bytes Received                            | The total number of bytes received by the server.                               |
| Bytes Sent                                | The total number of bytes sent by the server.                                   |
| Error Count                               | The total number of errors encountered by the server.                           |
| Free Memory                               | The amount of free memory available in the JVM heap.                            |
| Max Memory                                | The maximum memory limit for the JVM running the Tomcat server.                 |
| Name                                      | The name of the Tomcat server or instance.                                      |
| Percent Used Memory                       | The percentage of memory used out of the total allocated memory.                |
| Processing Time                           | The total time spent processing requests on the server.                         |
| Request Count                             | The total number of requests processed by the server.                           |
| Thread Allowed                            | The maximum number of threads allowed for the server to handle requests.        |
| Thread Busy                               | The current number of busy threads processing requests.                         |
| Thread Count                              | The current total number of threads allocated for request processing.           |
| Tomcat Version                            | The version of the Tomcat server.                                               |
| Total Memory                              | The total memory currently allocated to the JVM.                                |
| Usage Code Heap Non Nmethods              | The amount of non-method code memory used in the JVM's code heap.               |
| Usage Code Heap Non Profiled Nmethods     | The amount of memory used in the JVM's code heap for non-profiled nmethods.     |
| Usage Code Heap Profiled Nmethods         | The amount of memory used in the JVM's code heap for profiled nmethods.         |
| Usage Compressed Class Space              | The amount of memory used in the JVM's compressed class space.                  |
| Usage G1 Eden Space                       | The amount of memory used in the G1 Eden space region.                          |
| Usage G1 Old Gen                          | The amount of memory used in the G1 Old Generation region.                      |
| Usage G1 Survivor Space                   | The amount of memory used in the G1 Survivor space region.                      |
| Usage Metaspace                           | The amount of memory used in the JVM's metaspace.                               |
| Used Memory                               | The total amount of memory currently in use by the JVM.                         |

# Memory Metrics

| **Metric Name**            | **Description**                                                                |
|----------------------------|--------------------------------------------------------------------------------|
| Available Memory           | The amount of memory currently available for use by the Tomcat server.          |
| Free Memory                | The amount of free memory available in the JVM heap.                            |
| Max Memory                 | The maximum memory limit for the JVM running the Tomcat server.                 |
| Total Memory               | The total memory currently allocated to the JVM.                                |
| Used Memory                | The total amount of memory currently in use by the JVM.                         |
| Percent Used Memory        | The percentage of memory used out of the total allocated memory.                |

# JVM CodeHeap Usage

| **Metric Name**                           | **Description**                                                                |
|-------------------------------------------|--------------------------------------------------------------------------------|
| Usage CodeHeap Non Nmethods               | The amount of non-method code memory used in the JVM's CodeHeap.                |
| Usage CodeHeap Non Profiled Nmethods      | The amount of memory used in the JVM's CodeHeap for non-profiled nmethods.      |
| Usage CodeHeap Profiled Nmethods          | The amount of memory used in the JVM's CodeHeap for profiled nmethods.          |

# JVM Memory Pool Usage

| **Metric Name**                  | **Description**                                                                |
|----------------------------------|--------------------------------------------------------------------------------|
| Usage Compressed Class Space     | The amount of memory used in the JVM's compressed class space.                  |
| Usage G1 Eden Space              | The amount of memory used in the G1 Eden space region.                          |
| Usage G1 Old Gen                 | The amount of memory used in the G1 Old Generation region.                      |
| Usage G1 Survivor Space          | The amount of memory used in the G1 Survivor space region.                      |
| Usage Metaspace                  | The amount of memory used in the JVM's metaspace.                               |
