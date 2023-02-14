# Custom IBM DB2 Monitoring

                                                                                       
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install ibm_db module for python
```
  pip install ibm_db
```
---



### Plugin Installation  

- Create a directory named "ibmdb2_custom_query" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/ibmdb2_custom_query
      
- Download all the files in the "ibmdb2_custom_query" folder and place it under the "ibmdb2_custom_query" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibmdb2_custom_query/ibmdb2_custom_query.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibmdb2_custom_query/ibmdb2_custom_query.cfg

- Execute the following command in your server to install ibm_db: 
  ```
   pip install ibm_db
  ```
- Execute the below command with appropriate arguments to check for the valid json output:
```
 python3 ibmdb2_custom_query.py --host <hostname> --port <port no> --username <username> --password <password> --sample_db <db name> --query <db2 query>
 ```



---

### Configurations

- Provide your IBM DB2 configurations in ibmdb2_custom_query.cfg file.

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


