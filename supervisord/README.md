# Monitor supervisor instances with Site24x7 plugins

The server piece of supervisor is called as supervisord. Thus, supervisord monitoring is critical to monitor the application processes managed by supervisor, its count, and the overall state of the server to keep a track of all the processes or identify the problematic ones.

Know how to configure the supervisor plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of supervisord servers.

Learn more: https://www.site24x7.com/plugins/supervisord-monitoring.html

[How to install supervisor?]: <http://supervisord.org/installing.html>


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.
- Execute the following command in your server to install Redis:

      pip install supervisor


### Plugin Installation  

- Create a directory named "supervisord"

- Download the below files and place it under the "supervisord" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/supervisord/supervisord.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the supervisord.py script.

- Edit the supervisord.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python supervisord.py
  #### Linux

- Place the "supervisord" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/supervisord

  #### Windows 

- Move the folder "supervisord" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\supervisord
