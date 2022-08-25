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

