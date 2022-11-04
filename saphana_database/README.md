# SAP HANA DATABASE MONITORING

=================================================================
###What is SAP HANA Database ?

	SAP HANA (High-performance ANalytic Appliance) is a column-oriented database that stores data in its memory instead of on a disk. This unique architecture enables SAP HANA to process and query massive amounts of data with near-zero latency, which is significantly faster than other database management systems and allows for advanced real-time analytics.
	
	Monitor the availability and performance of your SAP HANA database with SAP HANA plugin integration.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Install the hdbcli module with the following command

		pip install hdbcli
		
- Ensure the SAP HANA database user has been provided public and monitoring role access:

		GRANT ROLE PUBLIC to user <username>
		GRANT ROLE MONITORING to user <username>

###Plugin Installation

- Create a directory named "saphana_database" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/saphana_database
		
- Download all the files in "saphana_database" folder and place it under the "saphana_database" directory

		
		wget https://raw.githubusercontent.com/site24x7/plugins/master/saphana_database/saphana_database.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/saphana_database/saphana_database.cfg
	
- Add the below configurations in saphana_database.cfg file:

		[saphana_database]
		host = <hostname>
		port = <port>
		username = <username>
		password = <password>

- Execute the below command with appropriate arguments to check for a valid json output.  

		python saphana_database.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> 
		
- To analyze your application logs and identify the exact root cause of the issues, you can make configuration changes by adding logs_enabled, log_type_name, and log_file_path in saphana_database.cfg file

		[saphana_database]
		host=<hostname>
		port=<port>
		username=<username>
		password=<password>
		logs_enabled=True
		log_type_name="saphana_log"
		log_file_path="/usr/sap/<SID>/HDB<Instance number>/<hostname>/trace/*.log"
		
 In the above, fill <SID> with the System ID, <Instance number> with the instance number, and <hostname> with the host name.
 
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center
		
###Metrics Monitored

		1.ACTIVE_THREADS - The number of active threads
		2.ACTIVE_TRANSACTIONS - The number of active transactions
		3.BACKUP_CATALOGS - The total number of backup catalogs
		4.DATA_DISK_FREE_SIZE - The volume of the free size of the data disk
		5.IDLE_CONNECTIONS - The number of idle connections
		6.INACTIVE_TRANSACTIONS - The number of inactive connections
		7.INDEX_SHARED_FREE_SIZE - Free shared memory size of the index module
		8.INDEX_SERVER_MEMORY_POOL_HEAP_USED_SIZE - The amount of pool heap memory that is in use of the index server
		9.INDEX_SERVER_MEMORY_POOL_USED_SIZE - The amount of memory in use from the memory pool of the index server
		10.INDEX_SERVER_MEMORY_POOL_SHARED_USED_SIZE - The amount of pool shared memory that is in use of the index server
		11.LOG_DISK_FREE_SIZE - The volume of the free size of the log disk
		12.NAMESERVER_MEMORY_POOL_HEAP_USED_SIZE - The amount of pool heap memory that is in use of the name server
		13.NAMESERVER_MEMORY_POOL_USED_SIZE - The amount of memory in use from the memory pool of the name server
		14.NAMESERVER_MEMORY_POOL_SHARED_USED_SIZE  - The amount of pool shared memory that is in use of the name server
		15.QUEUING_CONNECTIONS - Total number of connection currently queued
		16.REPLICATION_ERRORS - Number of replication is in error
		17.REPLICATION_SYNCING - Number of syncing replication
		18.RUNNING_CONNECTIONS - Total number of statement is executing
		19.TOTAL_DELTA_MERGE_ERRORS - Total number of table delta merge statistics
		20.TOTAL_EXPENSIVE_STATEMENTS - Total number of expensive statements
		21.TOTAL_NETWORK_IO_OPERATIONS - Total network I/O operations
