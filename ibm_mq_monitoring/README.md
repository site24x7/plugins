# IBM MQ Monitoring

IBM MQ is used by businesses to build scalable architectures.It is largely queue-based and capable of transporting any form of data as messages. It enables the delivery of secure messages across a wide range of computing platforms, online services, communication networks, and applications. With IBM MQ, you can monitor and manage the flow of messages and data.
 
Hence using our plugin, technician can monitor the performance  attributes of IBM MQ Objects like queue manager, channels and queues while also enabling easy alerting, health check would help  reduce risk of downtime within your IBM MQ infrastructure. 

                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install pymqi module for python
```
  pip install pymqi
```
---



### Plugin Installation  

- Create a directory named "ibm_mq_monitoring".
      
- Download all the files in the "ibm_mq_monitoring" folder and place it under the "ibm_mq_monitoring" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the ibm_mq_monitoring.py script.

- Execute the below command with appropriate arguments to check for the valid json output:
	 ```
	 python3 ibm_mq_monitoring.py --queue_manager_name=<name of the queue manager> --channel_name=<channel name> --queue_name=<queue_name> --host=<host name> --port=<port number>  --username=<optional - username> --password=<optional - password> 
	 ```
 - Move the folder "ibm_mq_monitoring" into the  Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/ibm_mq_monitoring
 
 
Since it's a python plugin, to run in windows server please follow the steps in below link, remaining configuration steps are exactly the same. 

  https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers



---

### Configurations

- Provide your IBM MQ configurations in ibm_mq_monitoring.cfg file.
```
    [ibm_mq]
    queue_manager_name=<QUEUE MANAGER NAME>
    channel_name=<CHANNEL NAME>
    queue_name = <QUEUE NAME>
    host=<HOST NAME>
    port = <PORT NUMBER>
    username=<IBM MQ USERNAME>
    password = <IBM MQ PASSWORD>
```	
		
		
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics
The following metrics are captured in the IBM MQ monitoring plugin, which has been categorized under the following entities of IBM WebSphere MQ.
 
- Queue Manager Metrics
- Queue Metrics
- Channel Metrics
 
### **Queue Manager Metrics**
 
- #### Connection_count
     The number of connections to the queue manager.

  
- #### Status
     The status of the queue manager.

 
### **Queue Metrics**

- #### Queue Name
     The name of the queue.


- #### High Queue Depth
     The maximum number of messages on the queue since the queue statistics were last reset.
  

- #### Msg Dequeue Count
     The number of messages removed from the queue since the queue statistics were last reset.

 

- #### Msg Enqueue Count
     The number of messages enqueued, i.e., the number of messages put on the queue since the queue statistics were last reset.
 

- #### Current Queue Depth
     The current number of messages on the queue.
  

- #### Handles Open (Input Count)
     The number of handles that are currently open for input for the queue.
  

- #### Handles Open (Output Count)
     The number of handles that are currently open for output for the queue.
  

- #### Last Msg get Date 
     The date of the last message successfully read from the queue.
  

- #### Last Msg get Time 
     The time of the last message successfully read from the queue.
 

- #### Last Msg put Date 
     The date of the last message successfully put to the queue.
  

- #### Last Msg put Time 
     The time of the last message successfully put to the queue.
  

- #### Oldest Msg Age
     The age of the oldest message on the queue.
  

- #### No. of Uncommitted Msgs
     The number of uncommitted messages on the queue.
 
 
### **Channel Metrics**
 
- #### Channel Name
     The name of the channel name.
 
 
- #### Channel Connection Name
     The number of connections described in the summary.
 
 
- #### Channel Status
     The current status of the client.
 
 
- #### No. of MQI calls
     The number of messages sent or received.

 
- #### Bytes Sent
     The number of bytes sent.

 
- #### Bytes Received
     The number of bytes received.

 
- #### Buffers Sent
     The number of buffers sent.


- #### Buffers Received
     The number of buffers received.
 
 
- #### Channel Substate
     The current action being performed by the channel.


- #### Channel Start Date
     The date when the channel started.
 

- #### Channel Start Time
     The time when the channel started.

