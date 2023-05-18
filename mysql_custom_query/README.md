# MySQL CUSTOM QUERY MONITORING

=================================================================

- This plugin is used to keep an eye on critical MySQL queries that impact the availability and performance of your business application. DBA, DevOps team can add the critical query for monitoring in their Database.. The monitor's dashboard is structured to give you an overview of the important metrics of the monitor.

  Using this plugin, the DBA, and DevOps teams can get information about the availability and the performance of the given database query.The plugin will execute the given query and display the result as performance data like column name as metric and assign the column value to the metric. However, for each data collection of the plugin, it will accept only the first row of the given MySQL table. Hence we recommend using the LIMIT clause in the query for better performance.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Intsall Pymysql module with following command

		pip install PyMySQL
		
- Pymysql(v1.0.3) works only for python with version>=3.7 	

- Select on queries permission is required to execute the queries mentioned above.
		GRANT SELECT ON mysql.* TO "username"@"hostname" IDENTIFIED BY "password";
		FLUSH PRIVILEGES;

---

### Plugin Installation 

- Create a directory "mysql_custom_query".

- Download the below files and place it under the "mysql_custom_query" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_custom_query/mysql_custom_query.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_custom_query/mysql_custom_query.cfg

- Update the below configurations in mysql_custom_query.cfg file:

		[mysql_custom_query]
		host = localhost
		port = 3306
		username = "root"
		password = 
		db = sys
		query = "select * from metrics LIMIT 1"
		
- This plugin will monitor only the first row of the result of the query.So, use LIMIT clause in the query as below to return only one row from the result.

		query = "select * from metrics LIMIT 1"

- Execute the below command with appropriate arguments to check for the valid json output.  

		python mysql_custom_query.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --db=<db> --query=<custom_query>
		
#### Linux 

- Move the directory "mysql_custom_query" under Site24x7 Linux Agent plugin directory :

		Linux             ->   /opt/site24x7/monagent/plugins/
		
#### Windows

- Move the directory "mysql_custom_query" under Site24x7 Windows Agent plugin directory :

		Windows             ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


---


