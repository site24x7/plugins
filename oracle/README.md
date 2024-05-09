

# Oracle Database Monitoring

## Quick installation

If you're using Linux servers, use the Oracle plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle/installer/Site24x7OraclePluginInstaller.sh && sudo bash Site24x7OraclePluginInstaller.sh
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



- **Average Active Sessions**

    Number of sessions, either working or waiting for a resource at a specific point in time


- **Buffer Busy Waits Time Waited**

    Total time the Oracle database spends waiting for data buffers in the buffer cache to become available due to contention for the same blocks.

- **Buffer Busy Waits Wait Count**

     Number of times the Oracle database has had to wait for data buffers in the buffer cache to become available due to contention for the same blocks.

- **Current SCN**

    The current logical timestamp of the Oracle database, reflecting the point in time in terms of committed changes or transactions.

- **Database Wait Time Ratio**

    Ratio of amount of CPU used to the amount of total db time


- **Dict Cache Hit Ratio**

    The measure of ratio of dictionary hits to misses


- **Disk Sort Per Sec**

    The number of sorts going to disk per second for this sample period


- **FRA Number of Files**

    Total number of files currently stored in the Oracle database's Flash Recovery Area (FRA), which includes backups, archived redo logs, and other recovery-related files.

- **FRA Space Limit**

    Total amount of storage space allocated for the Oracle database's Flash Recovery Area (FRA), which includes backups, archived redo logs, and other recovery-related files.

- **FRA Space Reclaimable**

    Amount of space in the Flash Recovery Area (FRA) that can be reclaimed or reused, typically after backups or archived files are no longer needed or have been transferred.

- **FRA Space Used**

    Amount of space currently being utilized in the Flash Recovery Area (FRA) for storing backups, archived redo logs, and other recovery-related files.

- **Free Buffer Waits Time Waited**

    Total time the Oracle database spends waiting for a free buffer in the buffer cache to become available, indicating possible buffer cache size issues or intense contention.

- **Free Buffer Waits Wait Count**

    The number of times the database has had to wait for a free buffer in the buffer cache due to a lack of available space or intense concurrent access to buffers.

- **GC CR Block Received Per Second**

    Number of GC CR block received per second


- **Global Cache Blocks Corrupted**

    Number of blocks that encountered a corruption or checksum failure during interconnect over the user-defined observation period


- **Invalid Index Count**

    Number of indexes in the Oracle database that are currently in an invalid state, meaning they are unusable for query optimization due to changes in the underlying table structure or other reasons.


- **Library Cache Hit Ratio**

    The number of pin requests which result in pin hits


- **Logons Per Sec**

    The number of logons per second during the sample period


- **Long Running Queries**

    Count of long running queries


- **Long Table Scans Per Sec**

    Number of long and short table scans per second during the sample period


- **Memory Sorts Ratio**

    Percentage of sorts that are done to disk vs. in-memory


- **Number of Session Users**

    Tracks the current count of distinct user sessions connected to the Oracle database.

- **Response Time**

    Time taken for a database query to execute and return results.

- **Rman Failed Backup Count**

    Count of RMAN failed backups


- **Rows Per Sort**

    Average number of rows per sort during this sample period


- **SQL Service Response Time**

    The average elapsed time per execution of a representative set of SQL statements


- **Session Count**

    Total count of sessions


- **Session Limit %**

    Max number of concurrent connections allowed by db


- **Shared Pool Free %**

    Percentage of free space in shared pool


- **Sort Segment Request Time Waited**

    Total time an Oracle database spends waiting for space to be allocated in a sort segment for sorting operations

- **Sort Segment Request Wait Count**

    Number of times the Oracle database has had to wait for space allocation in a sort segment for sorting operations

- **Temp Space Used**

    Temporary space used


- **Total Freeable PGA Memory**

    The amount of PGA memory that can be reallocated or given back to the operating system


- **Total Memory**

    Total size of the SGA, which is the sum of the fixed and variable components


- **Total Sorts Per User Call**

    Total number of sorts per user call


- **User Rollbacks Per Sec**


    Number of times, per second during the sample period, that users manually issue the ROLLBACK statement


### Parsing and Execution
- **Cursor Cache Hit Ratio**

    Ratio of the number of times an open cursor was found divided by the number of times a cursor was sought.

- **Hard Parse Count Per Sec**

    The total number hard parses per second.


- **Hard Parse Count Per Txn**

    The number of hard parses per transaction.


