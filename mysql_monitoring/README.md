####MYSQL MONITORING

=================================================================
---

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Intsall Pymysql module with following command

		pip install PyMySQL
		
---

### Plugin Installation 

- Create a directory "mysql_monitoring" under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/mysql_monitoring
      
- Download all the files in "mysql_monitoring" folder and place it under the "mysql_monitoring" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_monitoring/mysql_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_monitoring/mysql_monitoring.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python mysql_monitoring.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --database=<job_name> --table = <tablename> 


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---

### Configurations


		[MySQL]
		host = <hostname>
		port = <port>
		username = <username>
		database = <dbname>
		table = <tablename>
		password = <password>
		logs_enabled=<logenabled>
		log_type_name=<logtypename>
		log_file_path=<logfilepath>

- Applog is supported for MySQL Monitoring. To enable applog for this plugin, configure logs_enabled=true and configure log_type_name and log_file_path as need.

---

###Failover monitoring supported
- Receive failover alerts each time there is a failover between master and slave. This will help you ensure that your MySQL environment is always monitored and you receive timely alerts.

---

###Performance metrics

- You can monitor various metrics to stay on top of performance, including those related to MySQL connections, queries, aborted clients and connections, query cache items, handler, read-writes, MyISAM key cache, sort, data transferred, tables, replication, and InnoDB.

- Connections usage metrics


		Maximum connection-Max connections shows the maximum number of connection attempts to the MySQL server.
		Maximum used connections-Max Used Connections displays the maximum number of connections that have been in use simultaneously, since the server started.
		Connection usage-Connection Usage denotes the total number of connections with respect to the percentage of maximum connections in the database. This information can be used to tune the database connections for better performance.

- Queries and questions metrics


		Application queries-Application Queries provides the number of statements executed by the server. This variable includes the statements executed within stored programs.
		Client queries-Client Queries displays the number of statements executed by the server. This includes only the statements sent to the server by clients and not statements executed within stored programs.
		Slow queries-Slow Queries provides the number of queries that have taken more time in seconds than the long_query_time to execute.

- Aborted clients and connections metrics


		Aborted clients-Aborted Clients fetches the number of connections that were aborted because the client died without closing the connection properly.
		Aborted connects-Aborted Connects denotes the number of failed attempts to connect to the MySQL server.

- Table locks waited metrics


		Table locks waited-Table Locks Waited is the number of times the requests for table locks had to wait.

- Query cache items metrics


		Hits-Hits denotes the number of query cache hits. 
		Free memory-Free Memory fetches the amount of free memory in bytes for the query cache.
		Not cached-Not Cached displays the number of non-cached queries. 
		In cache-In Cache denotes the number of queries registered in the query cache.
		Free blocks-Free Blocks displays the number of free memory blocks in the query cache.
		Inserts-Inserts fetches the number of queries added to the query cache.
		Low memory prunes-Low Memory Prunes denotes the number of queries that were deleted from the query cache because of low memory.
		Total blocks-Total Blocks is the total number of blocks in the query cache.

- Handler metrics


		Handler rollback-Handler Rollback denotes the rate of requests to perform an internal rollback operation.
		Handler delete-Handler Delete fetches the number of times the rows in a table have been deleted.
		Handler read first-Handler Read First displays the number of times the first entry in an index was read.
		Handler read key-Handler Read Key provides the number of requests to read a row based on a key.
		Handler random next-Handler Random Next fetches the number of requests to read the next row in the data file.
		Handler read random -Handler Read Random denotes the number of requests to read a row based on a fixed position.
		Handler update-Handler Update fetches the number of requests to update a row in a table.
		Handler write-Handler Write displays the number of requests to insert a row in a table.

- Read write metrics


		Writes-Writes provides the total number of writes done in a MySQL server. It is the sum of inserted queries, replaced queries, updated queries, and deleted queries.
		Reads-Reads fetches the total number of reads done in a MySQL server. Technically, it is the number of selected queries and number of query cache hits.
		Transactions-Transactions denotes the number of transactions.

