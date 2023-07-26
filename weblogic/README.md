Plugin for WebLogic Monitoring
=============================

Oracle WebLogic is a Java EE application server. Install and use our WebLogic monitoring tool and get detailed insights into database activity and health.

Get to know how to configure the WebLogic plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of WebLogic servers.

Learn more https://www.site24x7.com/plugins/weblogic-plugin-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "weblogic"

- Download the below files and place it under the "weblogic" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/weblogic/weblogic.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the weblogic.py script.

- Edit the weblogic.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python weblogic.py --host='host' --port='port' --username='username' --password='password'

- Then place the configurations in the weblogic.py file.

        [local_server]
        host=<host>
        port=<port_no>
        username=<user_name>
        password=<password>
  
  #### Linux

- Place the "weblogic" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/weblogic

  #### Windows 

- Move the folder "weblogic" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\weblogic
