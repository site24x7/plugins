# **Process Count Monitoring**

## About Process Count
The plugin revolves around monitoring the process count of a particular user. 





**Best usecase of this plugin**

It can be used in monitoring the nproc limit for oracle user. Since the default limit for process count for oracle is very low, this plugin can be used to get alerts if the process count exceeds a particular threshold.



### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you intend  to run the plugin.



### Plugin Installation

Create a directory named "process_count_monitoring" under the Site24x7 Linux Agent plugin directory:

```
  Linux    ->   /opt/site24x7/monagent/plugins/process_count_monitoring
```
Download all the files in the "process_count_monitoring" folder and place them under the "process_count_monitoring" directory.

Execute the below command with appropriate arguments to check for the valid json output:

```
python3 process_count_monitoring.py --user_name=<USER NAME> 
```

### **Configuration**
##### Provide your Username details in process_count_monitoring.cfg file:

```
[user_1_process_count]
user_name=<USER NAME>
```
#### Supported Metrics
The following metrics are captured by the Kafka Producer monitoring plugin :

- **Process Count**

    The process count of a particular user


### Note
To set thresholds do refer the below help document.

https://www.site24x7.com/help/admin/configuration-profiles/threshold-and-availability/plugin-monitor.html



