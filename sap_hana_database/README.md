# SAP HANA DATABASE MONITORING


### What is SAP HANA ?

SAP HANA (High-performance ANalytic Appliance) is a column-oriented database that stores data in its memory instead of on a disk. This unique architecture enables SAP HANA to process and query massive amounts of data with near-zero latency, which is significantly faster than other database management systems and allows for advanced real-time analytics.
	
Monitor the availability and performance of your SAP HANA database with SAP HANA plugin integration.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Install the hdbcli module with the following command

		pip install hdbcli
		
- hdbcli driver supports for python 2.7, python 3.4 and above.
		
-  Ensure the SAP HANA user profile that will be added in the sap_hana_database.cfg file has been provided public and monitoring role access:

		GRANT ROLE PUBLIC to user username
		GRANT ROLE MONITORING to user username

### Plugin Installation

- Create a directory named "sap_hana_database".
		
		mkdir sap_hana_database
  		cd sap_hana_database/
  
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
		
### Supported Metrics

| Name                               | Description |
|------------------------------------|-------------|
| **Active Threads**                 | The number of threads actively processing tasks. |
| **Active Transactions**            | The number of currently active transactions. |
| **Idle Connections**               | The number of idle database connections. |
| **Inactive Transactions**          | The number of transactions currently inactive. |
| **Queuing Connections**            | The number of connections waiting in the queue. |
| **Running Connections**            | The number of connections actively running. |
| **Total Alerts**                   | The total number of alerts generated. |
| **Total CPU Idle Time**            | The idle time of the CPU in percentage. |
| **Total Network I/O Operations**   | The total network input/output operations performed. |
| **Total Active Statements**        | The number of active SQL statements currently running. |
| **Start Time of Services**         | The time when services were last started. |

---

### Backup and Replication

| Name                  | Description |
|-----------------------|-------------|
| **Backup Catalogs**   | The total number of backup catalogs available. |
| **Replication Errors**| The number of replication errors encountered. |
| **Replication Syncing**| Indicates if replication is in sync. |

---

### Disk

| Name                               | Description |
|------------------------------------|-------------|
| **CATALOG_BACKUP Disk Free Size**  | Free space available for catalog backup. |
| **DATA Disk Free Size**            | Free space available on the data disk. |
| **DATA_BACKUP Disk Free Size**     | Free space available for data backup. |
| **LOG Disk Free Size**             | Free space available on the log disk. |
| **LOG_BACKUP Disk Free Size**      | Free space available for log backup. |
| **TRACE Disk Free Size**           | Free space available on the trace disk. |

---

### Memory

| Name                                        | Description |
|---------------------------------------------|-------------|
| **Free Physical Memory**                    | The amount of free physical memory available. |
| **Index Server Memory Pool Heap Used Size** | Memory used by the index server heap pool. |
| **Index Server Memory Pool Shared Used Size**| Shared memory used by the index server pool. |
| **Index Server Memory Pool Used Size**      | Total memory used by the index server pool. |
| **Name Server Memory Pool Heap Used Size**  | Memory used by the name server heap pool. |
| **Name Server Memory Pool Shared Used Size**| Shared memory used by the name server pool. |
| **Name Server Memory Pool Used Size**       | Total memory used by the name server pool. |
| **Used Physical Memory**                    | The amount of physical memory currently in use. |

---

### Operations and Performance

| Name                               | Description |
|------------------------------------|-------------|
| **Total Active Statements**        | The number of active SQL statements currently running. |
| **Total Expensive Statements**     | The number of expensive SQL statements encountered. |
| **Total Caches**                   | The total number of caches available. |
| **Total Column Unloads**           | The number of columns unloaded from memory. |
| **Total Delta Merge Errors**       | The number of errors during delta merges. |
| **Total Network I/O Operations**   | The total number of network I/O operations performed. |
| **Total Alerts**                   | The total number of alerts generated. |

---

### Services

| Name            | Description |
|-----------------|-------------|
| **Daemon**      | Background service managing overall system operations. |
| **Preprocessor**| Service handling pre-compilation and query preprocessing. |
| **Webdispatcher**| Service managing web-based request routing. |
| **Compileserver**| Service compiling SQL queries and managing code generation. |
| **Nameserver**  | Service managing distributed system nodes and catalog data. |
| **Diserver**    | Data integration service for handling ETL and related tasks. |

---

### Workload

| Name                               | Description |
|------------------------------------|-------------|
| **Commit Rate (per min)**          | The rate of commits performed per minute. |
| **Compilation Rate (per min)**     | The rate of SQL compilations performed per minute. |
| **Execution Rate (per min)**       | The rate of query executions performed per minute. |
| **Memory Usage Rate (GB/min)**     | The rate of memory usage growth per minute. |
| **Transaction Rate (per min)**     | The rate of transactions processed per minute. |
