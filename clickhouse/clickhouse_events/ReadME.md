Clickhouse monitoring
---  
ClickHouse is a fast open-source OLAP database management system. For more details, refer their website: https://clickhouse.tech

### Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.
- Clickhouse Python Driver
https://clickhouse-driver.readthedocs.io/en/latest/installation.html

- To install the driver, execute the command :
	```
	pip install clickhouse-driver
	```

### Plugin Installation  

- Create a directory named "clickhouse_events"

- Download the below files and place it under the "clickhouse_events" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/clickhouse/clickhouse_events/clickhouse_events.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/clickhouse/clickhouse_events/clickhouse_events.cfg


- Edit the clickhouse_events.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python clickhouse_events.py --hostname = <hostname-or-ip> --port = <port>  --database = <db> --user = <username> --password = <password> --timeout = <timeout>
#### Configurations

- Edit the clickhouse_events.cfg with appropriate configurations
	```
	[localhost]
	hostname = localhost
	port = 9000
	database = default
	user = default
	password = 
	timeout = 10
	```
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the clickhouse_events.py script.

- Place the "clickhouse_events" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/clickhouse_events

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "clickhouse_events" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\clickhouse_events

### Metrics Captured
    ArenaAllocBytes
    ArenaAllocChunks
    CompressedReadBufferBlocks
    CompressedReadBufferBytes
    ContextLock
    CreatedReadBufferOrdinary
    CreatedWriteBufferOrdinary
    DiskReadElapsedMicroseconds
    DiskWriteElapsedMicroseconds
    FailedQuery
    FailedSelectQuery
    FileOpen
    FunctionExecute
    IOBufferAllocBytes
    IOBufferAllocs
    InsertedBytes
    InsertedRows
    Merge
    MergeTreeDataWriterBlocks
    MergeTreeDataWriterBlocksAlreadySorted
    MergeTreeDataWriterCompressedBytes
    MergeTreeDataWriterRows
    MergeTreeDataWriterUncompressedBytes
    MergedRows
    MergedUncompressedBytes
    MergesTimeMilliseconds
    NetworkReceiveElapsedMicroseconds
    NetworkSendElapsedMicroseconds
    OSCPUVirtualTimeMicroseconds
    OSCPUWaitMicroseconds
    OSWriteBytes
    OSWriteChars
    Query
    RWLockAcquiredReadLocks
    RWLockReadersWaitMilliseconds
    ReadBufferFromFileDescriptorRead
    ReadBufferFromFileDescriptorReadBytes
    ReadCompressedBytes
    RealTimeMicroseconds
    RegexpCreated
    SelectQuery
    SoftPageFaults
    SystemTimeMicroseconds
    UserTimeMicroseconds
    WriteBufferFromFileDescriptorWrite
    WriteBufferFromFileDescriptorWriteBytes
