# MSMQ Monitoring
                                                                                              
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

