# Oracle Tablespace Usage Monitoring


                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Install **python3.7** or higher version on the server.
- Roles need to be granted for the user to be used in plugin

	```
	grant select_catalog_role to {username}
	```
	```
	grant create session to {username}
	```
---

### Plugin Installation  

- Create a directory named "OracleTablespaceUsage".
- Install the **oracledb** python module.
	```
	pip3 install oracledb
	```
	
- Download the below files in the "OracleTablespaceUsage" folder and place it under the "OracleTablespaceUsage" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleTablespaceUsage/OracleTablespaceUsage.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleTablespaceUsage/OracleTablespaceUsage.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```
	 python3 OracleTablespaceUsage.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME>
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the OracleTablespaceUsage.cfg file.

	```
	[ORCL]
	hostname=localhost
	port=1521
	sid=<SID>
	username=<USERNAME>
	password=<PASSWORD>
	tablespace_names='["SYSTEM","USERS"]'
	logs_enabled="False"
	log_type_name =None
	log_file_path=None
	oracle_home=None
	```	
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the OracleTablespaceUsage.py script.

- Place the "OracleTablespaceUsage" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/OracleTablespaceUsage

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "OracleTablespaceUsage" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\OracleTablespaceUsage


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.




## Supported Metrics
The following metrics are captured in the OracleTablespaceUsage Plugin:

- **Usage Percent**

    Memory usage of oracle tablespace in Percentage

- **Status**

    Status of oracle tablespace

