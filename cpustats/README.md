## Monitoring CPU statistics on a Server

## CPU Statistics plugin installation:
	
* Create a directory with the name "cpustats".

* Download the file "cpustats.py" from our GitHub repository using below command and place it under the "cpustats" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/cpustats/cpustats.py
		
* Execute the plugin script manually using below command to get valid json output

		python cpustats.py
		
* Move the directory "cpustats", under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/cpustats.

* The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Monitored Attributes : All the system listed cpu attributes in top command output. 

	user_percentage : % CPU time spent in user space
	system_percentage :  % CPU time spent in kernel space
	nicetime_percentage : % CPU time spent on low priority processes
	idle_percentage : % CPU time spent idle
	iowait_percentage : % CPU time spent in wait (on disk)
	hardwareirq_percentage : % CPU time spent servicing/handling hardware interrupts
	software_irq : % CPU time spent servicing/handling software interrupts
	steal_time : % CPU time in involuntary wait by virtual cpu while hypervisor is servicing another processor

Learn more about the plugin installation steps and the various performance metrics that you can monitor here
https://www.site24x7.com/plugins.html
