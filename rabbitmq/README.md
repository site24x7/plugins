# RabbitMQ Monitoring
RabbitMQ is a message broker tool that routes messages between producers and consumers. It is open-source and functions based on the Advanced Message Queuing Protocol (AMQP).                                                                                              
## Prerequisites

- Download and install the latest version of the Site24x7 Linux Server Monitoring agent on the server where you plan to run the plugin.
- Python version 3 or higher.

## Plugin Installation  

#### Linux

- Create a directory named `rabbitmq`.

		mkdir rabbitmq
  		cd rabbitmq/
      
- Download all the files and place it under the `rabbitmq` directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq/rabbitmq.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq/rabbitmq.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the rabbitmq.py script.

- Execute the below command with appropriate arguments to check for the valid json output:

		python rabbitmq.py --host "localhost" --port "15672" --username "guest" --password "guest"
		
-  Provide your RabbitMQ configurations in rabbitmq.cfg file.

		[rabbitmq]
		host = "localhost"
		port = "15672"
		username = "guest"
		password = "guest"  

- Move the directory `rabbitmq` under the Site24x7 Linux Agent plugin directory: 

		mv rabbitmq /opt/site24x7/monagent/plugins/    
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

