# MSSQL CUSTOM QUERY MONITORING

=================================================================

- This plugin is used to keep an eye on critical SQL queries that impact the availability and performance of your business application. DBA, DevOps team can add the critical query for monitoring in their Database.. The monitor's dashboard is structured to give you an overview of the important metrics of the monitor.

  Using this plugin, the DBA, and DevOps teams can get information about the availability and the performance of the given database query.The plugin will execute the given query and display the result as performance data like column name as metric and assign the column value to the metric. However, for each data collection of the plugin, it will accept only the first row of the given SQL table. Hence we recommend using the TOP clause in the query for better performance.

### Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

---

### Plugin Installation 

- Create a folder named "mssql_custom_query" under the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\mssql_custom_query
		
- Download all the files in "mssql_custom_query" folder and place it under the "mssql_custom_query" directory

		https://raw.githubusercontent.com/site24x7/plugins/master/mssql_custom_query/mssql_custom_query.ps1
		https://raw.githubusercontent.com/site24x7/plugins/master/mssql_custom_query/mssql_custom_query.cfg

- Configurations
  Update the below configurations in mssql_custom_query.cfg file:


		[mssql_custom_query]
		SQLServer = <server_name> 
		SQLDBName = <dbname>
		query = "select TOP 1 * from sys.assemblies"
		sqlusername = <sql_username>
		sqlpassword  = <sql_password>
		
- This plugin will monitor only the first row of the result of the query.So, use TOP clause in the query as below to return only one row from the result.

		query = "select TOP 1 * from sys.assemblies"


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---



