# MYSQL MONITORING

=================================================================


### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Install python with version>=3.7 
- To create a MySQL user:

		CREATE USER username@hostname IDENTIFIED BY 'password';
		
  Select on queries permission is required to execute the queries mentioned above.
  
		GRANT SELECT ON mysql.* TO username@hostname IDENTIFIED BY password;
		
  For Example, create a user called 'site24x7' with 'site24x7' as password. Give Select permission, SUPER or REPLICATION CLIENT privilege(s)  for the 'site24x7' user and  flush the privileges:
  
		CREATE USER site24x7@localhost IDENTIFIED BY 'site24x7';
		GRANT SELECT ON mysql.* TO site24x7@localhost IDENTIFIED BY 'site24x7';
		use mysql;
  		UPDATE mysql.user SET Super_Priv='Y' WHERE user='site24x7' AND host='localhost';  (or)
  		UPDATE mysql.user SET Repl_client_priv='Y' WHERE user='site24x7' AND host='localhost';
		FLUSH PRIVILEGES;

  For MariaDB, use the following command:
  
		CREATE USER site24x7@localhost IDENTIFIED BY 'site24x7';
		GRANT SUPER ON *.* TO 'site24x7'@'localhost';
		GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'site24x7'@'localhost'; 
		FLUSH PRIVILEGES;

---
### Plugin Installation 

- Create a directory "mysql_monitoring".
- Copy and execute the below command under the "mysql_monitoring" folder to download the pymysql module.
	
		wget https://github.com/site24x7/plugins/raw/master/mysql_monitoring/pymysql/pymysql.zip && unzip pymysql.zip && rm pymysql.zip
		
- Download  the below files in "mysql_monitoring" folder and place it under the "mysql_monitoring" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_monitoring/mysql_monitoring.py && sed -i "1s|^.*|#! $(which python3)|" mysql_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_monitoring/mysql_monitoring.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python mysql_monitoring.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> 

- After above command with parameters gives expected output, please configure the relevant parameters in the mysql_monitoring.cfg file.

		[MySQL]
		host = <hostname>
		port = <port>
		username = <username>
		password = <password>
		logs_enabled=<logenabled>
		log_type_name=<logtypename>
		log_file_path=<logfilepath>

- Applog is supported for MySQL Monitoring. To enable applog for this plugin, configure logs_enabled=true and configure log_type_name and log_file_path as need.

- Place the "mysql_monitoring" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/mysql_monitoring
---

### Failover monitoring supported
- Receive failover alerts each time there is a failover between master and slave. This will help you ensure that your MySQL environment is always monitored and you receive timely alerts.

---

### Performance metrics

- You can monitor various metrics to stay on top of performance, including those related to MySQL connections, queries, aborted clients and connections, query cache items, handler, read-writes, MyISAM key cache, sort, data transferred, tables, replication, and InnoDB.

#### Connections usage metrics


		1.Maximum connection-Max connections shows the maximum number of connection attempts to the MySQL server.
		2.Maximum used connections-Max Used Connections displays the maximum number of connections that have been in use simultaneously, since the server started.
		3.Connection usage-Connection Usage denotes the total number of connections with respect to the percentage of maximum connections in the database. This information can be used to tune the database connections for better performance.

#### Queries and questions metrics


		1.Application queries-Application Queries provides the number of statements executed by the server. This variable includes the statements executed within stored programs.
		2.Client queries-Client Queries displays the number of statements executed by the server. This includes only the statements sent to the server by clients and not statements executed within stored programs.
		3.Slow queries-Slow Queries provides the number of queries that have taken more time in seconds than the long_query_time to execute.

#### Aborted clients and connections metrics


		1.Aborted clients-Aborted Clients fetches the number of connections that were aborted because the client died without closing the connection properly.
		2.Aborted connects-Aborted Connects denotes the number of failed attempts to connect to the MySQL server.

#### Table locks waited metrics


		1.Table locks waited-Table Locks Waited is the number of times the requests for table locks had to wait.

#### Query cache items metrics


		1.Hits-Hits denotes the number of query cache hits. 
		2.Free memory-Free Memory fetches the amount of free memory in bytes for the query cache.
		3.Not cached-Not Cached displays the number of non-cached queries. 
		4.In cache-In Cache denotes the number of queries registered in the query cache.
		5.Free blocks-Free Blocks displays the number of free memory blocks in the query cache.
		6.Inserts-Inserts fetches the number of queries added to the query cache.
		7.Low memory prunes-Low Memory Prunes denotes the number of queries that were deleted from the query cache because of low memory.
		8.Total blocks-Total Blocks is the total number of blocks in the query cache.

#### Handler metrics


		1.Handler rollback-Handler Rollback denotes the rate of requests to perform an internal rollback operation.
		2.Handler delete-Handler Delete fetches the number of times the rows in a table have been deleted.
		3.Handler read first-Handler Read First displays the number of times the first entry in an index was read.
		4.Handler read key-Handler Read Key provides the number of requests to read a row based on a key.
		5.Handler random next-Handler Random Next fetches the number of requests to read the next row in the data file.
		6.Handler read random -Handler Read Random denotes the number of requests to read a row based on a fixed position.
		7.Handler update-Handler Update fetches the number of requests to update a row in a table.
		8.Handler write-Handler Write displays the number of requests to insert a row in a table.

