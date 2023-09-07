
Plugin for JMX Monitoring
=========================

This plugin can be used to monitor the JMX MBean in the JVM.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 
- Plugin uses JDK to communicate with JMX MBean to get the metrics for monitoring.

### Plugin installation
---
##### Linux 

- Create a directory "jmx".

- Download all the files in "jmx" folder and place it under the "jmx" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jmx/jmx.sh
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jmx/JMXMonitoring.java
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jmx/metrics.txt
	
- Configure the host, port to be monitored, and the java home path in the jmx.sh configuration section.

- The JMX MBean configured by default is java.lang:type=OperatingSystem and is configured in metrics.txt file. Different mbean can be configured to register the metrics for the corresponding mbean.

- Execute the below command to check for the valid json output.  

		sh jmx.sh
		
- Move the directory "jmx" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/jmx

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.



### Metrics Captured
    AvailableProcessors
    CommittedVirtualMemorySize
    FreePhysicalMemorySize
    FreeSwapSpaceSize
    MaxFileDescriptorCount
    OpenFileDescriptorCount
    ProcessCpuLoad
    ProcessCpuTime
    SystemCpuLoad
    SystemLoadAverage
    TotalPhysicalMemorySize
    TotalSwapSpaceSize
    Arch
    Name
    ObjectName
    Version
