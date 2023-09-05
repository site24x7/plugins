
Plugin for JVM Memory Monitoring
================================

This plugin can be used to monitor the JVM memory through JMX Monitoring.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 
- Plugin uses JDK to communicate with JMX MBean to get the metrics for monitoring.

### Plugin installation
---
##### Linux 

- Create a directory "jvmmemory".

- Download all the files in "jvmmemory" folder and place it under the "jvmmemory" directory

	    wget https://raw.githubusercontent.com/site24x7/plugins/master/jvmmemory/jvmmemory.sh
	    wget https://raw.githubusercontent.com/site24x7/plugins/master/jvmmemory/JVMMemoryMonitoring.java
        
- Configure the java home path in the jvm.sh and the host, port of the application which is using Java path mentioned in jvmmemory.sh file.

- Execute the below command to check for the valid json output.  

		sh jvmmemory.sh
		
- Move the directory "jvmmemory" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/jvmmemory

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
    Heap Committed in bytes
    Heap Max in bytes
    Heap Used in bytes

    Non Heap Committed in bytes
    Non Heap Max in bytes
    Non Heap Used in bytes

    Individual Memory Pool's Committed in bytes
    Individual Memory Pool's Max in bytes
    Individual Memory Pool's Used in bytes
