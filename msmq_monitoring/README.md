# MSMQ Monitoring

Microsoft Message Queue (MSMQ) is a message-oriented middleware that helps the applications that run on different servers or processes to communicate. Moreover, the message delivery between apps inside and outside the organization is assured. Any MSMQ outage or performance decline might cause issues like message loss or a breakdown in service communication.

Monitoring Microsoft MSMQ entails providing thorough outage management and preemptive alerts, keeping an eye out for potential issues, and obtaining performance data.

                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


## Plugin Installation  

- Create a directory named `msmq_monitoring`.
      
- Download the files [msmq_monitoring.ps1](https://github.com/site24x7/plugins/blob/master/msmq_monitoring/msmq_monitoring.ps1), [msmq_monitoring.cfg](https://github.com/site24x7/plugins/blob/master/msmq_monitoring/msmq_monitoring.cfg)  and place them under the `msmq_monitoring` directory.

- Execute the below command with appropriate arguments to check for the valid JSON output:

	 ```
	.\msmq_monitoring.ps1 -queueName "*"
	 ```
#### Configurations

- If you want to monitor all the queues present in the server the plugin will do it automatically.
- For filtering the queues to monitor, Eg:
	- If you only need to monitor the queues with "otp" on their queue name Provide "otp" in msmq_monitoring.cfg file.
 
	```
	[msmq]
	queueName="otp"
	```
	- Now all the queues with "otp" in their name will be monitored.
- Move the folder into the  Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
		


	
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics

The metrics that are captured by the MSMQ plugin are:

 Name		        	| 	Description
---         			|   	---
Bytes in Journal		|	The number of message bytes in the journal of the destination queue.
Bytes in Queue			|	The number of message bytes in the destination queue.
Bytes In Queue [average]	|	Average of the Bytes in Queue of all queues.
Message Count			|	The message count for the specified queue on the host computer.
Message Count [average]		|	The Average of all the message count of the queues.
Max Journal Size		|	The maximum journal size.
Max Queue Size			|	The maximum queue size.
Transactional			|	The insight on whether the queue is transactional or not.