- **Parse Failure Count Per Sec**

    The number of failed parses per second.



- **Parse Failure Count Per Txn**

    The number of failed parses per transaction.


- **Soft Parse Ratio**

    The Soft Parse Ratio Oracle metric is the ratio of soft parses.


- **Total Parse Count Per Sec**

    The total number of parses per second.


- **Total Parse Count Per Txn**

    The total number of parses per transaction



### Input/Output
- **Control File Parallel Write Time Waited**

    Total time the Oracle database spends waiting for parallel write operations to control files

- **Control File Parallel Write Wait Count**

    Number of times the database has experienced a wait during parallel write operations to control files

- **Control File Sequential Read Time Waited**

    Total time the database spends waiting for sequential read operations from control files

- **Control File Sequential Read Wait Count**

    The number of times the database has had to wait during sequential read operations from control files

- **Db File Parallel Read Time Waited**

    Total time the database spends waiting for parallel read operations from data files

- **File Parallel Read Wait Count**

    Number of times the database has had to wait during parallel read operations from data files

- **Db File Parallel Write Time Waited**

    Total time the database spends waiting for parallel write operations to data files

- **Db File Parallel Write Wait Count**

    Number of times the database has had to wait during parallel write operations to data files

- **Direct Path Read Time Waited**

    Total time the database spends waiting for direct path read operations

- **Direct Path Read Wait Count**

    Number of times the database has had to wait during direct path read operations

- **Direct Path Write Time Waited**

    Total time the database spends waiting for direct path write operations

- **Direct Path Write Wait Count**

    Number of times the database has had to wait during direct path write operations

- **Log Buffer Space Time Waited**

    Total time the database spends waiting for space in the log buffer

- **Log Buffer Space Wait Count**

    Number of times the database has had to wait for space in the log buffer

- **Log File Sync Time Waited**

    Total time the database spends waiting for a redo log file synchronization

- **Log File Sync Wait Count**

    Number of times the database has had to wait for a redo log file synchronization

- **Physical Reads Per Sec**

    The number of direct physical reads per second


- **Physical Writes Per Sec**

    Number of physical write operations to disk (data files, control files, or redo logs) that occur per second

- **Write Complete Waits Time Waited**

    Total time the Oracle database spends waiting for a write operation to complete

- **Write Complete Waits Wait Count**

    Number of times the database has had to wait for a write operation to complete

### Buffer Cache and Memory

- **Buffer Cache Hit Ratio**

    The percentage of pages found in the buffer cache without having to read from disk


- **Database Block Size**

    Size of a block of data in the Oracle database

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


- **Total PGA Allocated**

    Total amount of memory provided currently


- **Total PGA Inuse**

    Total amount of memory inuse



### Locks and Contention
- **Blocking Locks**

    Total count of blocking locks


- **Enqueue Timeouts Per Sec**

    Total number of table and row locks per second that time out before they could complete


- **Latch Free Time Waited**

    Total time the Oracle database spends waiting for a latch to become available

- **Latch Free Wait Count**

    Number of times the Oracle database has experienced a wait due to contention for a latch

- **Library Cache Load Lock Time Waited**

    Total time the database spends waiting for a library cache load lock

- **Library Cache Load Lock Wait Count**

    Number of times the database has had to wait for a library cache load lock

- **Library Cache Pin Time Waited**

    Total time the database spends waiting for a library cache pin

- **Library Cache Pin Wait Count**

    Number of times the database has had to wait for a library cache pin

### Oracle Tablespace Metrics
- **Name**
  
    Name of the tablespace

- **Used_Space**

    Tablespace used space in MB

- **Tablepsace_Size***

    Tablespace size in MB

- **Used_Percent**

    Tablespace usage in percent(%)

- **TB_Status**

    Availability of the tablespace

### Oracle Tablespace Datafile Metrics
- **Name**
  
    Name of the tablespace datafile

- **Data_File_Blocks**

    Number of datafile blocks

- **Data_File_Size**

    Size of the datafile

- **Increment_By**

    The size by which the datafile should grow automatically when it reaches its maximum size

- **Max_Data_File_Blocks**

    Maximum blocks of the datafile

- **Max_Data_File_Size**

    Maximum size of the datafile

- **Usable_Data_File_Blocks**

    Number of usable data file blocks

- **Usable_Data_File_Size**

    Size of usable data file

### PDB Metrics

- **Block_Size**

   Size of the block

- **PDB_ID**

   ID of the PDB

- **PDB_Size**

   Size of the PDB
