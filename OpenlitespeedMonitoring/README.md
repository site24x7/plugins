# Openlitespeed Monitoring

                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


---



### Plugin Installation  

- Create a directory named "OpenlitespeedMonitoring" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/OpenlitespeedMonitoring
      
- Download all the files in the "OpenlitespeedMonitoring" folder and place it under the "OpenlitespeedMonitoring" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OpenlitespeedMonitoring/OpenlitespeedMonitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OpenlitespeedMonitoring/OpenlitespeedMonitoring.cfg



- Execute the below command with appropriate arguments to check for the valid json output:
```
 python3 OpenlitespeedMonitoring.py --metric_path=<swapping directory path> --virtual_host=<virtual host name>
 ```




---

### Configurations

- Provide your OpenlitespeedMonitoring configurations in OpenlitespeedMonitoring.cfg file.
```
[ols_monitoring]
metric_path='/tmp/lshttpd/'
virtual_host='_AdminVHost'
logs_enabled='False'
log_type_name=None
log_file_path=None

```	

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics
The following metrics are captured in the OpenlitespeedMonitoring Plugin

- **Request Processing**

    The number of requests being processed

- **Request Per Sec**

    The number of requests per second

- **Total Requests**

    Total number of requests

- **Pub Cache Hits Per Sec**

    Number of public cache hits per sec


- **Total Pub Cache Hits**

    Total number of public cache hits


- **Private Cache Hits Per Sec**

    Total number of private cache hits per sec

- **Total Private Cache Hits**

    Total number of private cache hits

- **Static Hits Per Sec**

    Total number of static hits per sec

- **Total Static Hits**

    Total number of static hits



