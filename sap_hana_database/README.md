# SAP HANA DATABASE MONITORING


### What is SAP HANA ?

SAP HANA (High-performance ANalytic Appliance) is a column-oriented database that stores data in its memory instead of on a disk. This unique architecture enables SAP HANA to process and query massive amounts of data with near-zero latency, which is significantly faster than other database management systems and allows for advanced real-time analytics.
	
Monitor the availability and performance of your SAP HANA database with SAP HANA plugin integration.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Install the hdbcli module with the following command

		pip install hdbcli
		
- hdbcli driver supports for python 2.7, python 3.4 and above.
		
-  Ensure the SAP HANA user profile that will be added in the sap_hana_database.cfg file has been provided public and monitoring role access:

		GRANT ROLE PUBLIC to user username
		GRANT ROLE MONITORING to user username

### Plugin Installation

- Create a directory named "sap_hana_database".
		
- Download all the files in "sap_hana_database" folder and place it under the "sap_hana_database" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/sap_hana_database/sap_hana_database.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/sap_hana_database/sap_hana_database.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the sap_hana_database.py script.
	
- Add the below configurations in sap_hana_database.cfg file:

		[sap_hana_database]
		host = "host"
		port = "port"
		username = "username"
		password = "password"

- Execute the below command with appropriate arguments to check for a valid json output:  

		python sap_hana_database.py --host "host" --port "port" --username "username" --password "password"
		
- To analyze your sap hana database logs and identify the exact root cause of the issues, you can make configuration changes by adding logs_enabled, log_type_name, and log_file_path in sap_hana_database.cfg file

		[sap_hana_database]
		host="host"
		port="port"
		username="username"
		password="password"
		logs_enabled=True
		log_type_name="saphana_log"
		log_file_path="/usr/sap/<SID>/HDB<Instance number>/<hostname>/trace/*.log"
		
 In the above, fill in the System ID, Instance number and hostname with applicable details.
 
- Move the directory "sap_hana_database" under the Site24x7 Linux Agent plugin directory: 

		mv sap_hana_database /opt/site24x7/monagent/plugins/
 
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
		
### Performance Metrics
Name		            			| 	Description
---         		   			|  	 ---
1.Active Threads 				| 	The number of active threads
2.Active Transactions 				|	The number of active transactions
3.Backup Catalogs 				|	The total number of backup catalogs
4.CPU Usage 					|	CPU Used by all processes in %
5.DATA Disk Free Size 				|	The volume of the free size of the data disk
6.Disk Free Size 				|	Disk free size in GB
7.Free Physical Memory 				|	Specifies the free physical memory on the host in GB
8.Idle Connections 				|	The number of idle connections
9.Inactive Transactions 			|	The number of inactive connections
10.Index Server Memory Pool Heap Used Size 	| 	The amount of pool heap memory that is in use of the index server
11.Index Server Memory Pool Used Size 		|	The amount of memory in use from the memory pool of the index server
12.Index Server Memory Pool Shared Used Size 	|	The amount of pool shared memory that is in use of the index server
13.LOG Disk Free Size 				|	The volume of the free size of the log disk
14.Name Server Memory Pool Heap Used Size 	|	The amount of pool heap memory that is in use of the name server
15.Name Server Memory Pool Used Size 		|	The amount of memory in use from the memory pool of the name server
16.Name Server Memory Pool Shared Used Size  	|	The amount of pool shared memory that is in use of the name server
17.Plan Cache Hit Ratio 			|	SQL Plan Cache hit ratio
18.Plan Cache Size 				|	Total size of SQL Plan Cache in GB
19.Queuing Connections 				|	Total number of connection currently queued
20.Replication Errors 				|	Number of replication is in error
21.Replication Syncing 				|	Number of syncing replication
22.Running Connections 				|	Total number of statement is executing
23.Start Time of Services 			|	Start Time of Services in seconds
24.Total Active Statements 			|	Total number of active statements
25.Total Alerts 				|	Total number of alerts
26.Total CPU Idle Time 				|	Total CPU idle time in minutes
27.Total Caches 				|	Total number of caches
28.Total Column Unloads 			|	Total number of column unloads
29.Total Delta Merge Errors 			|	Total number of table delta merge statistics
30.Total Expensive Statements 			|	Total number of expensive statements
31.Total Network I/O Operations 		|	Total network I/O operations
32.Used Physical Memory 			|	Specifies the used physical memory on the host in GB
		


