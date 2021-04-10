Plugin for ActiveMQ Monitoring 
==============================================

Apache ActiveMQ enables easy processing of messages from various applications and communicates them across your infrastructure. Install and configure the ActiveMQ plugin to get a detailed view of how your systems and services are performing, all in a single, intuitive dashboard.

Follow the below steps to configure the ActiveMQ plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Apache ActiveMQ instances.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "JPype" python library. This module is used to execute the jmx query and get data. Execute the below command to install python JPype modeule in your server.  

		pip install JPype1
		
- JMX connection should be enabled in the Apache ActiveMQ installation folder. To enable the JMX connection follow the below steps: Open conf/activemq.xml inside the installation folder of Apache ActiveMQ and change the following attributes

		<managementContext>
    		     <managementContext createConnector="true" connectorPort="1099"/>
		</managementContext>


### Plugin installation
---
##### Linux 

- Create a folder "activemq" under Site24x7 Linux Agent plugin directory : 

      Linux            ->   /<site24x7_installation_directory>/site24x7/monagent/plugins/activemq

##### Windows 

- Create a folder "activemq" under Site24x7 Windows Agent plugin directory : 

      Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\activemq
      
---

- Download all the files in "activemq" folder and place it under the "activemq" directory

	  wget https://raw.githubusercontent.com/mrkksparrow/plugins/master/activemq/activemq.py
	  wget https://raw.githubusercontent.com/mrkksparrow/plugins/master/activemq/activemq.cfg
	
- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python activemq.py –-host_name=localhost -–port=1099 -–broker_name=<your_broker_name> --destination_name=<your_destination_name>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations
---
	[display_name]
	host_name=“<your_host_name>”
	port=“1099”
	broker_name=“<your_broker_name>”
	destination_name=“<your_destination_name>”

### Metrics Captured
---
	memory_percent_usage -> metric calculates the percentage of memory used by the given Broker in your ActiveMQ Setup. [percent]

	storage_percent_usage -> metric calculates the percentage of storage used by the given Broker in your ActiveMQ Setup. [percent]

	temp_percent_usage -> metric calculates the percentage of temp used by the given Broker in your ActiveMQ Setup. [percent]

	avg_enqueue_time -> metric calculate the average amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [millisecond]

	min_enqueue_time -> metric calculate the minimum amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [millisecond]

	max_enqueue_time -> metric calculate the maximum amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [millisecond]

	dequeue_count -> metric calculate the number of messages that remained dequeued in the queue of the given Broker of your ActiveMQ Setup. [message]
	
	enqueue_count -> metric calculate the number of messages that remained enqueued in the queue of the given Broker of your ActiveMQ Setup. [message]

	consumer_count -> metric counts and records the number of consumers connected in the queue of the given Broker of your ActiveMQ Setup. [count]

	producer_count -> metric counts and records the number of producers connected in the queue of the given Broker of your ActiveMQ Setup. [count]

	dispatch_count -> metric counts and records the number of messages that have been dispatched in the queue of the given Broker of your ActiveMQ Setup. [message]

	queue_size -> metric calculate the number of messages that remained in the queue of the given Broker of your ActiveMQ Setup. [message]

	memory_percent -> metric calculate the percentage of memory currently used in the queue of the given Broker of your ActiveMQ Setup. [percent]

	expired_count -> metric calculate the number of messages that have been expired in the queue of the given Broker of your ActiveMQ Setup. [message]

	in_flight_count -> metric calculate the number of messages that have been in flight in the queue of the given Broker of your ActiveMQ Setup. [message]		
