# Oracle DB Custom Query monitoring

                                                                                       
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.7 or higher version has to be installed.
- **oracledb** python module has to be installed using the below command.
  
  		pip3 install oracledb

---



### Plugin Installation  

- Create a directory named "oracle_custom_query".

- Download the below files in the "oracle_custom_query" folder and place them under the "oracle_custom_query" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_custom_query/oracle_custom_query.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_custom_query/oracle_custom_query.py


- Execute the below command with appropriate arguments to check for the valid JSON output:

		python3 oracle_custom_query.py --hostname <hostname> --port <port no> --sid <sid> --username <username> --password <password> --oracle_home <oracle home> --query <oracle query>
		
- Provide your Oracle DB configurations in oracle_custom_query.cfg file.

		[query_1]
		hostname=localhost
		port=1521
		sid=<SID>
		username=<USERNAME>
		password=<PASSWORD>
		oracle_home=None
		query="Oracle Query"
  #### Note:
  -  If your custom query returns multiple rows based on specific criteria, you have the flexibility to utilize aggregation functions according to your needs, enabling manipulation of the retrieved rows.
  -  Reference - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Aggregate-Functions.html#GUID-62BE676B-AF18-4E63-BD14-25206FEA0848

- Move the directory named "oracle_custom_query" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/
		
The agent will automatically execute the plugin within five minutes and the user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---	

The custom query shall be given in the query section of the config file. The name of the columns of the result will be taken as the metric name and the result will be taken as the metric value.

