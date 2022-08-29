# MSMQ Monitoring

Microsoft Message Queue (MSMQ) is a message-oriented middleware that helps the applications that run on different servers or processes to communicate. Moreover, the message delivery between apps inside and outside the organization is assured. Any MSMQ outage or performance decline might cause issues like message loss or a breakdown in service communication.

To determine whether the Queues are functioning properly, the MSMQ monitoring plugin continuously monitors the various critical performance metrics of MSMQ. Monitoring Microsoft MSMQ entails providing thorough outage management and preemptive alerts, keeping an eye out for potential issues, and obtaining performance data.

Hence the MSMQ performance monitoring provides comprehensive performance metrics to monitor Microsoft MSMQ servers and helps ensure your messaging services reliably deliver messages.
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


---



### Plugin Installation  

- Create a directory named "msmq_monitoring" under the Site24x7 Windows Agent plugin directory: 

		Windows             ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
      
- Download all the files in the "msmq_monitoring" folder and place it under the "msmq_monitoring" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/msmq_monitoring/msmq_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/msmq_monitoring/msmq_monitoring.cfg



- Execute the below command with appropriate arguments to check for the valid json output:

 ```
.\msmq_monitoring.ps1 -queueName "queuename"
 ```
Since it's a windows plugin, to run in windows server please follow the steps in below link, remaining configuration steps are exactly the same. 

  https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers



---

### Configurations

- Provide your MSMQ configurations in msmq_monitoring.cfg file.
```
    [msmq]
    queueName=<queuename>
```	
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics

The metrics that are captured by the MSMQ plugin are as follows:
 
 - #### Bytes in Journal
   The number of message bytes in the journal of the destination queue.
 
 - #### Bytes in Queue
   The number of message bytes in the destination queue.

 - #### Message Count
   The message count for the specified queue on the host computer.

 - #### Machine Name
   The name of the host machine.

 - #### Max Journal Size
   The maximum journal size.
 
 - #### Max Queue Size
   The maximum queue size.

 - #### Transactional
   The insight on whether the queue is transactional or not.

