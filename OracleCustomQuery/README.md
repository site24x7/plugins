# Custom Oracle DB Monitoring

                                                                                       
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install cx_Oracle module for python
```
  pip install cx_Oracle
```
---



### Plugin Installation  

- Create a directory named "OracleCustomQuery" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/OracleCustomQuery
      
- Download all the files in the "OracleCustomQuery" folder and place it under the "OracleCustomQuery" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleCustomQuery/OracleCustomQuery.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleCustomQuery/OracleCustomQuery.py

- Execute the following command in your server to install Oracle DB: 
  ```
   pip install cx_Oracle
  ```
- Execute the below command with appropriate arguments to check for the valid json output:
```
 python3 OracleCustomQuery.py --hostname <hostname> --port <port no> --sid <sid> --username <username> --password <password> --oracle_home <oracle home> --query <oracle query>
 ```


---

### Configurations

- Provide your Oracle DB configurations in OracleCustomQuery.cfg file.

```
[query_1]
hostname=localhost
port=1521
sid=<SID>
username=<USERNAME>
password=<PASSWORD>
oracle_home=None
query="Oracle Query"
```	

The custom query shall be given in the query section of the config file. The name of the columns of the result will be taken as the metric name and the result will be taken as the metric value.


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.




