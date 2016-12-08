## Monitoring CPU statistics on a Server

## Monitored Attributes : All the system listed cpu attributes in top command output. 

	user_percentage : % CPU time spent in user space
	system_percentage :  % CPU time spent in kernel space
	nicetime_percentage : % CPU time spent on low priority processes
	idle_percentage : % CPU time spent idle
	iowait_percentage : % CPU time spent in wait (on disk)
	hardwareirq_percentage : % CPU time spent servicing/handling hardware interrupts
	software_irq : % CPU time spent servicing/handling software interrupts
	steal_time : % CPU time in involuntary wait by virtual cpu while hypervisor is servicing another processor
	
## CPU Statistics plugin installation:
	
Create a directory with the name "cpustats", under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/cpustats. 

Download the file "cpustats.py" from our GitHub repository and place it under the "cpustats" directory

## Commands to perform the above step:

	cd /opt/site24x7/monagent/plugins/
	mkdir cpustats
	cd cpustats
	wget https://raw.githubusercontent.com/site24x7/plugins/master/cpustats/cpustats.py

Once the plugin file is downloaded, the agent will mark it up in the next data collection and you can view it in Site24x7 client

Learn more about the plugin installation steps and the various performance metrics that you can monitor here
https://www.site24x7.com/plugins.html
