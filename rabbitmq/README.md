# RabbitMQ Monitoring
RabbitMQ is a message broker tool that routes messages between producers and consumers. It is open-source and functions based on the Advanced Message Queuing Protocol (AMQP).                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Server Monitoring agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) on the server where you plan to run the plugin.

## User Creation

Create a dedicated monitoring user with restricted permissions for RabbitMQ monitoring.

User Tag: monitoring

VHost Permissions: Read-only access for all virtual hosts

1. **Create User with Monitoring Tag:**
   ```bash
   curl -u admin:password -X PUT http://localhost:15672/api/users/monitoring_user \
     -H "content-type:application/json" \
     -d '{"password":"monitoring_password","tags":"monitoring"}'
	    ```
2. **Grant Read-Only Permissions to All VHosts:**
	# For default vhost "/"
	```bash
	curl -u admin:password -X PUT http://localhost:15672/api/permissions/%2F/monitoring_user \
	-H "content-type:application/json" \
	-d '{"configure":"^$","write":"^$","read":".*"}'
	```

	# For custom vhosts (repeat for each vhost)
	```bash
	curl -u admin:password -X PUT http://localhost:15672/api/permissions/vhost_name/monitoring_user \
	-H "content-type:application/json" \
	-d '{"configure":"^$","write":"^$","read":".*"}'
	```

### Automated User Creation:

Download and run the user setup script:

	```bash
	wget https://github.com/site24x7/plugins/raw/refs/heads/master/rabbitmq/prerequisites/prerequisites.sh

	chmod +x prerequisites.sh

	./prerequisites.sh
	```

This script will create a monitoring user and provide read-only permissions to all virtual hosts automatically.

## Plugin Installation  

#### Linux

- Create a directory named `rabbitmq`.

		mkdir rabbitmq
  		cd rabbitmq/
      
- Download all the files and place it under the `rabbitmq` directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq/rabbitmq.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq/rabbitmq.cfg

- Execute the below command with appropriate arguments to check for the valid json output:

		python3 rabbitmq.py --host 'localhost' --port '15672' --username 'guest' --password 'guest' --ssl 'false' --insecure 'true'
		
-  Provide your RabbitMQ configurations in rabbitmq.cfg file.

		[global_configurations]
		use_agent_python=1

		[rabbitmq]
		host = "localhost"
		port = "15675"
		username = "guest"
		password = "guest"
		ssl = "false"
		insecure = "true"


- Move the directory `rabbitmq` under the Site24x7 Linux Agent plugin directory: 

		mv rabbitmq /opt/site24x7/monagent/plugins/

#### Windows

- Create a directory named `rabbitmq`.

- Download the files [rabbitmq.py](https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq/rabbitmq.py), [rabbitmq.cfg](https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq/rabbitmq.cfg) and place it under the `rabbitmq` directory.

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers).
  
- Execute the below command with appropriate arguments in cmd to check for the valid json output:

		python rabbitmq.py --host 'localhost' --port '15672' --username 'guest' --password 'guest' --ssl 'false' --insecure 'true'
  
-  Provide your RabbitMQ configurations in rabbitmq.cfg file.

		[rabbitmq]
		host = "localhost"
		port = "15675"
		username = "guest"
		password = "guest"
		ssl = "false"
		insecure = "true"


- Move the folder `rabbitmq` under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
  
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Supported Metrics

### Summary

Name		        			| 	Description
---         					|   	---
Node Name					|	Unique identifier for the RabbitMQ node in the cluster (e.g., rabbit@nodecheck4)
Node Uptime					|	Time in minutes since this RabbitMQ node was started
Rates Mode					|	Rate calculation mode - basic (default 5s window), detailed (multiple time windows), or none (no rates)
Partitions					|	Number of network partitions detected - should always be 0 for healthy cluster
Total Connections				|	Number of currently active connections on this node
Total Channels					|	Number of currently active AMQP channels on this node
Total Exchanges					|	Total number of exchanges in the entire cluster (shared across all nodes)
Total Consumers					|	Number of active message consumers currently connected to queues on this node
Total Messages					|	Total number of messages in all queues on this node
Total Messages Ready				|	Number of messages ready for delivery to consumers on this node
Total Messages Unacknowledged			|	Number of messages delivered to consumers but not yet acknowledged on this node
Total Messages Rate				|	Messages per second throughput rate for all operations on this node
Total Messages Ready Rate			|	Rate at which messages become ready for delivery per second on this node
Total Messages Unacknowledged Rate		|	Rate at which messages are delivered but remain unacknowledged per second on this node
Connections Created				|	Total number of new client connections established to this node since startup
Connections Closed				|	Total number of client connections terminated on this node since startup
Channels Created				|	Total number of new AMQP channels created on this node since startup
Channels Closed					|	Total number of AMQP channels closed on this node since startup

### Queues

Name		        			| 	Description
---         					|   	---
Queues						|	List of individual queue objects with detailed metrics
Queues Declared					|	Total number of queue declaration operations (create or verify) on this node since startup
Queues Created					|	Total number of new queues actually created on this node since startup
Queues Deleted					|	Total number of queues deleted from this node since startup
Total Queues					|	Total number of queues currently hosted on this specific node

### I/O Operations

