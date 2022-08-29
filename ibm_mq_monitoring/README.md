# IBM MQ Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install pymqi module for python
```
  pip install pymqi
```
---



### Plugin Installation  

- Create a directory named "ibm_mq_monitoring" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/ibm_mq_monitoring
      
- Download all the files in the "ibm_mq_monitoring" folder and place it under the "ibm_mq_monitoring" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.cfg

- Execute the following command in your server to install pymqi: 

		pip install pymqi

- Execute the below command with appropriate arguments to check for the valid json output:
```
 python3 ibm_mq_monitoring.py --queue_manager_name=<name of the queue manager> --channel_name=<channel name> --queue_name=<queue_name> --host=<host name> --port=<port number>  --username=<optional - username> --password=<optional - password> 
 ```
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

##Supported Metrics
The following metrics are captured in the IBM MQ monitoring plugin, which has been categorized under the following entities of IBM WebSphere MQ.
 
- Queue Manager Metrics
- Queue Metrics
- Channel Metrics
 
### **Queue Manager Metrics**
 
#### Connection_count
 The number of connections to the queue manager.
  <p>&nbsp;</p>
  
#### Status
 The status of the queue manager.
 <p>&nbsp;</p>
 
### **Queue Metrics**

#### Queue Name
 The name of the queue.
<p>&nbsp;</p>

#### High Queue Depth
The maximum number of messages on the queue since the queue statistics were last reset.
  <p>&nbsp;</p>

#### Msg Dequeue Count
The number of messages removed from the queue since the queue statistics were last reset.
 <p>&nbsp;</p>
 

#### Msg Enqueue Count
The number of messages enqueued, i.e., the number of messages put on the queue since the queue statistics were last reset.
  <p>&nbsp;</p>

#### Current Queue Depth
The current number of messages on the queue.
  <p>&nbsp;</p>

#### Handles Open (Input Count)
The number of handles that are currently open for input for the queue.
  <p>&nbsp;</p>

#### Handles Open (Output Count)
 The number of handles that are currently open for output for the queue.
  <p>&nbsp;</p>

#### Last Msg get Date 
   The date of the last message successfully read from the queue.
  <p>&nbsp;</p>

#### Last Msg get Time 
The time of the last message successfully read from the queue.
  <p>&nbsp;</p>

#### Last Msg put Date 
The date of the last message successfully put to the queue.
  <p>&nbsp;</p>

#### Last Msg put Time 
The time of the last message successfully put to the queue.
  <p>&nbsp;</p>

#### Oldest Msg Age
 The age of the oldest message on the queue.
  <p>&nbsp;</p>

#### No. of Uncommitted Msgs
The number of uncommitted messages on the queue.
 <p>&nbsp;</p>
 
### **Channel Metrics**
 
#### Channel Name
 The name of the channel name.
 <p>&nbsp;</p>
 
#### Channel Connection Name
 The number of connections described in the summary.
 <p>&nbsp;</p>
 
#### Channel Status
 The current status of the client.
 <p>&nbsp;</p>
 
#### No. of MQI calls
The number of messages sent or received.
<p>&nbsp;</p>
 
#### Bytes Sent
The number of bytes sent.
<p>&nbsp;</p>
 
#### Bytes Received
The number of bytes received.
<p>&nbsp;</p>
 
#### Buffers Sent
The number of buffers sent.
<p>&nbsp;</p>

#### Buffers Received
The number of buffers received.
 <p>&nbsp;</p>
 
#### Channel Substate
The current action being performed by the channel.
<p>&nbsp;</p>

#### Channel Start Date
The date when the channel started.
<p>&nbsp;</p> 

#### Channel Start Time
The time when the channel started.

