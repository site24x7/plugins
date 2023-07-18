# MySQL CUSTOM QUERY MONITORING

=================================================================

- This plugin is used to keep an eye on critical MySQL queries that impact the availability and performance of your business application. DBA, DevOps team can add the critical query for monitoring in their Database.. The monitor's dashboard is structured to give you an overview of the important metrics of the monitor.

  Using this plugin, the DBA, and DevOps teams can get information about the availability and the performance of the given database query.The plugin will execute the given query and display the result as performance data like column name as metric and assign the column value to the metric. However, for each data collection of the plugin, it will accept only the first row of the given MySQL table. Hence we recommend using the LIMIT clause in the query for better performance.

---

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

- Create a directory "mysql_custom_query".
- Copy and execute the below command under the "mysql_custom_query" folder to download the pymysql module.
	
		wget https://github.com/site24x7/plugins/raw/master/mysql_monitoring/pymysql/pymysql.zip && unzip pymysql.zip && rm pymysql.zip
		
- Download  the below files in "mysql_custom_query" folder and place it under the "mysql_custom_query" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_custom_query/mysql_custom_query.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_custom_query/mysql_custom_query.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		  python mysql_custom_query.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --db=<db> --query=<custom_query>

- After above command with parameters gives expected output, please configure the relevant parameters in the mysql_custom_query.cfg file.

		  [mysql_custom_query]
		  host = localhost
		  port = 3306
		  username = "root"
		  password = 
		  db = sys
		  query = "select * from metrics LIMIT 1"
  #### Note:
  -  If your custom query returns multiple rows based on specific criteria, you have the flexibility to utilize aggregation functions according to your needs, enabling manipulation of the retrieved rows.
  - Reference - https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html

- Applog is supported for MySQL Monitoring. To enable applog for this plugin, configure logs_enabled=true and configure log_type_name and log_file_path as need.

- Place the "mysql_custom_query" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/mysql_custom_query
---
		
#### Windows

- Move the directory "mysql_custom_query" under Site24x7 Windows Agent plugin directory :

		Windows             ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


---
_The pymysql source can be found [here](https://github.com/PyMySQL/PyMySQL/tree/main)._

_Zoho Corporation has made this into one single [zip file](https://github.com/site24x7/plugins/tree/master/mysql_custom_query/pymysql/pymysql.zip) and is licensed under the same [license](https://github.com/PyMySQL/PyMySQL/blob/main/LICENSE) which can be found [here](https://github.com/site24x7/plugins/tree/master/mysql_custom_query/pymysql/LICENSE.txt)._



