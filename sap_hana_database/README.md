# SAP HANA DATABASE MONITORING


### What is SAP HANA ?

SAP HANA (High-performance ANalytic Appliance) is a column-oriented database that stores data in its memory instead of on a disk. This unique architecture enables SAP HANA to process and query massive amounts of data with near-zero latency, which is significantly faster than other database management systems and allows for advanced real-time analytics.
	
Monitor the availability and performance of your SAP HANA database with SAP HANA plugin integration.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Install the hdbcli module with the following command

		pip install hdbcli
		
-  Ensure the SAP HANA user profile that will be added in the sap_hana_database.cfg file has been provided public and monitoring role access:

		GRANT ROLE PUBLIC to user <username>
		GRANT ROLE MONITORING to user <username>

### Plugin Installation

- Create a directory named "sap_hana_database" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/sap_hana_database
		
- Download all the files in "sap_hana_database" folder and place it under the "sap_hana_database" directory

		
		wget https://raw.githubusercontent.com/site24x7/plugins/master/sap_hana_database/sap_hana_database.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/sap_hana_database/sap_hana_database.cfg
	
- Add the below configurations in sap_hana_database.cfg file:

		[sap_hana_database]
		host = <hostname>
		port = <port>
		username = <username>
		password = <password>

- Execute the below command with appropriate arguments to check for a valid json output:  

		python sap_hana_database.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> 
		
- To analyze your sap hana database logs and identify the exact root cause of the issues, you can make configuration changes by adding logs_enabled, log_type_name, and log_file_path in sap_hana_database.cfg file

		[sap_hana_database]
		host=<hostname>
		port=<port>
		username=<username>
		password=<password>
		logs_enabled=True
		log_type_name="saphana_log"
		log_file_path="/usr/sap/<SID>/HDB<Instance number>/<hostname>/trace/*.log"
		
 In the above, fill <SID> with the System ID, <Instance number> with the instance number, and <hostname> with the host name.
 
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center
		
### Performance Metrics

		1.Active Threads - The number of active threads
		2.Active Transactions - The number of active transactions
		3.Backup Catalogs - The total number of backup catalogs
		4.DATA Disk Free Size - The volume of the free size of the data disk
		5.Idle Connections - The number of idle connections
		6.Inactive Transactions - The number of inactive connections
		7.Index Server Memory Pool Heap Used Size - The amount of pool heap memory that is in use of the index server
		8.Index Server Memory Pool Used Size - The amount of memory in use from the memory pool of the index server
		9.Index Server Memory Pool Shared Used Size - The amount of pool shared memory that is in use of the index server
		10.LOG Disk Free Size - The volume of the free size of the log disk
		11.Name Server Memory Pool Heap Used Size - The amount of pool heap memory that is in use of the name server
		12.Name Server Memory Pool Used Size - The amount of memory in use from the memory pool of the name server
		13.Name Server Memory Pool Shared Used Size  - The amount of pool shared memory that is in use of the name server
		14.Queuing Connections - The total number of connections currently queued
		15.Replication Errors - The number of replications that have in errors
		16.Replication Syncing - The number of syncing replications
		17.Running Connections - The total number of statement is executing
		18.Total Delta Merge Errors - The total number of table delta merge statistics
		19.Total Expensive Statements - The total number of expensive statements
		20.Total Network I/O Operations - The total network I/O operations
		21.Total Column Unloads - The total number of column unloads
