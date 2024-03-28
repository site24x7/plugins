

# Oracle Database Monitoring

## Quick installation

If you're using Linux servers, use the Oracle plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle/installer/Site24x7OraclePluginInstaller.sh && bash Site24x7OraclePluginInstaller.sh
```
## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Prerequisites
- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.7 or higher version should be installed.
- Install **oracledb** module for python
	```
	pip3 install oracledb
	```

- Roles need to be granted

	```
	grant select_catalog_role to {username}
	```
	```
	grant create session to {username}
	```

### Installation  

- Create a directory named "oracle".
- Install the **oracledb** python module.
	```
	pip3 install oracledb
	```

	
- Download the below files in the "oracle" folder and place it under the "oracle" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle/oracle.py && sed -i "1s|^.*|#! $(which python3)|" oracle.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle/oracle.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```
	 python3 oracle.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME>
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the oracle.cfg file.
	```
		[ORCL]
		hostname = "localhost"
		port = "1521"
		sid = "ORCL"
		username = "oracle_username"
		password = "oracle_password"
		tls = "false"
		wallet_location = "/opt/oracle/product/19c/dbhome_1/network/admin/wallets"
		oracle_home = "/opt/oracle/product/19c/dbhome_1/"
		logs_enabled = "false"
		log_type_name = "None"
		log_file_path = "None"
	```	
#### Linux
- Place the "oracle" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/oracle
#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further, move the folder "OracleCore" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\oracle


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics:
### System Metrics 

- **Soft Parse Ratio**

    The Soft Parse Ratio Oracle metric is the ratio of soft parses

- **Total Parse Count Per Sec**

    The total number of parses per second

- **Total Parse Count Per Txn**

    The total number of parses per transaction

- **Hard Parse Count Per Sec**

    The total number hard parses per second

- **Hard Parse Count Per Txn**

    The number of hard parses per transaction

- **Parse Failure Count Per Sec**

    The number of failed parses per second

- **Parse Failure Count Per Txn**

    The number of failed parses per transaction

- **Temp Space Used**

    Temporary space used

- **Session Count**

    Total count of sessions

- **Session Limit %**

    Max number of concurrent connections allowed by db

- **Database Wait Time Ratio**

    Ratio of amount of CPU used to the amount of total db time

- **Memory Sorts Ratio**

    Percentage of sorts that are done to disk vs. in-memory

- **Disk Sort Per Sec**

    The number of sorts going to disk per second for this sample period

- **Rows Per Sort**

    Average number of rows per sort during this sample period

- **Total Sorts Per User Call**

    Total number of sorts per user call

- **User Rollbacks Per Sec**

    Number of times, per second during the sample period, that users manually issue the ROLLBACK statement

- **SQL Service Response Time**

    The average elapsed time per execution of a representative set of SQL statements

- **Long Table Scans Per Sec**

    Number of long and short table scans per second during the sample period

- **Average Active Sessions**

    Number of sessions, either working or waiting for a resource at a specific point in time

- **Logons Per Sec**

    The number of logons per second during the sample period

- **Global Cache Blocks Lost**

    Number of global cache blocks lost over the user-defined observation period

- **Global Cache Blocks Corrupted**

    Number of blocks that encountered a corruption or checksum failure during interconnect over the user-defined observation period


- **GC CR Block Received Per Second**

    Number of GC CR block received per second

- **Enqueue Timeouts Per Sec**

    Total number of table and row locks per second that time out before they could complete

- **Physical Writes Per Sec**

    The number of direct physical writes per second

- **Physical Reads Per Sec**

    The number of direct physical reads per second

- **Shared Pool Free %**

    Percentage of free space in shared pool

- **Library Cache Hit Ratio**

    The number of pin requests which result in pin hits

- **Cursor Cache Hit Ratio**

    Ratio of the number of times an open cursor was found divided by the number of times a cursor was sought

- **Buffer Cache Hit Ratio**

    The percentage of pages found in the buffer cache without having to read from disk

- **Dict Cache Hit Ratio**

    The measure  of ratio of dictionary hits to misses

- **Rman Failed Backup Count**

    Count of RMAN failed backups

- **Long Running Query**

    Count of long running queries


### PGA Metrics

- **Total PGA Allocated**

    Total amount of memory provided currently

- **Total Freeable PGA Memory**

    The amount of PGA memory that can be reallocated or given back to the operating system

- **Maximum PGA Allocated**

    Maximum amount of memory provided currently

- **Total PGA Inuse**

    Total amount of memory inuse

### Oracle Blocking Locks

- **Blocking Locks**

    Total count of blocking locks

### PDB Metrics

- **PDB ID**

    ID of the PDB

### SGA Metrics

- **SGA Database Buffers**
  
    Portion of the SGA used to cache data blocks read from disk

- **SGA Fixed Size**

    Fixed portion of the SGA that contains information such as internal data structures and the shared pool

- **SGA Hit Ratio**

   Measure of how often the database finds the data it needs in the SGA without having to read from disk

- **SGA Log Alloc Retries**

   Number of times a redo log buffer allocation request has to be retried due to contention or unavailability

- **SGA Redo Buffers**

    Portion of the SGA used to hold redo log entries before they are written to disk

- **SGA Shared Pool Dict Cache Ratio**

    Ratio represents the efficiency of caching dictionary data in the shared pool
  
- **SGA Shared Pool Lib Cache Hit Ratio**

    The efficiency of caching library cache data in the shared pool

- **SGA Shared Pool Lib Cache Reload Ratio**

    Ratio of reloads of library cache entries from disk to the total number of lookups

- **SGA Shared Pool Lib Cache Sharable Statement**

    Number of statements in the library cache that are shareable among different sessions

- **SGA Shared Pool Lib Cache Shareable User**

    Number of shareable library cache entries for a specific user

- **SGA Variable Size**

    Size of variable portion of the SGA
  
- **Total Memory**

   Total size of the SGA, which is the sum of the fixed and variable components

### Oracle Tablespace Metrics

- **Name**
  
    Name of the tablespace

- **Used Space**

    Tablespace used space in MB

- **Tablepsace Size***

    Tablespace size in MB

- **Used Percent**

    Tablespace usage in percent(%)

- **TB_Status**

    Availability of the tablespace

### Oracle Wait Metrics


- **Free Buffer Waits**

- **Buffer Busy Waits**

- **Latch Free**

- **Library Cache Pin**

- **Library Cache Load Lock**

- **Log Buffer Space**

- **Library Object Reloads Count**

- **Enqueue Waits**

- **DB File Parallel Read**

- **DB File Parallel Write**

- **Control File Sequential Read**

- **Control File Parallel Write**

- **Write Complete Waits**

- **Log File Sync**

- **Sort Segment Request**

- **Direct Path Read**

- **Direct Path Write**
