# Custom Postgres DB Monitoring

                                                                                       
## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- The following packages are required to install psycopg2 python module. Please install them using.
  
  - Debian:

		apt install libpq-dev python3-dev gcc
 
  - Redhat:

		yum install postgresql-libs postgresql-devel python3-devel gcc

- Install psycopg2 module for python
	```
  	pip install psycopg2
	```

## Plugin Installation  

- Create a directory named `postgres_custom_query`.

		mkdir postgres_custom_query
  		cd postgres_custom_query/
      
- Download all the files and place it under the `postgres_custom_query` directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres_custom_query/postgres_custom_query.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres_custom_query/postgres_custom_query.cfg

- Execute the following command in your server to install psycopg2: 

		pip install psycopg2

- Execute the below command with appropriate arguments to check for the valid json output:

		python3 postgres_custom_query.py --db_name "db_name" --port "port no" --username "username" --password "password" --query "query"

- Provide your Postgres DB configurations in postgres_custom_query.cfg file.

		[custom_metric_1]
		db_name='postgres'
		username=None
		password=None
		hostname='localhost'
		port=5432
		query="SELECT buffers_checkpoint, buffers_backend, maxwritten_clean, checkpoints_req, checkpoints_timed, buffers_alloc FROM pg_stat_bgwriter;"
  #### Note:
  -  If your custom query returns multiple rows based on specific criteria, you have the flexibility to utilize aggregation functions according to your needs, enabling manipulation of the retrieved rows.
  -  Reference - https://www.postgresql.org/docs/9.5/functions-aggregate.html
  
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the postgres_custom_query.py script.
  
- Move the directory `postgres_custom_query` under the Site24x7 Linux Agent plugin directory: 

		mv postgres_custom_query /opt/site24x7/monagent/plugins/
#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Move the folder `postgres_custom_query` under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

The custom query shall be given in the query section of the config file. The name of the columns of the result will be taken as the metric name and the result will be taken as the metric value.

Example : 

Query to be given :
<img src="https://i.imgur.com/cmN8qo4.png"/>

Metrics captured :
<img src="https://i.imgur.com/onxWKO6.png"/>

