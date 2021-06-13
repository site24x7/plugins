Plugin for Squid Proxy Monitoring 
==============================================

Squid Proxy is a fully-featured HTTP/1.0 proxy which is almost a fully-featured HTTP/1.1 proxy. Squid offers a rich access control, authorization and logging environment to develop web proxy and content serving applications. Squid offers a rich set of traffic optimization options, most of which are enabled by default for simpler installation and high performance.

Follow the below steps to configure the Kong plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Apache Kong service instances.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---
##### Linux 

- Create a folder "squid" under Site24x7 Linux Agent plugin directory : 

      Linux            ->   /opt/site24x7/monagent/plugins/squid

##### Windows 

- Create a folder "squid" under Site24x7 Windows Agent plugin directory : 

      Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\squid
      
---

- Download all the files in "squid" folder and place it under the "squid" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/squid/squid.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/squid/squid.cfg
	
- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python squid.py --host_name=localhost --port=3128


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations
---
	[display_name]
	host_name=“<your_host_name>”
	port=“3128”

### Metrics Captured
---
	proxysql_uptime -> metric calculates the percentage of memory used by the given Broker in your ActiveMQ Setup. [percent]

	sqlite3_memory_bytes -> metric calculates the percentage of storage used by the given Broker in your ActiveMQ Setup. [percent]

	active_transactions -> metric calculates the percentage of temp used by the given Broker in your ActiveMQ Setup. [percent]

	client_connections_aborted -> metric calculate the average amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [millisecond]

	client_connections_connected -> metric calculate the minimum amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [millisecond]

	client_connections_created -> metric calculate the maximum amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [millisecond]

	server_connections_aborted -> metric calculate the number of messages that remained dequeued in the queue of the given Broker of your ActiveMQ Setup. [message]
	
	server_connections_connected -> metric calculate the number of messages that remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [message]

	server_connections_created -> metric counts and records the number of consumers connected in the queue of the given Broker of your ActiveMQ Setup. [count]

	client_connections_non_idle -> metric counts and records the number of producers connected in the queue of the given Broker of your ActiveMQ Setup. [count]

	backend_query_time_nsec -> metric counts and records the number of messages that have been dispatched in the queue of the given Broker of your ActiveMQ Setup. [message]

	mysql_backend_buffers_bytes -> metric calculate the number of messages that remained in the queue of the given Broker of your ActiveMQ Setup. [message]

	mysql_frontend_buffers_bytes -> metric calculate the percentage of memory currently used in the queue of the given Broker of your ActiveMQ Setup. [percent]

	mysql_session_internal_bytes -> metric calculate the number of messages that have been expired in the queue of the given Broker of your ActiveMQ Setup. [message]

	mysql_thread_workers -> metric calculate the number of messages that have been in flight in the queue of the given Broker of your ActiveMQ Setup. [message]		

	mysql_monitor_workers -> metric calculates the percentage of temp used by the given Broker in your ActiveMQ Setup. [percent]

	client_connections_aborted -> metric calculate the average amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [millisecond]

	client_connections_connected -> metric calculate the minimum amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [millisecond]

	client_connections_created -> metric calculate the maximum amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [millisecond]

	server_connections_aborted -> metric calculate the number of messages that remained dequeued in the queue of the given Broker of your ActiveMQ Setup. [message]
	
	server_connections_connected -> metric calculate the number of messages that remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [message]

	server_connections_created -> metric counts and records the number of consumers connected in the queue of the given Broker of your ActiveMQ Setup. [count]

	client_connections_non_idle -> metric counts and records the number of producers connected in the queue of the given Broker of your ActiveMQ Setup. [count]

	backend_query_time_nsec -> metric counts and records the number of messages that have been dispatched in the queue of the given Broker of your ActiveMQ Setup. [message]

	mysql_backend_buffers_bytes -> metric calculate the number of messages that remained in the queue of the given Broker of your ActiveMQ Setup. [message]

	mysql_frontend_buffers_bytes -> metric calculate the percentage of memory currently used in the queue of the given Broker of your ActiveMQ Setup. [percent]

	mysql_session_internal_bytes -> metric calculate the number of messages that have been expired in the queue of the given Broker of your ActiveMQ Setup. [message]

	mysql_thread_workers -> metric calculate the number of messages that have been in flight in the queue of the given Broker of your ActiveMQ Setup. [message]		
