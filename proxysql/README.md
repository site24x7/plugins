Plugin for Monitoring ProxySQL
==============================================

ProxySQL is a high performance, high availability, protocol aware proxy for MySQL and forks (like Percona Server and MariaDB). ProxySQL runs as a daemon watched by a monitoring process.

Follow the below steps to configure the ProxySQL plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of ProxySQL.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "mysql.connector" python library. This module is MySQL driver written in Python which does not depend on MySQL C client libraries and implements the DB API  

		pip install mysql-connector-python
		

### Plugin installation
---
##### Linux 

- Create a folder "proxysql".

- Download all the files in "proxysql" folder and place it under the "proxysql" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/proxysql/proxysql.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/proxysql/proxysql.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the proxysql.py script.
  
- Configure the keys to be monitored, as mentioned below in proxysql.cfg

		[display_name]
		host_name=“<your_host_name>”
		port=“1099”
		user="<proxysql_user_name>”
		password="<proxysql_user_password>”

- Execute the below command with appropriate arguments to check for the valid json output.  

		python proxysql.py --host_name=localhost --port=6032 --user=<proxysql_user_name> --password=<proxysql_user_password>

- Move the folder "proxysql" under Site24x7 Linux Agent plugin directory : 

		Linux            ->   /opt/site24x7/monagent/plugins/
      
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Captured
---
	active_transactions -> metric calculates the number of client connections currently processing a transaction. [transaction]

	sqlite3_memory_bytes -> metric calculates the memory used by the embedded SQLite. [byte]

	client_connections_aborted -> metric calculate the number of client failed or improperly closed connections per second. [connection]

	client_connections_connected -> metric calculate the number of client connections that are currently connected. [connection]

	client_connections_created -> metric calculate the number of client connections created per second. [connection]

	server_connections_aborted -> metric calculate the number of backend failed or improperly closed connections per second. [connection]
	
	server_connections_connected -> metric calculate the number of backend connections that are currently connected. [connection]

	server_connections_created -> metric calculate the number of backend connections created per second. [connection]

	client_connections_non_idle -> metric calculate the number of client connections that are currently handled by the main worker threads. [connection]

	backend_query_time_nsec -> metric calculate the time spent making network calls to communicate with the backends. [message]

	mysql_backend_buffers_bytes -> metric calculate the memory use of buffers related to backend connections. [byte]

	mysql_frontend_buffers_bytes -> metric calculate the memory use of buffers related to frontend connections (read/write buffers and other queues). [byte]

	mysql_thread_workers -> metric calculate the number of MySQL Thread workers i.e. 'mysql-threads'. [worker]		

	mysql_monitor_workers -> metric calculates the number of monitor threads. [worker]

	connpool_get_conn_success -> metric calculate the number of requests per second where a connection was already available in the connection pool. [connection]

	connpool_get_conn_immediate -> metric calculate the number of connections per second that a MySQL Thread obtained from its own local connection pool cache. [connection]

	questions -> metric calculate the number of client requests / statements executed per second. [question]
	
	slow_queries -> metric calculate the number of queries per second with an execution time greater than 'mysql-long_query_time' milliseconds. [query]

	connpool_memory_bytes -> metric calculate the memory used by the connection pool to store connections metadata. [byte]

	stmt_client_active_total -> metric calculate the number of prepared statements that are in use by clients. [unit]

	stmt_client_active_unique -> metric calculate the number of unique prepared statements currently in use by clients. [unit]

	stmt_server_active_total -> metric calculate the number of prepared statements currently available across all backend connections. [unit]

	stmt_server_active_total -> metric calculate the number of prepared statements currently available across all backend connections. [unit]
	
	stmt_server_active_unique -> metric calculate the number of unique prepared statements currently available across all backend connections. [unit]

	stmt_cached -> metric calculate the number of global prepared statements for which proxysql has metadata. [unit]

	query_processor_time_nsec -> metric calculate the time spent inside the query processor determining the action to take with the query. [percent]
