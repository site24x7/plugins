# SAP HANA DATABASE MONITORING

=================================================================
###What is SAP HANA Database ?

	As an in-memory database, SAP HANA places data storage, analytics capabilities, and transactions which load data on the same level of RAM storage. This reduces the amount of time needed to access and manipulate data, resulting in decreased processing time. In order to quickly access all this data, SAP HANA utilizes high-compression rates in both columnar and row storage, saves only one copy of data to avoid bloat, and categorizes data based on its necessity and age keeping only what it needs in-memory. The remainder of the data is then kept on the SAP HANA disk, and in some cases, in external storage.SAP HANA has the ability to connect to data lakes and other stores of big data and intelligently process the information.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Intsall hdbcli module with following command

		pip install hdbcli
		
- To monitor sap hana database user required public and monitoring role

		GRANT ROLE PUBLIC to user <username>
		GRANT ROLE MONITORING to user <username>

###Plugin Installation

- Create a directory "saphana_database" under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/saphana_database
		
- Download all the files in "saphana_database" folder and place it under the "saphana_database" directory

		
		wget https://raw.githubusercontent.com/site24x7/plugins/master/saphana_database/saphana_database.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/saphana_database/saphana_database.cfg
	
- Add the configuration in saphana_database.cfg

		[saphana_database]
		host = <hostname>
		port = <port>
		username = <username>
		password = <password>

- Execute the below command with appropriate arguments to check for the valid json output.  

		python saphana_database.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> 


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

###Metrics Monitored

		1.ACTIVE_THREADS - Number of active threads
		2.ACTIVE_TRANSACTIONS - Number of active transactions
		3.BACKUP_CATALOGS - total number of backup catalogs
		4.DATA_DISK_FREE_SIZE - The volume of the free size of the data disk
		5.IDLE_CONNECTIONS - Number of idle connections
		6.INACTIVE_TRANSACTIONS - Number of inactive connections
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
