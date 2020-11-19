Plugin for Monitoring Uptime of a Process
=========================================

### PreRequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "ps" command.

### Plugin installation
---
##### Linux 

- Create a directory "process_uptime"

- Download the files "process_uptime.py" , "process_uptime.cfg" and place it under the "process_uptime" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/process_uptime/process_uptime.py

  wget https://raw.githubusercontent.com/site24x7/plugins/master/process_uptime/process_uptime.cfg
	
- Edit the file process_uptime.cfg and provide the process to be monitored

        Make sure the given process is unique . If more than one process runs in the same name desired output wont be obtained.

        In that case provide any unique string from process arguments to match the exact process for monitoring.

        If more than one process needs to be monitored create a new section in the process_time.cfg and provide the process name.

- To make sure plugin is providing the correct output

        python process_uptime.py --process=<process_name>
 
- Copy-paste the process_uptime folder to the agent's plugin directory  under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/
  
- The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center


### Metrics Captured
---

start_time : Start time of the process

days : No of days the process is running

hours : No of hours the process is runnning

minutes : No of minutes the process is running

seconds : No of seconds the process is running