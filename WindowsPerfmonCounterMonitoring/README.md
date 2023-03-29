# Monitor any perfmon counter in Windows Server

Windows Performance Counters provide a high-level abstraction layer that provides a consistent interface for collecting various kinds of system data such as CPU, memory, and disk usage. System administrators often use performance counters to monitor systems for performance or behavior problems. Software developers often use performance counters to examine the resource usage of their programs.
	
## **Prerequisite**

Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder named "WindowsPerfmonCounterMonitoring" under the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\WindowsPerfmonCounterMonitoring

2. Download all the files from the "WindowsPerfmonCounterMonitoring" folder in GitHub and place them under the created "WindowsPerfmonCounterMonitoring" directory.

		https://raw.githubusercontent.com/site24x7/plugins/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.ps1
		https://raw.githubusercontent.com/site24x7/plugins/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.cfg
		
3. Open the "WindowsPerfmonCounterMonitoring.cfg" and in the counters config, configure your desired perfmon counters and displaynames. The value of each is separated by a comma .

		[counter_monitoring]
		counters="\Web Service(_Total)\Current Connections,\Processor Information(_Total)\% Processor Time,\Server\Logon Total"
		displaynames="webservice_current_connections,processor_time,total_server_logon"
		


Please ensure to map the metric number and position of each counter, displaynames correctly. 
For example, the number of counters and displaynames should be same. Also, the first metric from counters should map to displaynames.

 The agent will automatically execute the plugin within five minutes and send metrics to the Site24x7 data center.