Name		        			| 	Description
---         					|   	---
IO Read Avg Time				|	Average time in milliseconds for each RabbitMQ disk read operation - lower is better
IO Read Bytes					|	Total bytes read from disk by RabbitMQ process on this node since startup
IO Read Count					|	Number of disk read operations performed by RabbitMQ process on this node since startup
IO Sync Avg Time				|	Average time in milliseconds for RabbitMQ disk sync operations - can be high due to disk flushing
IO Sync Count					|	Number of forced disk synchronization operations by RabbitMQ process since startup
IO Write Avg Time				|	Average time in milliseconds for each RabbitMQ disk write operation - lower is better
IO Write Bytes					|	Total bytes written to disk by RabbitMQ process on this node since startup
IO Write Count					|	Number of disk write operations performed by RabbitMQ process on this node since startup
IO Seek Count					|	Number of disk seek operations performed by RabbitMQ process since startup
IO Seek Avg Time				|	Average time in milliseconds for each RabbitMQ disk seek operation - indicates disk performance
IO Reopen Count					|	Number of file reopen operations performed by RabbitMQ process since startup

### Storage Operations

Name		        			| 	Description
---         					|   	---
Mnesia RAM Transaction Count			|	Number of RAM-based Mnesia transactions - database operations indicator
Mnesia Disk Transaction Count			|	Number of database transactions written to persistent storage for durability
Message Store Read Count			|	Number of persistent messages read from disk storage
Message Store Write Count			|	Number of persistent messages written to disk storage for durability
Queue Index Read Count				|	Number of queue index read operations for message ordering and retrieval
Queue Index Write Count				|	Number of queue index write operations when messages are added to queues

### Erlang VM

Name		        			| 	Description
---         					|   	---
Total Garbage Collection Count			|	Total number of garbage collection cycles performed by the Erlang virtual machine since node startup
Total Garbage Collection Bytes Reclaimed	|	Total amount of memory in bytes freed by garbage collection processes since node startup
Context Switches				|	Number of times the Erlang scheduler switched execution between different Erlang processes since startup
ErLang Processes Used				|	Currently running Erlang processes - each queue, connection, and channel is an Erlang process
ErLang Processes Total				|	Maximum number of Erlang processes allowed by the Erlang virtual machine
ErLang Processes Remaining			|	Available Erlang process slots calculated as (Total - Used) - shows remaining capacity for new processes
File Descriptor Used				|	Currently open file handles - each connection, queue, and file uses one descriptor
File Descriptor Total				|	Maximum number of file handles this node can open - system limit for file operations
File Descriptor Remaining			|	Available file handles calculated as (Total - Used) - shows remaining capacity for new file operations
Sockets Used					|	Number of active network connections currently established to this node
Run Queue					|	Number of Erlang processes waiting for CPU time - high values indicate CPU pressure

### Performance Rates

Name		        			| 	Description
---         					|   	---
Memory Usage Rate				|	Rate at which memory usage is changing per second in bytes - positive values indicate memory growth
Garbage Collection Rate				|	Number of garbage collection cycles performed per second by the Erlang virtual machine
Context Switch Rate				|	Rate of Erlang process execution switches per second by the VM scheduler
Connections Created Rate			|	Rate of new client connections being established per second
Connections Closed Rate				|	Rate of client connections being terminated per second
IO Read Count Rate				|	Rate of disk read operations per second performed by RabbitMQ process
IO Read Bytes Rate				|	Rate of bytes being read from disk per second by RabbitMQ process
IO Read Avg Time Rate				|	Rate of change in average read time per second - indicates read performance trends
IO Write Count Rate				|	Rate of disk write operations per second performed by RabbitMQ process
IO Write Bytes Rate				|	Rate of bytes being written to disk per second by RabbitMQ process
IO Write Avg Time Rate				|	Rate of change in average write time per second - indicates write performance trends
IO Sync Count Rate				|	Rate of forced disk synchronization operations per second
IO Sync Avg Time Rate				|	Rate of change in average sync time per second - indicates sync performance trends
IO Seek Count Rate				|	Rate of disk seek operations per second performed by RabbitMQ process
IO Seek Avg Time Rate				|	Rate of change in average seek time per second - indicates seek performance trends
IO Reopen Count Rate				|	Rate of file reopen operations per second performed by RabbitMQ process
File Descriptor Usage Rate			|	Rate of change in file descriptor usage per second - file handle management trends
Socket Usage Rate				|	Rate of change in socket usage per second - network connection management trends
GC Bytes Reclaimed Rate				|	Rate of memory reclaimed by garbage collection in bytes per second - memory cleanup efficiency
Mnesia RAM Transaction Rate			|	Rate of database transactions processed in RAM per second
Mnesia Disk Transaction Rate			|	Rate of database transactions written to persistent storage per second
Message Store Read Rate				|	Rate of persistent messages being read from disk storage per second
Message Store Write Rate			|	Rate of persistent messages being written to disk storage per second
Queue Index Read Rate				|	Rate of queue index read operations per second for message ordering and retrieval
Queue Index Write Rate				|	Rate of queue index write operations per second when messages are added to queues

### Queue Metrics

Name		        			| 	Description
---         					|   	---
name						|	Unique name identifier for this specific queue
Vhost						|	Virtual host that contains this queue - allows logical separation of resources
Consumers					|	Number of active consumers currently subscribed to this specific queue
Messages					|	Total number of messages currently in this specific queue
Messages_Ready					|	Number of messages in this queue that are ready for immediate delivery
Messages_Unacknowledged				|	Number of messages from this queue that are delivered but awaiting acknowledgment
Messages_Persistent				|	Number of persistent (durable) messages in this queue that survive restarts
Messages_Rate					|	Rate of message operations (publish/deliver) per second for this specific queue
Messages_Ready_Rate				|	Rate at which messages become ready in this queue per second
Messages_Unacknowledged_Rate			|	Rate at which messages are delivered but remain unacked from this queue per second

## Sample Image

<img width="1640" height="906" alt="image" src="https://github.com/user-attachments/assets/1845456d-5ca6-4a8b-993e-4c3e38946ed7" />

<img width="1657" height="721" alt="image" src="https://github.com/user-attachments/assets/c9357888-bf90-4d4d-bad1-ffcb326f54e1" />


