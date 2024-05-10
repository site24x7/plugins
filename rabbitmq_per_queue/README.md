Plugin for monitoring individual queues in RabbitMQ
===================================================

This plugin monitors the individual rabbitmq queues.

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 
- Python version 3 or higher.


## Plugin installation

#### Linux 

- Create a directory `rabbitmq_per_queue`.

- Download all the files in `rabbitmq_per_queue` directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq_per_queue/rabbitmq_per_queue.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq_per_queue/rabbitmq_per_queue.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the rabbitmq_per_queue.py script.
	
- Configure the keys to be monitored, as mentioned below in rabbitmq_per_queue.cfg

		[localhost]
		hostname="localhost"
		port=15672
		username="guest"
		password="guest"
		vhost="/"
		queue_name="Test Queue"
		plugin_version=1
		heartbeat=True

- Execute the below command with appropriate arguments to check for the valid json output.  

		python rabbitmq_per_queue.py --hostname "localhost" --port "15672" --username "guest" --password "guest" --vhost "/" --queue_name "Test Queue" --realm "None"
	
- Move the directory `rabbitmq_per_queue` under Site24x7 Linux Agent plugin directory.
	```
	mv rabbitmq_per_queue /opt/site24x7/monagent/plugins/
	```

#### Windows

- Create a directory named `rabbitmq_per_queue`.

- Download the files [rabbitmq_per_queue.py](https://github.com/site24x7/plugins/blob/master/rabbitmq_per_queue/rabbitmq_per_queue.py), [rabbitmq_per_queue.cfg](https://github.com/site24x7/plugins/blob/master/rabbitmq_per_queue/rabbitmq_per_queue.cfg) and place it under the `rabbitmq_per_queue` directory.

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers).
  
- Execute the below command with appropriate arguments in cmd to check for the valid json output:

		python rabbitmq_per_queue.py --hostname "localhost" --port "15672" --username "guest" --password "guest" --vhost "/" --queue_name "Test Queue" --realm "None"
  
-  Provide your RabbitMQ queue configurations in rabbitmq_per_queue.cfg file.

		[localhost]
		hostname="localhost"
		port=15672
		username="guest"
		password="guest"
		vhost="/"
		queue_name="Test Queue"
		plugin_version=1
		heartbeat=True

- Move the folder `rabbitmq_per_queue` under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
  
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 -> Plugins -> Plugin Integrations.

### Metrics Captured
---
- consumers
- messages
- messages.persistent
- messages.rate
- messages.ready
- messages.ready.rate
- messages.unack
- messages.unack.rate 			
