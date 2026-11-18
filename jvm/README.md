Plugin for JVM Monitoring
=========================

This plugin can be used to monitor the JVM through JMX Monitoring.

### Prerequisites

- Download and install the latest version of the Site24x7 agent in the server where you plan to run the plugin. 

-  Install the jmxquery module for python.
	```
	pip install jmxquery
	```

### Plugin installation
---

- Create a directory "jvm".

- Download all the files in "jvm" folder and place it under the "jvm" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jvm/jvm.cfg
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jvm/jvm.py
        
-  Execute the below command with appropriate arguments to check for a valid json output:

    ```
     python3 jvm.py --jvm_host "localhost" --jvm_jmx_port "7199"
    ```
		
#### Configurations


-  Provide your JVM configurations in the jvm.cfg file.
  
```
[jvm]
jvm_host="localhost"
jvm_jmx_port=7199

```

#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the jvm.py script.

- Place the "jvm" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

-  Further move the folder "jvm" into the  Site24x7 Windows Agent plugin directory:
    ```
        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
    ```

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
| PS Eden Space Committed               | The committed memory for Parallel Scavenge Eden space (bytes). |
| PS Eden Space Max                     | The maximum memory allocated for PS Eden space (bytes).     |
| PS Eden Space Used                    | The memory used in PS Eden space (bytes).                   |
| PS Old Gen Committed                  | The committed memory for Parallel Scavenge Old Generation (bytes). |
| PS Old Gen Max                        | The maximum memory allocated for PS Old Generation (bytes). |
| PS Old Gen Used                       | The memory used in PS Old Generation (bytes).               |
| PS Survivor Space Committed           | The committed memory for PS Survivor space (bytes).         |
| PS Survivor Space Max                 | The maximum memory allocated for PS Survivor space (bytes). |
| PS Survivor Space Used                | The memory used in PS Survivor space (bytes).               |
| Par Eden Space Committed              | The committed memory for ParNew Eden space (bytes).         |
| Par Eden Space Max                    | The maximum memory allocated for ParNew Eden space (bytes). |
| Par Eden Space Used                   | The memory used in ParNew Eden space (bytes).               |
| Par Survivor Space Committed          | The committed memory for ParNew Survivor space (bytes).     |
| Par Survivor Space Max                | The maximum memory allocated for ParNew Survivor space (bytes). |
| Par Survivor Space Used               | The memory used in ParNew Survivor space (bytes).           |
| CMS Old Gen Committed                 | The committed memory for CMS Old Generation (bytes).        |
| CMS Old Gen Max                       | The maximum memory allocated for CMS Old Generation (bytes).|
| CMS Old Gen Used                      | The memory used in CMS Old Generation (bytes).              |
| Copy Collections Count                | The number of collections performed by Copy garbage collector. |
| Copy Time Spent                       | The total time spent in Copy garbage collection (milliseconds). |
| MarkSweepCompact Collections Count    | The number of collections performed by MarkSweepCompact GC. |
| MarkSweepCompact Time Spent           | The total time spent in MarkSweepCompact GC (milliseconds). |
| ParNew Collections Count              | The number of collections performed by ParNew garbage collector. |
| ParNew Time Spent                     | The total time spent in ParNew garbage collection (milliseconds). |
| ConcurrentMarkSweep Collections Count | The number of collections performed by CMS garbage collector. |
| ConcurrentMarkSweep Time Spent        | The total time spent in CMS garbage collection (milliseconds). |
| PSScavenge Collections Count          | The number of collections performed by Parallel Scavenge GC. |
| PSScavenge Time Spent                 | The total time spent in Parallel Scavenge GC (milliseconds). |
| PSMarkSweep Collections Count         | The number of collections performed by PSMarkSweep GC.      |
| PSMarkSweep Time Spent                | The total time spent in PSMarkSweep GC (milliseconds).      |
| G1 Young Generation Collections Count | The number of collections performed by G1 Young Generation GC. |
| G1 Young Generation Time Spent        | The total time spent in G1 Young Generation GC (milliseconds). |
| G1 Old Generation Collections Count   | The number of collections performed by G1 Old Generation GC. |
| G1 Old Generation Time Spent          | The total time spent in G1 Old Generation GC (milliseconds). |

### Sample Image

<img width="1640" height="966" alt="image" src="https://github.com/user-attachments/assets/7222c319-5773-491b-b290-0cdcab58ec75" />