- Read queries metrics
		Full join-Full Join denotes the number of joins that perform table scans because they do not use indexes.
		Full range join-Full Range Join displays the number of joins that used a range search on a reference table.
		Select range-Select Range shows the number of joins that used ranges on the first table.
		Range check-Range Check fetches the number of joins without keys that check for key usage after each row.
		Select scan-Select Scan provides the number of joins that did a full scan of the first table.
		Maximum execution time exceeded-Max Execution Time Exceeded denotes the number of select statements for which the execution timeout exceeded.

- Write queries metrics


		Commit-Commit provides the number of commit statements executed.
		Commit Select-Commit Select fetches the number of select statements executed.
		Commit delete-Commit Delete displays the number of delete statements executed.
		Commit delete multi-Commit Delete Multi denotes the number of delete statements that use the multiple-table syntax.
		Commit insert-Commit Insert fetches the number of insert statements executed.
		Commit insert select-Commit Insert Select displays the number of insert select statements executed.
		Commit replace select-Commit Replace Select denotes the number of replace select statements executed.
		Commit rollback-Commit Rollback provides the number of rollback statements executed.
		Commit update-Commit Update provides the number of update statements executed.
		Commit update multi-Commit Update Multi shows the number of update statements that use the multiple-table syntax.

- MyISAM key cache metrics


		Blocks not flushed-Blocks Not Flushed shows the number of key blocks in the MyISAM key cache that have changed but have not yet been flushed to disk.
		Read requests-Read Requests denotes the number of requests to read a key block from the MyISAM key cache.
		Key reads-Key Reads displays the number of physical reads of a key block from the disk into the MyISAM key cache
		Write requests-Write Requests fetches the number of requests to write a key block to the MyISAM key cache.
		Key writes-Key Writes shows the number of physical writes of a key block from the MyISAM key cache to disk


- Sort metrics


		Merge passes-Merge Passes denote the number of merge passes that the sort algorithm has had to execute. 
		Range-Range displays the number of sorts that were done using ranges.
		Rows-Rows fetch the number of sorted rows.
		Scan-Scan displays the number of sorts that were done by scanning the table.


- Threads metrics


		Connected-Connected shows the number of currently open connections.
		Running-Running displays the number of threads that are not sleeping.
		Cached-Cached fetches the number of threads in the thread cache.
		Created-Created denotes the number of threads created to handle connections.

- Bytes received and sent metrics
		Received-Received provides the number of bytes received from all clients.
		Sent-Sent displays the number of bytes sent to all clients.

- Table monitoring metrics
		Row length-Row Length provides the average row length in bytes.
		Data length-Data Length displays the length of the data file in bytes.
		Index length-Index Length depicts the length of the index file in bytes.
		Maximum data length-Max Data Length shows the total bytes of data that can be stored in the table.

- Table cache metrics


		Open cache hits-Open Cache Hits displays the number of hits for open tables cache lookups.
		Open cache misses-Open Cache Misses fetches the number of misses for open tables cache lookups.
		Open cache overflows-Open Cache Overflows provides the number of overflows for the open tables cache.

- Created temporary tables metrics 


		Temporary tables-Temporary Tables displays the number of internal temporary tables created by the server while executing statements. 
		Disk tables-Disk Tables denotes the number of internal on-disk temporary tables created by the server while executing statements.
		Temporary files-Temporary Files shows the number of internal temporary tables created by the server while executing statements.

