ActiveMQ Topics Monitoring 
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
	
Restart the instance after making the above changes.

### Plugin installation
---
##### Linux 

- Create a folder "activemq" under Site24x7 Linux Agent plugin directory : 

      Linux            ->   /opt/site24x7/monagent/plugins/activemq_topics

##### Windows 

- Create a folder "activemq" under Site24x7 Windows Agent plugin directory : 

      Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\activemq_topics
      
---

- Download all the files in "activemq" folder and place it under the "activemq" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/activemq/activemq_topics/activemq_topics.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/activemq/activemq_topics/activemq_topics.cfg
	
- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.  

  ```
  python3 activemq_topics.py --hostname <hostname> --port <port> --broker_name <broker_name> --topic_name <topic_name>
  ```

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations
---
```
[active mq_topics]
hostname=hostname
port=port
broker_name=broker_name
topic_name=topic_name
logs_enabled="False"
log_type_name=None
log_file_path==None
```
### Metrics Captured

- **AlwaysRetroactive** 
  
    This metric specifies whether messages are always retroactive, meaning they can be consumed by a consumer that connects after the message was originally produced.

- **AverageBlockedTime** 

    The average time a producer was blocked waiting to send a message due to flow control.

- **AverageEnqueueTime**
  
    The average time it takes to enqueue a message in the broker.

- **AverageMessageSize** 
    
    The average size of messages stored in the broker.

- **BlockedProducerWarningInterval** 
    
    The interval at which the broker logs a warning message if producers are blocked due to flow control.

- **BlockedSends** 
    
    The number of times a producer was blocked waiting to send a message due to flow control.

- **ConsumerCount** 

    The number of consumers currently subscribed to a queue or topic.

- **DLQ** 

    The number of messages that have been moved to the dead-letter queue (DLQ) due to message expiration, exceeded maximum redelivery attempts, or other reasons.

- **DequeueCount**
 
    The total number of messages that have been dequeued from a queue or topic.

- **DispatchCount** 
    
    The total number of messages that have been dispatched to consumers.

- **DuplicateFromStoreCount** 

    The number of times a message was sent again from the store due to a failure in the original delivery.

- **EnqueueCount** 

    The total number of messages that have been enqueued in the broker.

- **ExpiredCount** 
    
    The number of messages that have expired and have been removed from the broker.

- **ForwardCount** 
    
    The number of messages that have been forwarded to another destination.

- **InFlightCount** 
    
    The number of messages currently in flight, meaning they have been dispatched to a consumer but have not yet been acknowledged.

- **MaxAuditDepth** 
 
    The maximum depth of the audit log.

- **MaxEnqueueTime** 

    The maximum time it takes to enqueue a message in the broker.

- **MaxMessageSize** 

    The maximum size of messages that can be stored in the broker.

- **MaxPageSize** 

    The maximum number of messages that can be paged in a single request.

- **MaxProducersToAudit** 

    The maximum number of producers to audit.

- **MemoryLimit** 

    The maximum amount of memory that can be used by the broker.

- **MemoryPercentUsage** 

    The percentage of memory currently used by the broker.

- **MemoryUsageByteCount** 

    The total number of bytes currently used by the broker's memory.

- **MemoryUsagePortion** 

    The percentage of total memory usage that is used by the broker.

- **MinEnqueueTime** 
    
    The minimum time it takes to enqueue a message in the broker.

- **MinMessageSize** 

    The minimum size of messages stored in the broker.

- **PrioritizedMessages** 

    The number of prioritized messages.

- **ProducerCount** 

    The number of producers currently sending messages to a queue or topic.

- **ProducerFlowControl** 
  
    Whether producer flow control is enabled or not.

- **QueueSize** 

    The current size of a queue.

- **SendDuplicateFromStoreToDLQ**
    
    Whether messages that are sent again from the store due to a failure in the original delivery are moved to the DLQ.

- **StoreMessageSize** 

    The total size of messages stored in the broker.

- **TempUsageLimit** 

    The maximum amount of temporary storage that can be used by the broker.

- **TempUsagePercentUsage** 
    
    The percentage of temporary storage currently used by the broker.

- **TotalBlockedTime** 

    The total time that producers have been blocked waiting to send messages due to flow control.
    
- **UseCache** 
  
    A boolean value indicating whether caching is enabled for a queue/topic.




