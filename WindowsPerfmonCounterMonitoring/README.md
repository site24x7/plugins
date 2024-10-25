# Monitor any perfmon counter in Windows Server

Windows Performance Counters provide a high-level abstraction layer that provides a consistent interface for collecting various kinds of system data such as CPU, memory, and disk usage. System administrators often use performance counters to monitor systems for performance or behavior problems. Software developers often use performance counters to examine the resource usage of their programs.
	
## **Prerequisite**

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- After installation of the Site24x7 Windows agent, to run Powershell plugin, ensure the below policy has been set.
  - Run the PowerShell prompt as Admin and execute the following 
  - Set-ExecutionPolicy RemoteSigned


## **Plugin installation**

1. Create a folder named `WindowsPerfmonCounterMonitoring`.

2. Download the below files [WindowsPerfmonCounterMonitoring.cfg](https://github.com/site24x7/plugins/blob/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.cfg) and [WindowsPerfmonCounterMonitoring.ps1](https://github.com/site24x7/plugins/blob/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.ps1), and place them under the created "WindowsPerfmonCounterMonitoring" directory.
	```
	wget https://raw.githubusercontent.com/site24x7/plugins/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.ps1
	wget https://raw.githubusercontent.com/site24x7/plugins/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.cfg
	```
		
3. To monitor desired Windows perfmon counters, you need the exact names of the performance counters. To get the counter name from the Windows Performance Monitor [read this](https://support.site24x7.com/portal/en/kb/articles/add-perfmon-counters-in-windows) article.

5. Open the "WindowsPerfmonCounterMonitoring.cfg" and in the counters config, configure your desired perfmon counters, units and displaynames. The value of each is separated by a comma. Example as follows

  	```bash
	[counter_monitoring]
	counters="\LogicalDisk(C:)\Avg. Disk sec/Write,\Processor Information(_Total)\% Processor Time,\LogicalDisk(C:)\Avg. Disk Bytes/Write,\Processor(_Total)\% Idle Time,\Event Log\Events/sec,\PhysicalDisk(_Total)\Avg. Disk Bytes/Read,\LogicalDisk(_Total)\Current Disk Queue Length,\Thread(_Total/_Total)\Priority Current,\Process(_Total)\IO Read Operations/sec,\Database(HealthService)\Database Cache % Hit"
	```
		
6. Further move the folder `WindowsPerfmonCounterMonitoring` into the Site24x7 Windows Agent plugin directory:
   
	```
	C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
	```
 
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations. 
