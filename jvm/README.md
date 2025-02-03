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

| **Metric Name**                      | **Description**                                               |
|--------------------------------------|---------------------------------------------------------------|
| Classes Unloaded                     | The total number of classes unloaded by the JVM.             |
| Classes Loaded                        | The total number of classes loaded into memory.              |
| VmName                                | The name of the JVM implementation.                          |
| Uptime                                | The total uptime of the JVM in milliseconds.                 |
| Runtime Free Memory                   | The amount of free memory available in the JVM heap (bytes). |
| Runtime Total Memory                  | The total amount of memory allocated for the JVM (bytes).    |
| CPU Usage                             | The percentage of CPU being used by the JVM process.         |
| Peak Threads                          | The highest number of live threads recorded since startup.   |
| Daemon Threads                        | The number of daemon threads currently running.              |
| Live Threads                          | The current number of live threads in the JVM.               |
| Total Started Threads                 | The total number of threads started since JVM startup.       |
| CPU Time                              | The total CPU time used by the JVM (nanoseconds).            |
| User Time                             | The time spent by user-mode threads in the JVM (nanoseconds).|
| Compilation Time                      | The total time spent in JIT compilation (milliseconds).      |
| Heap Committed                        | The amount of memory committed for the JVM heap (bytes).     |
| Heap Max                              | The maximum memory that can be allocated for the heap (bytes). |
| Heap Used                             | The memory currently used in the JVM heap (bytes).          |
| Non Heap Committed                    | The committed non-heap memory used by JVM (bytes).          |
| Non Heap Max                          | The maximum non-heap memory allowed (bytes).                |
| Non Heap Used                         | The amount of memory currently used in non-heap (bytes).    |
| Compressed Class Space Committed      | The committed memory for compressed class space (bytes).    |
| Compressed Class Space Max            | The maximum memory allocated for compressed class space (bytes). |
| Compressed Class Space Used           | The memory used by compressed class space (bytes).          |
| Metaspace Committed                   | The committed memory used by Metaspace (bytes).             |
| Metaspace Max                         | The maximum Metaspace memory allocated (bytes).             |
| Metaspace Used                        | The memory used in the JVM Metaspace (bytes).               |
| CodeHeap 'non-nmethods' Committed     | The committed memory for non-method CodeHeap (bytes).       |
| CodeHeap 'non-nmethods' Max           | The maximum memory allocated for non-method CodeHeap (bytes). |
| CodeHeap 'non-nmethods' Used          | The memory used in non-method CodeHeap (bytes).             |
| CodeHeap 'profiled nmethods' Committed| The committed memory for profiled nmethods CodeHeap (bytes). |
| CodeHeap 'profiled nmethods' Max      | The maximum memory allocated for profiled nmethods CodeHeap (bytes). |
| CodeHeap 'profiled nmethods' Used     | The memory used in profiled nmethods CodeHeap (bytes).      |
| CodeHeap 'non-profiled nmethods' Committed | The committed memory for non-profiled nmethods CodeHeap (bytes). |
| G1 Eden Space Committed               | The committed memory for the G1 Eden space (bytes).         |
| G1 Eden Space Max                     | The maximum memory allocated for G1 Eden space (bytes).     |
| G1 Eden Space Used                    | The memory used in G1 Eden space (bytes).                   |
| G1 Old Gen Committed                  | The committed memory for G1 Old Generation (bytes).         |
| G1 Old Gen Max                        | The maximum memory allocated for G1 Old Generation (bytes). |
| G1 Old Gen Used                       | The memory used in G1 Old Generation (bytes).               |
| G1 Survivor Space Committed           | The committed memory for G1 Survivor space (bytes).         |
| G1 Survivor Space Max                 | The maximum memory allocated for G1 Survivor space (bytes). |
| G1 Survivor Space Used                | The memory used in G1 Survivor space (bytes).               |


![image](https://github.com/user-attachments/assets/7eb65352-5281-4f78-a95b-16426180dfa2)
