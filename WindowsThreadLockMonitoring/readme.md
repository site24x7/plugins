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
| `Dotnet Locks Total Contentions` | Cumulative number of times threads in the CLR have attempted to acquire a managed lock unsuccessfully since the process started. This counter only increases and resets to zero when the .NET process restarts. | contentions |
| `Dotnet Locks Total Contentions Delta` | Number of new lock contentions that occurred since the last polling interval. Calculated by subtracting the previous `Total Contentions` value (stored in `locks_state.json`) from the current value. | contentions |
| `Dotnet Locks Contention Rate Per Sec Global` | Rate at which threads in the CLR attempt to acquire a managed lock unsuccessfully, measured per second. A rising value indicates increasing lock contention in real time. | contentions/sec |
| `Dotnet Locks Current Queue Length Global` | Number of threads that are currently waiting to acquire a managed lock. A value greater than zero means threads are actively blocked waiting for a lock to be released. | waiting_threads |
| `Dotnet Locks Queue Length Per Sec Global` | Rate at which threads are added to the lock wait queue, measured per second. This represents the queue arrival rate, not the current queue depth. | queue_events/sec |
| `Dotnet Locks Queue Length Peak Global` | Highest number of threads that were simultaneously waiting to acquire a managed lock since the .NET process started. This value only increases and resets to zero on process restart. | peak_waiting_threads |
| `Dotnet Locks Current Logical Threads` | Number of current managed thread objects in the CLR. This includes all threads that have been started and not yet garbage collected, whether running, suspended, or stopped. | threads |
| `Dotnet Locks Current Physical Threads` | Number of native OS threads that the CLR has created to serve as underlying threads for managed thread objects. These are the actual operating system threads backing the managed threads. | threads |
| `Dotnet Locks Recognized Threads Rate Per Sec` | Rate at which previously unmanaged threads (threads created outside the CLR, such as COM interop or native code threads) are recognized by the CLR as they enter managed code, measured per second. | threads/sec |
| `Dotnet Locks Current Recognized Threads` | Number of threads that were originally created outside the CLR but have since entered managed code and are currently recognized by the runtime. | threads |
| `Dotnet Locks Total Recognized Threads` | Cumulative number of threads that have been recognized by the CLR since the process started. This value only increases and resets to zero on process restart. On stable systems, this value may stop changing once all external threads have been recognized. | threads |

### System Metrics

| **Metric** | **Description** | **Unit** |
|---|---|---|
| `System Processor Queue Length` | Number of threads that are ready to execute but waiting for a CPU core to become available. A sustained value above 2 per CPU core may indicate CPU pressure. | waiting_threads |
| `CPU Total Usage Percent` | Percentage of total processor time being used across all CPU cores. A value of 100 means all cores are fully utilized. | percent |
| `Process Thread Count` | Sum of thread counts from all user-mode processes on the system. This includes application processes, system services (`svchost`, `lsass`), and OS processes (`csrss`, `System`). | threads |
| `System Context Switches Per Sec` | Rate at which the processor switches execution from one thread to another, per second. High values may indicate excessive lock contention or too many threads competing for CPU time. | switches/sec |
| `System Threads` | Total number of threads managed by the OS kernel scheduler. This includes all user-mode process threads plus kernel-only threads such as driver worker threads and deferred procedure call (DPC) threads that do not belong to any user-mode process. | threads |

### Top Processes (Table)

Reports the top 5 processes sorted by CPU usage (lifetime CPU seconds).

| **Field** | **Description** | **Unit** |
|---|---|---|
| `name` | Generic identifier for the process entry (`Process1` through `Process5`), used as the row key in Site24x7. | \Uffffffff |
| `Process Name` | Actual name of the process as reported by the operating system. | \Uffffffff |
| `Thread Count` | Number of active threads currently running within the process. | threads |
| `Memory` | Working set memory of the process, which is the amount of physical RAM currently in use by the process. | MB |

