# Oracle DB Custom Query monitoring

                                                                                       
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install cx_Oracle module for python
```
  pip install cx_Oracle
```
---



### Plugin Installation  

- Create a directory named "oracle_custom_query".
      
- Download all the files in the "oracle_custom_query" folder and place it under the "oracle_custom_query" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_custom_query/oracle_custom_query.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_custom_query/oracle_custom_query.py

- Execute the following command in your server to install Oracle DB: 

		pip install cx_Oracle

- Execute the below command with appropriate arguments to check for the valid json output:

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

- Move the directory named "oracle_custom_query" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---	

The custom query shall be given in the query section of the config file. The name of the columns of the result will be taken as the metric name and the result will be taken as the metric value.


_The cx_Oracle source can be found [here](https://github.com/oracle/python-cx_Oracle)._

_Zoho Corporation has made this into one single [executable](https://github.com/site24x7/plugins/tree/master/oracle_custom_query/cx_Oracle/cx_Oracle_linux) and is licensed under the same [license](https://github.com/oracle/python-cx_Oracle/blob/main/LICENSE.txt) which can be found [here](https://github.com/site24x7/plugins/blob/master/oracle_custom_query/cx_Oracle/LICENSE.txt)._
