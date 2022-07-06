# RabbitMQ Monitoring
RabbitMQ is a message broker tool that routes messages between producers and consumers. It is open-source and functions based on the Advanced Message Queuing Protocol (AMQP).                                                                                              
## Prerequisites

- Download and install the latest version of the Site24x7 Linux Server Monitoring agent on the server where you plan to run the plugin. 
---

### Plugin Installation  

- Create a directory named "rabbitmq" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/rabbitmq
      
- Download all the files in the "rabbitmq" folder and place it under the "rabbitmq" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq/rabbitmq.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/rabbitmq/rabbitmq.cfg


- Execute the below command with appropriate arguments to check for the valid json output:

		python rabbitmq.py --host=<RABBITMQ_HOST> --port=<RABBITMQ_PORT> --username=<RABBITMQ_USERNAME> --password=<RABBITMQ_PASSWORD>


---

### Configurations

-  Provide your RabbitMQ configurations in rabbitmq.cfg file.

		[rabbitmq]
		host = <RABBITMQ_HOST>
		port = <RABBITMQ_PORT>
		username = <RABBITMQ_USERNAME>
		password = <RABBITMQ_PASSWORD>    
		
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


