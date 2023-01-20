# Monitor any perfmon counter in Windows Server

Monitor any perfmon counter.

	
## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder named "WindowsPerfmonCounterMonitoring" under the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\WindowsPerfmonCounterMonitoring

2. Download all the files from the "WindowsPerfmonCounterMonitoring" folder and place them under the "WindowsPerfmonCounterMonitoring" directory.

		https://raw.githubusercontent.com/site24x7/plugins/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.ps1
		https://raw.githubusercontent.com/site24x7/plugins/master/WindowsPerfmonCounterMonitoring/WindowsPerfmonCounterMonitoring.cfg
		
3. Open the "WindowsPerfmonCounterMonitoring.cfg" and In the counters config, configure your desired perfmon counters by one by one comma separated with double quotes. Example config as follows.

		[counter_monitoring]
		counters="\LogicalDisk(C:)\Avg. Disk sec/Write,\Processor Information(_Total)\% Processor Time,\LogicalDisk(C:)\Avg. Disk Bytes/Write"
		units="sec/Write,%,bytes/Write"
		displaynames="c:disk sec/write,processor time %,c:disk bytes/write"
		
  You can add any perfmon counter with comma (,) seperated value. Please ensure to configure all three counters,units,displayname for all perfmon counter. 

  The agent will automatically execute the plugin within five minutes and send metrics to the Site24x7 data center.


