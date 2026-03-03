# Windows Thread Lock Monitoring

## Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- The server must have .NET Framework applications running to populate the `.NET CLR LocksAndThreads` performance counters.

### Plugin Installation

- Create a directory named `WindowsThreadLockMonitoring`.

```bash
mkdir WindowsThreadLockMonitoring
cd .\WindowsThreadLockMonitoring\
```

- Download the below file and place it under the "WindowsThreadLockMonitoring" directory.

```bash
WindowsThreadLockMonitoring.ps1
```

- Execute the below command to check for the valid json output:

```bash
powershell .\WindowsThreadLockMonitoring.ps1
```

### Move the plugin under the Site24x7 agent directory

- Move the "WindowsThreadLockMonitoring" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---

## Windows Thread Lock Monitoring Metrics

### .NET CLR Lock & Thread Metrics

| **Metric** | **Description** | **Unit** |
|---|---|---|
| `Dotnet Locks Total Contentions` | Total number of times threads in the CLR have attempted to acquire a managed lock unsuccessfully (cumulative). | contentions |
| `Dotnet Locks Total Contentions Delta` | Number of new lock contentions since the last polling interval. Computed from the state file. | contentions |
| `Dotnet Locks Contention Rate Per Sec Global` | Rate at which threads in the CLR attempt to acquire a managed lock unsuccessfully, per second. | contentions/sec |
| `Dotnet Locks Current Queue Length Global` | Number of threads currently waiting to acquire a managed lock. | waiting_threads |
| `Dotnet Locks Queue Length Per Sec Global` | Number of threads per second waiting to acquire a lock. Represents queue arrival rate, not an instantaneous count. | queue_events/sec |
| `Dotnet Locks Queue Length Peak Global` | Peak number of threads that waited to acquire a managed lock since the application started. | peak_waiting_threads |
| `Dotnet Locks Current Logical Threads` | Number of current managed thread objects in the CLR, including both running and stopped threads. | threads |
| `Dotnet Locks Current Physical Threads` | Number of native OS threads created and owned by the CLR to act as underlying threads for managed thread objects. | threads |
| `Dotnet Locks Rate Recognized Threads Per Sec` | Rate at which the CLR recognizes previously unmanaged threads entering the managed runtime, per second. | threads/sec |
| `Dotnet Locks Current Recognized Threads` | Number of currently recognized threads that have an associated managed thread object. | threads |
| `Dotnet Locks Total Recognized Threads` | Total number of threads that have been recognized by the CLR since the application started (cumulative). | threads |

### System Metrics

| **Metric** | **Description** | **Unit** |
|---|---|---|
| `System Processor Queue Length` | Number of threads waiting in the processor queue. A sustained value above 2 per CPU may indicate CPU pressure. | waiting_threads |
| `Cpu Total Usage Percent` | Total processor time across all cores as a percentage. | percent |
| `Process Thread Count` | Total number of threads across all processes on the system. | threads |
| `System Context Switches Per Sec` | Rate at which the processor switches from one thread to another, per second. High values may indicate excessive lock contention. | switches/sec |
| `System Threads` | Total number of threads in the system at the time of data collection. | threads |

### Top Processes (Table)

Reports the top 5 processes sorted by CPU usage (lifetime CPU seconds).

| **Field** | **Description** | **Unit** |
|---|---|---|
| `name` | Generic identifier (`Process1` through `Process5`). |  |
| `Process Name` | Name of the process. |  |
| `Thread Count` | Number of threads in the process. | threads |
| `Memory` | Working set memory usage of the process. | MB |

