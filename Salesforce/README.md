Plugin for Salesforce Log Monitoring
====================================

Salesforce offers a Event Log File (ELF) [API](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_eventlogfile_supportedeventtypes.htm) to access your Salesforce account activities. 
Configure the Site24x7 Salesforce plugin and monitor and manage Salesforce event logs effectively. 

This document details how to configure the Salesforce plugin and how Site24x7 manages its logs.

Learn more https://www.site24x7.com/help/log-management/salesforce-logs.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "Salesforce"

- Download the below files and place it under the "Salesforce" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/Salesforce/Salesforce.py


- Edit the Salesforce.cfg file with appropriate arguments and Execute the plugin manually to check for the valid JSON output

#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the Salesforce.py script.

- Place the "Salesforce" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/Salesforce

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "Salesforce" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\Salesforce
