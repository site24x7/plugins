# Mule Monitoring

Install and configure the Mule monitoring plugin to monitor the performance, availability, and health of your Mule Runtime environment. Track JVM heap memory, garbage collection, thread activity, CPU usage, and memory pool utilization to ensure optimal performance of your Mule applications.

---

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python version 3 or higher.
- Python package required: `jmxquery`

Install it using the following command:

```bash
pip3 install jmxquery
```

- JMX remote access must be enabled on the Mule Runtime. Add the following JVM arguments to your Mule startup configuration:

```
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9999
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
```

---

## Installation

### Plugin Installation

- Create a directory named `mule`:

```bash
mkdir mule
cd mule/
```

- Download all the files [mule.cfg](https://github.com/site24x7/plugins/blob/master/mule/mule.cfg), [mule.py](https://github.com/site24x7/plugins/blob/master/mule/mule.py) and place them under the `mule` directory:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/mule/mule.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/mule/mule.cfg
```

- Execute the below command with appropriate arguments to check for valid JSON output:

```bash
python3 mule.py --hostname "localhost" --port "9999"
```

### Configurations

Provide your Mule Runtime configurations in the `mule.cfg` file.

```bash
[mule]
hostname = "localhost"
port = "9999"
```

### Move the plugin under the Site24x7 agent directory

#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mule.py script.

- Move the `mule` directory under the Site24x7 Linux Agent plugin directory:

```bash
mv mule /opt/site24x7/monagent/plugins/
```

#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Move the folder `mule` under Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---

## Metrics Captured

### Summary

| Metric Name                    | Description                                                                                              |
|--------------------------------|----------------------------------------------------------------------------------------------------------|
| PID                            | Process ID of the Mule Runtime JVM process, displayed as a string (e.g., "Process 12345").               |
| Heap Used Percent              | Percentage of JVM heap memory currently in use by the Mule Runtime.                                      |
| Heap Free Memory               | Amount of free JVM heap memory available to the Mule Runtime (MB).                                       |
| File Descriptor Usage Percent  | Percentage of the maximum allowed file descriptors currently in use by the Mule Runtime process.         |
| Thread Count                   | Number of active threads in the Mule Runtime JVM.                                                        |
| CPU Process Load               | CPU load consumed by the Mule Runtime JVM process as a percentage.                                       |
| GC Collections Total           | Total number of garbage collection events across all GC generations in the Mule Runtime JVM.             |
| GC Time Total                  | Total time spent on garbage collection across all GC generations in the Mule Runtime JVM (min).          |
| Open Files                     | Number of file descriptors currently open by the Mule Runtime JVM process.                               |
| Classes Loaded                 | Number of Java classes currently loaded in the Mule Runtime JVM.                                         |
| Loaded Class Count             | Number of Java classes currently loaded in the Mule Runtime JVM class loader.                            |
| Total Loaded Class Count       | Total number of Java classes loaded since the Mule Runtime JVM started.                                  |
| Unloaded Class Count           | Number of Java classes unloaded from the Mule Runtime JVM since startup.                                 |
| Total Compilation Time         | Total time spent by the JIT compiler compiling Java code in the Mule Runtime JVM (min).                  |
| Direct Buffer Count            | Number of direct NIO byte buffers allocated by the Mule Runtime JVM for I/O operations.                  |
| Direct Buffer Memory Used      | Total memory used by direct NIO byte buffers in the Mule Runtime JVM (MB).                               |
| Mapped Buffer Count            | Number of memory-mapped NIO byte buffers allocated by the Mule Runtime JVM.                              |
| Mapped Buffer Memory Used      | Total memory used by memory-mapped NIO byte buffers in the Mule Runtime JVM (MB).                        |
| Available Processors           | Number of CPU cores available to the Mule Runtime JVM, displayed as a string (e.g., "16 Cores").         |

### Heap Memory

| Metric Name                        | Description                                                                                          |
|------------------------------------|------------------------------------------------------------------------------------------------------|
| Heap Memory Used                   | Amount of JVM heap memory currently in use by the Mule Runtime (MB).                                 |
| Heap Memory Committed              | Amount of JVM heap memory guaranteed to be available for the Mule Runtime (MB).                      |
| Heap Memory Max                    | Maximum amount of JVM heap memory that can be used by the Mule Runtime, displayed as a string (e.g., "1024.0 MB"). |
| Heap Memory Init                   | Initial amount of JVM heap memory requested at Mule Runtime startup, displayed as a string (e.g., "1024.0 MB"). |
| Heap Memory Used Percentage        | Percentage of maximum JVM heap memory currently in use by the Mule Runtime.                          |
| Non Heap Memory Used               | Amount of JVM non-heap memory (Metaspace, code cache) currently in use by the Mule Runtime (MB).     |
| Non Heap Memory Committed          | Amount of JVM non-heap memory guaranteed to be available for the Mule Runtime (MB).                  |
| Non Heap Memory Max                | Maximum amount of JVM non-heap memory that can be used by the Mule Runtime, displayed as a string (e.g., "704.0 MB"). |
| Non Heap Memory Init               | Initial amount of JVM non-heap memory requested at Mule Runtime startup, displayed as a string (e.g., "7.31 MB"). |
| Pending Object Finalization Count  | Number of Java objects in the Mule Runtime JVM waiting for finalization before garbage collection.    |

### Memory Pools

| Metric Name               | Description                                                                                              |
|---------------------------|----------------------------------------------------------------------------------------------------------|
| Eden Space Used           | Amount of G1 Eden space memory used by the Mule Runtime JVM for newly allocated objects (MB).             |
| Eden Space Committed      | Amount of G1 Eden space memory committed for the Mule Runtime JVM (MB).                                  |
| Eden Space Peak Used      | Peak amount of G1 Eden space memory used by the Mule Runtime JVM since startup (MB).                     |
| Old Gen Used              | Amount of G1 Old Generation memory used by the Mule Runtime JVM for long-lived objects (MB).             |
| Old Gen Committed         | Amount of G1 Old Generation memory committed for the Mule Runtime JVM (MB).                              |
| Old Gen Max               | Maximum amount of G1 Old Generation memory available to the Mule Runtime JVM, displayed as a string (e.g., "1024.0 MB"). |
| Old Gen Peak Used         | Peak amount of G1 Old Generation memory used by the Mule Runtime JVM since startup (MB).                 |
| Survivor Space Used       | Amount of G1 Survivor space memory used by the Mule Runtime JVM for objects surviving young GC (MB).     |
| Survivor Space Committed  | Amount of G1 Survivor space memory committed for the Mule Runtime JVM (MB).                              |
| Survivor Space Peak Used  | Peak amount of G1 Survivor space memory used by the Mule Runtime JVM since startup (MB).                 |
| Metaspace Used            | Amount of Metaspace memory used by the Mule Runtime JVM for class metadata (MB).                         |
| Metaspace Committed       | Amount of Metaspace memory committed for the Mule Runtime JVM (MB).                                      |
| Metaspace Max             | Maximum amount of Metaspace memory available to the Mule Runtime JVM, displayed as a string (e.g., "256.0 MB"). |
| Metaspace Peak Used       | Peak amount of Metaspace memory used by the Mule Runtime JVM since startup (MB).                         |
| Compressed Class Space Used | Amount of compressed class space memory used by the Mule Runtime JVM (MB).                             |

### Garbage Collection

| Metric Name          | Description                                                                                              |
|----------------------|----------------------------------------------------------------------------------------------------------|
| Young Gen GC Count   | Number of G1 Young Generation garbage collection events in the Mule Runtime JVM.                         |
| Young Gen GC Time    | Total time spent on G1 Young Generation garbage collections in the Mule Runtime JVM (min).               |
| Old Gen GC Count     | Number of G1 Old Generation garbage collection events in the Mule Runtime JVM.                           |
| Old Gen GC Time      | Total time spent on G1 Old Generation garbage collections in the Mule Runtime JVM (min).                 |
| Concurrent GC Count  | Number of G1 Concurrent garbage collection events in the Mule Runtime JVM.                               |
| Concurrent GC Time   | Total time spent on G1 Concurrent garbage collections in the Mule Runtime JVM (min).                     |
| Last GC Duration     | Duration of the most recent garbage collection pause in the Mule Runtime JVM (min).                      |
| Last GC Thread Count | Number of threads used by the most recent garbage collection event in the Mule Runtime JVM.              |

### Threads

| Metric Name                   | Description                                                                                              |
|-------------------------------|----------------------------------------------------------------------------------------------------------|
| Live Thread Count             | Number of currently active threads in the Mule Runtime JVM including daemon and non-daemon threads.      |
| Daemon Thread Count           | Number of daemon threads running in the Mule Runtime JVM for background tasks.                           |
| Peak Thread Count             | Highest number of threads that were simultaneously active in the Mule Runtime JVM since startup.         |
| Total Started Thread Count    | Total number of threads created and started in the Mule Runtime JVM since startup.                       |
| Non Daemon Thread Count       | Number of non-daemon threads running in the Mule Runtime JVM for application tasks.                      |
| Total Threads Allocated Bytes | Total memory allocated by all threads in the Mule Runtime JVM since startup (MB).                        |
| Current Thread CPU Time       | CPU time consumed by the current thread in the Mule Runtime JVM (min).                                   |

### CPU & System

| Metric Name                | Description                                                                                              |
|----------------------------|----------------------------------------------------------------------------------------------------------|
| Process CPU Load           | CPU load consumed by the Mule Runtime JVM process as a percentage of total CPU capacity.                 |
| Process CPU Time           | Total CPU time consumed by the Mule Runtime JVM process since startup (min).                             |
| Committed Virtual Memory   | Amount of virtual memory guaranteed to be available for the Mule Runtime JVM process (MB).               |
| Open File Descriptor Count | Number of file descriptors currently open by the Mule Runtime JVM process.                               |
| Max File Descriptor Count  | Maximum number of file descriptors allowed for the Mule Runtime JVM process, displayed as a string (e.g., "1048576 Descriptors"). |
