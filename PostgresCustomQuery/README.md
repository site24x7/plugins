# Custom Postgres DB Monitoring

                                                                                       
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install psycopg2 module for python
```
  pip install psycopg2
```
---



### Plugin Installation  

- Create a directory named "PostgresCustomQuery" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/PostgresCustomQuery
      
- Download all the files in the "PostgresCustomQuery" folder and place it under the "PostgresCustomQuery" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/PostgresCustomQuery/PostgresCustomQuery.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/PostgresCustomQuery/PostgresCustomQuery.py

- Execute the following command in your server to install psycopg2: 
  ```
   pip install psycopg2
  ```
- Execute the below command with appropriate arguments to check for the valid json output:
```
 python3 PostgresCustomQuery.py --db_name <db_name> --port <port no> --username <username> --password <password> --query <db2 query>
 ```



---

### Configurations

- Provide your Postgres DB configurations in PostgresCustomQuery.cfg file.

```
    [custom_metric_1]
    db_name='postgres'
    username=None
    password=None
    hostname='localhost'
    port=5432
    query="SELECT buffers_checkpoint, buffers_backend, maxwritten_clean, checkpoints_req, checkpoints_timed, buffers_alloc FROM pg_stat_bgwriter;"
```	

The custom query shall be given in the query section of the config file. The name of the columns of the result will be taken as the metric name and the result will be taken as the metric value.

Example : 

Query to be given :
<img src="https://i.imgur.com/cmN8qo4.png"/>

Metrics captured :
<img src="https://i.imgur.com/onxWKO6.png"/>
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


