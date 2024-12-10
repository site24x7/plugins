# IBM MQ Monitoring

IBM MQ is used by businesses to build scalable architectures.It is largely queue-based and capable of transporting any form of data as messages. It enables the delivery of secure messages across a wide range of computing platforms, online services, communication networks, and applications. With IBM MQ, you can monitor and manage the flow of messages and data.
 
Hence using our plugin, technician can monitor the performance  attributes of IBM MQ Objects like queue manager, channels and queues while also enabling easy alerting, health check would help  reduce risk of downtime within your IBM MQ infrastructure. 

## Quick installation

If you're using Linux servers, use the IBM MQ plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/installer/Site24x7IbmMqPluginInstaller.sh && sudo bash Site24x7IbmMqPluginInstaller.sh
```
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install pymqi module for python
	```
 	pip install pymqi
	```
---



### Plugin Installation  

- Create a directory named `ibm_mq_monitoring`.

	```bash
 	mkdir ibm_mq_monitoring
 	cd ibm_mq_monitoring/
 	```
      
- Download all the files and place it under the `ibm_mq_monitoring` directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.py && sed -i "1s|^.*|#! $(which python3)|" ibm_mq_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the ibm_mq_monitoring.py script.

- Execute the below command with appropriate arguments to check for the valid json output:
	 ```bash
	 python3 ibm_mq_monitoring.py --queue_manager_name "QM1" --channel_name "DEV.APP.SVRCONN" --host "localhost" --port "1414" --username "app" --password "plugin"
	 ```
#### Configurations

- Provide your IBM MQ configurations in ibm_mq_monitoring.cfg file.
	```ini
	[QM1]
	queue_manager_name ="QM1"
	channel_name="DEV.APP.SVRCONN"
	host="localhost"
	port="1414"
	username="app"
	password ="plugin"
	```	
#### Linux

 - Move the folder `ibm_mq_monitoring` into the  Site24x7 Linux Agent plugin directory:

	```bash
	mv ibm_mq_monitoring /opt/site24x7/monagent/plugins/
 	```
 #### Windows
 
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

-  Further, move the folder `ibm_mq_monitoring` into the  Site24x7 Windows Agent plugin directory:

        C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---



## Supported Metrics
The following metrics are captured in the IBM MQ monitoring plugin, which has been categorized under the following entities of IBM WebSphere MQ.
 
- Queue Manager Metrics
- Queue Metrics
- Channel Metrics
- Listeners Metrics
 
### **Queue Manager Metrics**

Name		        	| 	Description
---         			|   	---
Connection_count		|	The number of connections to the queue manager.
Status				|	The status of the queue manager.

 
### **Queue Metrics**
Name		        	| 	Description
---         			|   	---
Queue Name			|	The name of the queue.
High Queue Depth		|	The maximum number of messages on the queue since the queue statistics were last reset.
Msg Dequeue Count		|	The number of messages removed from the queue since the queue statistics were last reset.
Msg Enqueue Count		|	The number of messages enqueued, i.e., the number of messages put on the queue since the queue statistics were last reset.
Current Queue Depth		|	The current number of messages on the queue.
Handles Open (Input Count)	|	The number of handles that are currently open for input for the queue.
Handles Open (Output Count)	|	The number of handles that are currently open for output for the queue.
Oldest Msg Age			|	The age of the oldest message on the queue.
No. of Uncommitted Msgs		|	The number of uncommitted messages on the queue.
 
 
### **Channel Metrics**
Name		        	| 	Description
---         			|   	---
Channel Name			|	The name of the channel.
Channel Status			|	The current status of the client. Refer [here](https://github.com/site24x7/plugins/blob/master/ibm_mq_monitoring/README.md#values-for-channel-statuses).
No. of MQI calls		|	The number of messages sent or received.
Bytes Sent			|	The number of bytes sent.
Bytes Received			|	The number of bytes received.
Buffers Sent			|	The number of buffers sent.
Buffers Received		|	The number of buffers received.
Channel Substate		|	The current action being performed by the channel. Refer [here](https://github.com/site24x7/plugins/blob/TharunRajTR-patch-9/ibm_mq_monitoring/README.md#values-for-channel-sub-state).


#### Values for Channel Statuses 
 No		        	| 	Description
---         			|   	---
0				|	Channel Inactive
1				|	Channel Binding
2				|	Channel Starting
3				|	Channel Running
4				|	Channel Stopping
5				|	Channel Retrying
6				|	Channel Stopped
7				|	Channel Requesting
8				|	Channel Paused
9				|	Channel Disconnected
10				|	Channel Initializing
11				|	Channel Switching

#### Values for Channel Sub State
 No		        	| 	Description
---         			|   	---
0				|	Undefined State
100				|	End of batch processing
200				|	Network send
300				|	Network receive
400				|	Serialized on queue manager access
500				|	Resynching with partner
600				|	Heartbeating with partner
700				|	Running security exit
800				|	Running receive exit
900				|	Running send exit
1000				|	Running message exit
1100				|	Running retry exit
1200				|	Running channel auto-definition exit
1250				|	Network connect
1300				|	SSL Handshaking
1400				|	Name server request
1500				|	Performing MQPUT
1600				|	Performing MQGET
1700				|	Executing IBM MQ API call
1800				|	Compressing or decompressing data

### **Listeners Metrics**

 Name		        	| 	Description
---         			|   	---
Listeners Name			|	The name of the listener.
port				|	The port number used by the listener.
Backlog				|	Backlog of the listener.
State				|	The Current state of listener.
