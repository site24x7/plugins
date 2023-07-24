Plugin for monitoring individual queues in RabbitMQ
===================================================

This plugin monitors the individual rabbitmq queues

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "urllib" python library. 


### Plugin installation
---
##### Linux 

- Create a directory "rabbitmq_per_queue".

- Download all the files in "rabbitmq_per_queue" folder and place it under the "rabbitmq_per_queue" directory

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

		python rabbitmq_per_queue.py --hostname="localhost" --port=15672 --username="guest" --password="guest" --vhost="/" --queue_name="Test Queue" --realm=None --plugin_version="1" --heartbeat="True"
	
- Move the directory "rabbitmq_per_queue" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Captured
---
	consumers
	messages
	messages.persistent
	messages.rate
	messages.ready
	messages.ready.rate
	messages.unack
	messages.unack.rate 			
