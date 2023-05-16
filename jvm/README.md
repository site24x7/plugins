
Plugin for JVM Monitoring
=========================

This plugin can be used to monitor the JVM through JMX Monitoring.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 
- Plugin uses JDK to communicate with JMX MBean to get the metrics for monitoring.

### Plugin installation
---
##### Linux 

- Create a directory "jvm".

- Download all the files in "jvm" folder and place it under the "jvm" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jvm/jvm.sh
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jvm/JVMMonitoring.java
        
- Configure the java home path in the jvm.sh and the host, port of the application which is using Java path mentioned in jvm.sh file.

- Execute the below command to check for the valid json output.

		sh jvm.sh
		
- Move the directory "jvm" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Captured
    VmName
    Uptime
    Runtime Free Memory in bytes
    Runtime Total Memory in bytes
    CPU Usage of the JVM

    Classes Loaded
    Classes Unloaded
    Compilation Time in ms

    Peak threads
    Daemon threads
    Live threads
    Total Started Threads
    CPU Time in ms
    User Time in ms

    GC Collections Count
    GC Time Spent in ms
