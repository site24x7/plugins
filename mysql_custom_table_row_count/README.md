# MySQL CUSTOM TABLE ROW COUNT 

=================================================================

### MySQL Table Row Count Monitoring

- This plugin is used to monitor the row count for the given query. Hence use the count clause in the query.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Intsall Pymysql module with following command

		pip install PyMySQL
		
- Pymysql(v1.0.3) works only for python with version>=3.7 	

- For the given user and password in the configuration, you need to Grant privileges by executing the below query.
  
		GRANT SELECT ON mysql.* TO "username"@"hostname" IDENTIFIED BY "password";
		FLUSH PRIVILEGES;

---

### Plugin Installation 

- Create a directory "mysql_custom_table_row_count".
		
- Download all the files in "mysql_custom_table_row_count" folder and place it under the "mysql_custom_table_row_count" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_custom_table_row_count/mysql_custom_table_row_count.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_custom_table_row_count/mysql_custom_table_row_count.cfg

- Update the below configurations in mysql_custom_table_row_count.cfg file:

		[mysql_custom_table_row_count]
		host = localhost
		port = 3306
		username = "root"
		password = 
		db = sys
		query = "select count(*) from metrics"
		
- Execute the below command with appropriate arguments to check for the valid json output. 

		python mysql_custom_table_row_count.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --db=<db> --query=<custom_query>
		
#### Linux 

- Move the directory "mysql_custom_table_row_count" under Site24x7 Linux Agent plugin directory :

		Linux             ->   /opt/site24x7/monagent/plugins/
		
#### Windows

- Move the directory "mysql_custom_table_row_count" under Site24x7 Windows Agent plugin directory :

		Windows             ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


---

