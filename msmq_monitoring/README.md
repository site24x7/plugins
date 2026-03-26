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
 
	```
	[global_configurations]
	redirect_output="1"
	
	[Queues]
	queueName="*"
	```
- Move the folder into the  Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
		


	
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## MSMQ Monitoring Metrics

| **Name** | **Description** |
|-----------|-----------------|
| **Bytes In Queue In Average** | The average number of message bytes in the queue across all monitored queues. |
| **Message Count In Average** | The average number of messages in the queue across all monitored queues. |
| **Total No Of Queues** | The total number of queues discovered and monitored by the plugin. |

### Queues

| **Name** | **Description** |
|-----------|-----------------|
| **Bytes In Queue** | The number of message bytes currently stored in the destination queue. |
| **Bytes In Journal** | The number of message bytes in the journal of the destination queue. |
| **Message Count** | The total number of messages in the specified queue. |
| **Journal Message Count** | The total number of messages in the journal of the specified queue. |
| **Message Journal Size** | The maximum size (in MB) of the journal associated with the queue. |
| **Message Queue Size** | The maximum size (in MB) allocated for the queue. |
| **Is Transactional** | Indicates whether the queue is transactional (`Yes`) or non-transactional (`No`). |

### Service

| **Name** | **Description** |
|-----------|-----------------|
| **Incoming Messages Per Sec** | The rate (messages per second) of incoming messages being processed by MSMQ. |
| **Outgoing Messages Per Sec** | The rate (messages per second) of outgoing messages being processed by MSMQ. |
| **MSMQ Incoming Messages** | The total number of incoming messages handled by MSMQ since startup. |
| **MSMQ Outgoing Messages** | The total number of outgoing messages handled by MSMQ since startup. |
| **Sessions** | The number of active MSMQ sessions currently established. |
| **IP Sessions** | The number of MSMQ sessions that are using IP-based connections. |
| **Total Bytes All Queues** | The total number of message bytes across all monitored queues. |
| **Total Messages All Queues** | The total number of messages across all monitored queues. |

### Outgoing

| **Name** | **Description** |
|-----------|-----------------|
| **Total Outgoing Queues** | The total number of outgoing queues with messages pending delivery to remote servers. |
| **Total Outgoing Messages** | The total number of messages across all outgoing queues waiting for delivery. |
| **Total Outgoing Bytes** | The total number of bytes across all outgoing queues waiting for delivery. |
| **Total Unacknowledged Messages** | The total number of messages sent to remote servers but not yet acknowledged. |
| **Total Unprocessed Messages** | The total number of messages in outgoing queues that have not yet been processed for delivery. |


## Sample Image

<img width="1637" height="689" alt="image" src="https://github.com/user-attachments/assets/da02198b-eba1-4b4c-97ad-095dd4b7ae58" />

