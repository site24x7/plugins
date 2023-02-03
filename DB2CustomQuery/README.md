# Custom IBM DB2 Monitoring

                                                                                       
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install ibm_db module for python
```
  pip install ibm_db
```
---



### Plugin Installation  

- Create a directory named "DB2CustomQuery" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/DB2CustomQuery
      
- Download all the files in the "DB2CustomQuery" folder and place it under the "DB2CustomQuery" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/DB2CustomQuery/DB2CustomQuery.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/DB2CustomQuery/DB2CustomQuery.py

- Execute the following command in your server to install ibm_db: 
  ```
   pip install ibm_db
  ```
- Execute the below command with appropriate arguments to check for the valid json output:
```
 python3 DB2CustomQuery.py --host <hostname> --port <port no> --username <username> --password <password> --sample_db <db name> --query <db2 query>
 ```



---

### Configurations

- Provide your IBM MQ configurations in DB2CustomQuery.cfg file.

```
  [ibm_db_2]
  host 		= "<hostname>"
  port 		= "<port>"
  username	= "<username>"
  password 	= "<password>"
  sample_db	= "<sample_db>"
  query         = "<DB2 Query>
```	

The custom query shall be given in the query section of the config file. The name of the columns of the result will be taken as the metric name and the result will be taken as the metric value.

Example : 

Query to be given :
<img src="https://i.imgur.com/petJTnD.png"/>


Metrics captured :
<img src="https://i.imgur.com/gQ9nPzS.png"/>

		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.