#### Read write metrics


		1.Writes-Writes provides the total number of writes done in a MySQL server. It is the sum of inserted queries, replaced queries, updated queries, and deleted queries.
		2.Reads-Reads fetches the total number of reads done in a MySQL server. Technically, it is the number of selected queries and number of query cache hits.
		3.Transactions-Transactions denotes the number of transactions.

#### Read queries metrics


		1.Full join-Full Join denotes the number of joins that perform table scans because they do not use indexes.
		2.Full range join-Full Range Join displays the number of joins that used a range search on a reference table.
		3.Select range-Select Range shows the number of joins that used ranges on the first table.
		4.Range check-Range Check fetches the number of joins without keys that check for key usage after each row.
		5.Select scan-Select Scan provides the number of joins that did a full scan of the first table.
		6.Maximum execution time exceeded-Max Execution Time Exceeded denotes the number of select statements for which the execution timeout exceeded.

#### Write queries metrics


		1.Commit-Commit provides the number of commit statements executed.
		2.Commit Select-Commit Select fetches the number of select statements executed.
		3.Commit delete-Commit Delete displays the number of delete statements executed.
		4.Commit delete multi-Commit Delete Multi denotes the number of delete statements that use the multiple-table syntax.
		5.Commit insert-Commit Insert fetches the number of insert statements executed.
		6.Commit insert select-Commit Insert Select displays the number of insert select statements executed.
		7.Commit replace select-Commit Replace Select denotes the number of replace select statements executed.
		8.Commit rollback-Commit Rollback provides the number of rollback statements executed.
		9.Commit update-Commit Update provides the number of update statements executed.
		10.Commit update multi-Commit Update Multi shows the number of update statements that use the multiple-table syntax.

#### MyISAM key cache metrics


		1.Blocks not flushed-Blocks Not Flushed shows the number of key blocks in the MyISAM key cache that have changed but have not yet been flushed to disk.
		2.Read requests-Read Requests denotes the number of requests to read a key block from the MyISAM key cache.
		3.Key reads-Key Reads displays the number of physical reads of a key block from the disk into the MyISAM key cache
		4.Write requests-Write Requests fetches the number of requests to write a key block to the MyISAM key cache.
		5.Key writes-Key Writes shows the number of physical writes of a key block from the MyISAM key cache to disk


#### Sort metrics


		1.Merge passes-Merge Passes denote the number of merge passes that the sort algorithm has had to execute. 
		2.Range-Range displays the number of sorts that were done using ranges.
		3.Rows-Rows fetch the number of sorted rows.
		4.Scan-Scan displays the number of sorts that were done by scanning the table.


#### Threads metrics


		1.Connected-Connected shows the number of currently open connections.
		2.Running-Running displays the number of threads that are not sleeping.
		3.Cached-Cached fetches the number of threads in the thread cache.
		4.Created-Created denotes the number of threads created to handle connections.

#### Bytes received and sent metrics


		1.Received-Received provides the number of bytes received from all clients.
		2.Sent-Sent displays the number of bytes sent to all clients.

#### Table monitoring metrics


		1.Row length-Row Length provides the average row length in bytes.
		2.Data length-Data Length displays the length of the data file in bytes.
		3.Index length-Index Length depicts the length of the index file in bytes.
		4.Maximum data length-Max Data Length shows the total bytes of data that can be stored in the table.

#### Table cache metrics


		1.Open cache hits-Open Cache Hits displays the number of hits for open tables cache lookups.
		2.Open cache misses-Open Cache Misses fetches the number of misses for open tables cache lookups.
		3.Open cache overflows-Open Cache Overflows provides the number of overflows for the open tables cache.

#### Created temporary tables metrics 


		1.Temporary tables-Temporary Tables displays the number of internal temporary tables created by the server while executing statements. 
		2.Disk tables-Disk Tables denotes the number of internal on-disk temporary tables created by the server while executing statements.
		3.Temporary files-Temporary Files shows the number of internal temporary tables created by the server while executing statements.