- InnoDB metrics


		Buffer pool pages data-Buffer Pool Pages Data displays the number of pages in the InnoDB buffer pool containing data.
		Buffer pool pages dirty-Buffer Pool PagesDirty denotes the current number of dirty pages in the InnoDB buffer pool.
		Buffer pool pages free-Buffer Pool Pages Free provides the number of free pages in the InnoDB buffer pool.
		Buffer pool pages total-Buffer Pool Pages Total fetches the total number of pages in the InnoDB buffer pool.
		Buffer pool wait free-Buffer Pool Wait Free shows the number of times a read or write to InnoDB had to wait as clean pages were not available in the buffer pool.
		Log waits -Log Waits displays the number of times the log buffer was too small and a wait was required for it to be flushed before continuing.
		Row lock time average-Row Lock Time Avg denotes time to acquire a row lock for InnoDB tables, in milliseconds.
		Row lock waits-Row Lock Waits shows the number of times operations on InnoDB tables had to wait for a row lock.
		Buffer pool pages flushed-Buffer Pool Pages Flushed fetches the number of requests to flush pages from the InnoDB buffer pool.
		Buffer pool read ahead evicted-Buffer Pool Read Ahead Evicted denotes the number of pages that read into the InnoDB buffer pool by the read-ahead background thread that were subsequently evicted without having been accessed by queries.
		Buffer pool read ahead -buffer Pool Read Ahead displays the number of pages that read into the InnoDB buffer pool by the read-ahead background thread.
		Buffer pool read ahead random-Buffer Pool Read Ahead Random denotes the number of random read-aheads that  were initiated by InnoDB. 
		Buffer pool read requests-Buffer Pool Read Requests fetches the number of logical read requests.
		Buffer pool reads-Buffer Pool Reads shows the number of logical reads that InnoDB could not satisfy from the buffer pool, and had to read directly from disk.
		Buffer pool write requests-Buffer Pool Write Requests fetches the number of writes in the InnoDB buffer pool.
		Data fsync-Data Fsyncs displays the number of fsync() operations per second.
		Data pending fsync-Data Pending Fsyncs shows the current number of pending fsync() operations.
		Data pending reads-Data Pending Reads provides the current number of pending reads.
		Data pending writes-Data Pending Writes denotes the current number of pending writes.
		Data reads-Data Reads shows the number of data reads.
		Data writes-Data Writes displays the number of data writes.
		Data write requests-Log Write Requests denotes the number of write requests for the InnoDB redo log file.
		Log writes-Log Writes depicts the number of physical writes to the InnoDB redo log file.
		OS log fsyncs-Os Log Fsyncs provides the number of fsync() writes done to the InnoDB redo log files.
		OS log pending fsyncs-Os Log Pending Fsyncs fetches the number of pending fsync() operations for the InnoDB redo log files.
		OS log pending writes-Os Log Pending Writes shows the number of pending writes to the InnoDB redo log files.
		OS log written-Os Log Written displays the number of bytes written to the InnoDB redo log files.
		Pages created-Pages Created denotes the number of pages created by operations on InnoDB tables.
		Pages read-Pages Read depicts the number pages read from the InnoDB buffer pool by operations on InnoDB tables.
		Pages written-Pages Written fetches the number of pages written by operations on InnoDB tables.
		Rows deleted-Rows Deleted provides the number of rows deleted from InnoDB tables.
		Rows inserted-Rows Inserted shows the number of rows inserted into InnoDB tables.
		Rows read-Rows Read denotes the number of rows read from InnoDB tables.
		Rows updated-Rows Updated depicts the number of rows updated in InnoDB tables.

- Replication metrics


		Slave IO state-Slave IO State shows the state of what a thread is doing, such as trying to connect to the source, waiting for events from the source, reconnecting to the source, and so on. 
		Slave IO running-Slave IO Running displays if the I/O thread has started and connected successfully to the source.
		Slave SQL running-Slave Sql Running shows if the SQL thread has started.
		Slave running-Slave Running denotes if a slave is running or not.
		Connect retry-Connect Retry provides the time between connect retires, in seconds.
		Last IO error number-Last IO Errno denotes the error number of the most recent error that caused the I/O thread to stop.
		Last SQL error number-Last Sql Errno provides the error number of the most recent error that caused the SQL thread to stop.
		Master host-Master Host is the source host that the replica is connected to.
		Master retry count-Master Retry Count provides the number of times the replica can attempt to reconnect to the source in the event of a lost connection. 
		Master server ID-Master Server ID is the server ID value from the source.
		Master user-Master User is the user name of the account used to connect to the source.
		Relay log space-Relay Log Space is the total combined size of all existing relay log files in bytes.
		Seconds behind master-Seconds Behind Master is the difference in seconds between the slave’s clock time and the timestamp of the query, when it was recorded in the master’s binary log.
		Skip counter-Skip Counter denotes the number of events from the source that a replica server should skip.


