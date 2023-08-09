ActiveMQ Queue Monitoring 
==============================================

Apache ActiveMQ enables easy processing of messages from various applications and communicates them across your infrastructure. Install and configure the ActiveMQ plugin to get a detailed view of how your systems and services are performing, all in a single, intuitive dashboard.

Follow the below steps to configure the ActiveMQ plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Apache ActiveMQ instances.

### Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "JPype" python library. This module is used to execute the jmx query and get data. Execute the below command to install python JPype modeule in your server. 

- Python version must be 3.7 or above.  

		pip install JPype1
		
- JMX connection should be enabled in the Apache ActiveMQ installation folder. 
  - To enable it with password protection follow the [ActiveMQ Documentation](https://activemq.apache.org/jmx)
  - To enable it without passsword protection follow the below steps: 
  	- Open conf/activemq.xml inside the installation folder of Apache ActiveMQ and change the following attributes

	```
		<managementContext>
    		     <managementContext createConnector="true" connectorPort="1099"/>
		</managementContext>
	```
	
	
	
	
- Restart the activemq service after making the above changes.

### Plugin installation
---



- Download all the files in "activemq" folder and place it under the "activemq" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/activemq/activemq.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/activemq/activemq.cfg
	

- Execute the below command with appropriate arguments to check for the valid json output.  

		python activemq.py –-host_name=localhost -–port=1099 -–broker_name=<your_broker_name> --destination_name=<your_queue_name>

#### Configurations
-  Edit the activemq.cfg file with appropriate arguments
	```
	[display_name]
	host_name=“<your_host_name>”
	port=“1099”
	broker_name=“<your_broker_name>”
	destination_name=“<your_destination_name>”
	```
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the activemq.py script.

- Place the "activemq" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/activemq

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "activemq" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\activemq



The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured

- **memory_percent_usage** 
    
    Percentage of memory used by the given Broker in your ActiveMQ Setup.

- **storage_percent_usage** 

    Storage used by the given Broker in your ActiveMQ Setup.

- **temp_percent_usage** 
    
    Temp storage used by the given Broker in your ActiveMQ Setup.

- **avg_enqueue_time**

    The average amount of time the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup.

- **min_enqueue_time** 

    Minimum amount of time the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup.

- **max_enqueue_time** 

    Maximum amount of time, the messages remained enqueued in the queue of the given Broker of your ActiveMQ Setup.

- **dequeue_count**

    Number of messages that remained dequeued in the queue of the given Broker of your ActiveMQ Setup.

- **enqueue_count** 

    Number of messages that remained enqueued in the queue of the given Broker of your ActiveMQ Setup.

- **consumer_count** 

    Number of consumers connected in the queue of the given Broker of your ActiveMQ Setup.

- **producer_count** 

    Number of producers connected in the queue of the given Broker of your ActiveMQ Setup.

- **dispatch_count** 

    Number of messages that have been dispatched in the queue of the given Broker of your ActiveMQ Setup.

- **queue_size**
 
    Number of messages that remained in the queue of the given Broker of your ActiveMQ Setup.

- **memory_percent** 

    Percentage of memory currently used in the queue of the given Broker of your ActiveMQ Setup.

- **expired_count** 

    Number of messages that have been expired in the queue of the given Broker of your ActiveMQ Setup.

- **in_flight_count** 

    Number of messages that have been in flight in the queue of the given Broker of your ActiveMQ Setup.
