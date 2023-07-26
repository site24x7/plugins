# Monitor your Lighttpd web server metrics

A web server, Lighttpd is known for its smaller size, speed and scalability. Lighttpd monitoring is critical to reduce both lag and downtime, and at the same time troubleshoot efficiently when these issues occur.

Know how to configure the Lighttpd plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Lighttpd web servers.

Learn more: https://www.site24x7.com/plugins/lighttpd-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "lighttpd"

- Download the below files and place it under the "lighttpd" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/lighttpd/lighttpd.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the lighttpd.py script.

- Edit the lighttpd.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python lighttpd.py
  #### Linux

- Place the "lighttpd" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/lighttpd

  #### Windows 

- Move the folder "lighttpd" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\lighttpd
