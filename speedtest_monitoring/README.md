# **SpeedTest-CLI Monitoring**

## SpeedTest-CLI

SpeedTest is a command line interface tool to get the performance of the network from the terminal.

This plugin revolves around displaying the network performance data in the site24x7 console.


## Prerequisites
 - Installation of SpeedTest-CLI
```
pip install speedtest-cli
```

 - Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Plugin Installation

- Create a directory named "speedtest_monitoring" under the Site24x7 Linux Agent plugin directory

```
  Linux    ->   /opt/site24x7/monagent/plugins/speedtest_monitoring
```

 - Download all the files in the "speedtest_monitoring" folder and place it under the "speedtest_monitoring" directory. 

```
  wget https://raw.githubusercontent.com/site24x7/plugins/master/speedtest_monitoring/speedtest_monitoring.py

```

- Execute the below command with appropriate arguments to check for the valid json output:

```
 python3 speedtest_monitoring.py 
```





