# Monitor any perfmon counter in Windows Server

Windows Performance Counters provide a high-level abstraction layer that provides a consistent interface for collecting various kinds of system data such as CPU, memory, and disk usage. System administrators often use performance counters to monitor systems for performance or behavior problems. Software developers often use performance counters to examine the resource usage of their programs.
	
## **Prerequisite**

Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- To run powershell plugin, ensure the below policy has been set.

  - Login to your server
  - Run the PowerShell prompt as Admin and execute the following:
  - Set-ExecutionPolicy RemoteSigned
  - Restart the plugin agent service

## **Plugin installation**

1. Create a folder named "WindowsPerfmonCounterMonitoring" under the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\WindowsPerfmonCounterMonitoring

2. Download all the files from the "WindowsPerfmonCounterMonitoring" folder in GitHub and place them under the created "WindowsPerfmonCounterMonitoring" directory.

		https://raw.githubusercontent.com/site24x7/plugins/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.ps1
		https://raw.githubusercontent.com/site24x7/plugins/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.cfg
		
3. Open the "WindowsPerfmonCounterMonitoring.cfg" and in the counters config, configure your desired perfmon counters, units and displaynames. The value of each is separated by a comma. Example as follows

		[counter_monitoring]
		counters="\LogicalDisk(C:)\Avg. Disk sec/Write,\Processor Information(_Total)\% Processor Time,\LogicalDisk(C:)\Avg. Disk Bytes/Write,\Processor(_Total)\% Idle Time,\Event Log\Events/sec,\PhysicalDisk(_Total)\Avg. Disk Bytes/Read,\LogicalDisk(_Total)\Current Disk Queue Length,\Thread(_Total/_Total)\Priority Current,\Process(_Total)\IO Read Operations/sec,\Database(HealthService)\Database Cache % Hit"
		
		units="sec/Write,%,bytes/Write,%,/sec,bytes/read,count,count,/sec,%"
				displaynames="disk_write,processor_time,disk_byteswrite,Processor_idle_time,event_logs,disk_read,disk_queue_length,current_priority_thread,IO_read_operations,database_healthservice_cache_hit"
		


Please ensure to map the metric number and position of each counter, units, displaynames correctly. 
For example, the number of counters, units, and displaynames should be same. Also, the first metric from counters should map to both units and displaynames.

 The agent will automatically execute the plugin within five minutes and send metrics to the Site24x7 data center.




