

# Sybase Database Monitoring

## Quick installation

If you're using Linux servers, use the Sybase plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/sybase/installer/Site24x7SybasePluginInstaller.sh && sudo bash Site24x7SybasePluginInstaller.sh
```
## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Prerequisites
- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Run the following command in Sybase terminal to enable monitroing permission of databases
	```
	sp_configure "enable monitoring", 1
	```
	```
	sp_configure 'statement statistics active', 1
	```
	```
	EXEC sp_configure 'per object statistics active', 1
	```
	```
	EXEC sp_configure 'wait event timing', 1
	```
	```
	sp_configure 'statement statistics active', 1
	```

### Linux  

- Create a directory named "sybase".

- Download the below files in the "sybase" folder and place it under the "sybase" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/sybase/sybase.sh
		wget https://raw.githubusercontent.com/site24x7/plugins/master/sybase/sybaseDB.java
		wget https://raw.githubusercontent.com/site24x7/plugins/master/sybase/json-20140107.jar
		wget https://raw.githubusercontent.com/site24x7/plugins/master/sybase/jconn4.jar

- Open sybase.sh file and set the values for HOST, USERNAME, PASSWORD, JAVA_HOME

- Run the command- which java. Copy the output you get and paste it in the JAVA_HOME field. Make sure to paste the path to bin directory and not the path to java.

- Move the "sybase" folder to the site24x7 agent directory
```
  Linux             ->   /opt/site24x7/monagent/plugins/sybase
```
- Once configured the agent will automatically execute the plugin in five minutes interval and send performance data to the Site24x7 data center.

	```	
### Windows

- Create a directory "sybase" 

- Download the files "sybase.bat" , "sybaseDB.java", "json-20140107.jar", "jconn4.jar" and place it under the "sybase" directory:

		https://raw.githubusercontent.com/site24x7/plugins/master/sybase/sybase.bat
		https://raw.githubusercontent.com/site24x7/plugins/master/sybase/sybaseDB.java
		https://raw.githubusercontent.com/site24x7/plugins/master/sybase/json-20140107.jar
		https://raw.githubusercontent.com/site24x7/plugins/master/sybase/jconn4.jar
    		
- Open sybase.bat file and set the values for HOST, USERNAME, PASSWORD, JAVA_HOME

- Run the command- where java. Copy the output of, bin directory of jdk and not the path to java.

- Move the "sybase" into the Site24x7 Windows Agent plugin directory.
```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\sybase
```
- Once configured the agent will automatically execute the plugin in five minutes interval and send performance data to the Site24x7 data center.

## Supported Metrics:
### Overview Metrics 

- **Connection Time**

    Time taken to get connected to the Sybase database ASE server (in nanoseconds).
    
- **Total Memory**

    Total amount of memory available for the ASE server (in MB).

- **Used Memory**

    Amount of memory used by the ASE server (in MB).
    
- **Free Memory**

    Remaining amount of memory available for the ASE server (in MB).
    
- **Used Memory Percentage**

    Amount of memory used by the ASE server (in percentage).

- **Max Remote Connections**

    The number of max remote connections available in the ASE server.

- **Active Remote Connections**

    The number of active remote connections after the ASE server has restarted.
    
- **Max User Connections**

    The number of max user connections available in the ASE server.

- **Active User Connections**

    The number of active user connections after the ASE server has restarted.
    
- **Max Locks**

    Total number of locks configured to be held in the ASE server.

- **Active Locks**

    Number of locks that are in active state.
    
### Cache Details

- **Max Procedure Cache**

    Total amount of procedure cache allocated for Sybase ASE server.

- **Procedure Cache Used**

    Amount of procedure cache that are currently in use.

- **Procedure Cache Used Percentage**

    Percentage of procedure cache used with the max procedure cache.
    
- **Procedure Cache ReUsed**	

    Amount of procedure cache that are currently in reuse.
    
- **Configured Data Cache**

    Amount of data cache configured during the server startup (in MB).
    
- **PhysicalReads**

    Number of buffers read into the cache from disk

- **LogicalReads**

    Number of buffers retrieved from the cache

- **PhysicalWrites**

    Number of buffers written from the cache to disk
    
### Transaction Details

- **Coordinator**

    The coordinator of the transaction

- **State**

    The state of the current transaction like it is started or in process or ended

- **Connection**

    The type of connection

- **Start Time**

    The time at which the transaction started

- **Failover**

    The failover state for the transaction
    
### Database Details

- **DB Name**

    Name of the database instances.

- **Total Size**

    Total amount of space allocated for the database (in MB).
    
- **Used Size**

    Amount of space used in the database (in MB).

- **Used Size (%)**

    Amount of space used in the database (in percentage).
    
- **Log Size**

    Amount of space allocated for logs in the database (in MB).

- **Log Used**

    Amount of space used from the allocated log space in the database (in MB).

- **Log Used (%)**

    Amount of space used from the allocated log space in the database (in percentage).
    
### Backup Database Details

- **DB Name**

    Name of the database.

- **Backup Status**

    Status of the backup performed.

- **Suspended Processes**

    Number of processes that are currently suspended due to the database transaction log being full.

- **Transaction Log Full**

    Indicates whether the database transaction log is full. 