#### InnoDB metrics


		1.Buffer pool pages data-Buffer Pool Pages Data displays the number of pages in the InnoDB buffer pool containing data.
		2.Buffer pool pages dirty-Buffer Pool PagesDirty denotes the current number of dirty pages in the InnoDB buffer pool.
		3.Buffer pool pages free-Buffer Pool Pages Free provides the number of free pages in the InnoDB buffer pool.
		4.Buffer pool pages total-Buffer Pool Pages Total fetches the total number of pages in the InnoDB buffer pool.
		5.Buffer pool wait free-Buffer Pool Wait Free shows the number of times a read or write to InnoDB had to wait as clean pages were not available in the buffer pool.
		6.Log waits -Log Waits displays the number of times the log buffer was too small and a wait was required for it to be flushed before continuing.
		7.Row lock time average-Row Lock Time Avg denotes time to acquire a row lock for InnoDB tables, in milliseconds.
		8.Row lock waits-Row Lock Waits shows the number of times operations on InnoDB tables had to wait for a row lock.
		9.Buffer pool pages flushed-Buffer Pool Pages Flushed fetches the number of requests to flush pages from the InnoDB buffer pool.
		10.Buffer pool read ahead evicted-Buffer Pool Read Ahead Evicted denotes the number of pages that read into the InnoDB buffer pool by the read-ahead background thread that were subsequently evicted without having been accessed by queries.
		11.Buffer pool read ahead -buffer Pool Read Ahead displays the number of pages that read into the InnoDB buffer pool by the read-ahead background thread.
		12.Buffer pool read ahead random-Buffer Pool Read Ahead Random denotes the number of random read-aheads that  were initiated by InnoDB. 
		13.Buffer pool read requests-Buffer Pool Read Requests fetches the number of logical read requests.
		14.Buffer pool reads-Buffer Pool Reads shows the number of logical reads that InnoDB could not satisfy from the buffer pool, and had to read directly from disk.
		15.Buffer pool write requests-Buffer Pool Write Requests fetches the number of writes in the InnoDB buffer pool.
		16.Data fsync-Data Fsyncs displays the number of fsync() operations per second.
		17.Data pending fsync-Data Pending Fsyncs shows the current number of pending fsync() operations.
		18.Data pending reads-Data Pending Reads provides the current number of pending reads.
		19.Data pending writes-Data Pending Writes denotes the current number of pending writes.
		20.Data reads-Data Reads shows the number of data reads.
		21.Data writes-Data Writes displays the number of data writes.
		22.Data write requests-Log Write Requests denotes the number of write requests for the InnoDB redo log file.
		23.Log writes-Log Writes depicts the number of physical writes to the InnoDB redo log file.
		24.OS log fsyncs-Os Log Fsyncs provides the number of fsync() writes done to the InnoDB redo log files.
		25.OS log pending fsyncs-Os Log Pending Fsyncs fetches the number of pending fsync() operations for the InnoDB redo log files.
		26.OS log pending writes-Os Log Pending Writes shows the number of pending writes to the InnoDB redo log files.
		27.OS log written-Os Log Written displays the number of bytes written to the InnoDB redo log files.
		28.Pages created-Pages Created denotes the number of pages created by operations on InnoDB tables.
		29.Pages read-Pages Read depicts the number pages read from the InnoDB buffer pool by operations on InnoDB tables.
		30.Pages written-Pages Written fetches the number of pages written by operations on InnoDB tables.
		31.Rows deleted-Rows Deleted provides the number of rows deleted from InnoDB tables.
		32.Rows inserted-Rows Inserted shows the number of rows inserted into InnoDB tables.
		33.Rows read-Rows Read denotes the number of rows read from InnoDB tables.
		34.Rows updated-Rows Updated depicts the number of rows updated in InnoDB tables.

#### Replication metrics


		1.Slave IO state-Slave IO State shows the state of what a thread is doing, such as trying to connect to the source, waiting for events from the source, reconnecting to the source, and so on. 
		2.Slave IO running-Slave IO Running displays if the I/O thread has started and connected successfully to the source.
		3.Slave SQL running-Slave Sql Running shows if the SQL thread has started.
		4.Slave running-Slave Running denotes if a slave is running or not.
		5.Connect retry-Connect Retry provides the time between connect retires, in seconds.
		6.Last IO error number-Last IO Errno denotes the error number of the most recent error that caused the I/O thread to stop.
		7.Last SQL error number-Last Sql Errno provides the error number of the most recent error that caused the SQL thread to stop.
		8.Master host-Master Host is the source host that the replica is connected to.
		9.Master retry count-Master Retry Count provides the number of times the replica can attempt to reconnect to the source in the event of a lost connection. 
		10.Master server ID-Master Server ID is the server ID value from the source.
		11.Master user-Master User is the user name of the account used to connect to the source.
		12.Relay log space-Relay Log Space is the total combined size of all existing relay log files in bytes.
		13.Seconds behind master-Seconds Behind Master is the difference in seconds between the slave’s clock time and the timestamp of the query, when it was recorded in the master’s binary log.
		14.Skip counter-Skip Counter denotes the number of events from the source that a replica server should skip.


_The pymysql source can be found [here](https://github.com/PyMySQL/PyMySQL/tree/main)._

_Zoho Corporation has made this into one single [zip file](https://github.com/site24x7/plugins/tree/master/mysql_monitoring/pymysql/pymysql.zip) and is licensed under the same [license](https://github.com/PyMySQL/PyMySQL/blob/main/LICENSE) which can be found [here](https://github.com/site24x7/plugins/tree/master/mysql_monitoring/pymysql/LICENSE.txt)._


