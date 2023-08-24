# Oracle Waits Monitoring


                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Install python3.7 or higher version on the server.
- Roles need to be granted for the user to be used in plugin

	```
	grant select_catalog_role to {username}
	```
	```
	grant create session to {username}
	```
---


### Plugin Installation  

- Create a directory named "OracleWaits".
- Install the **oracledb** python module.
	```
	pip3 install oracledb
	```
	
- Download the below files in the "OracleWaits" folder and place it under the "OracleWaits" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleWaits/OracleWaits.py && sed -i "1s|^.*|#! $(which python3)|" OracleWaits.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleWaits/OracleWaits.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```
	 python3 OracleWaits.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME>
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the OracleWaits.cfg file.

```
    [ORCL]
    hostname=localhost
    port=1521
    sid=<SID>
    username=<USERNAME>
    password=<PASSWORD>
    logs_enabled="False"
    log_type_name =None
    log_file_path=None
    oracle_home=None

```	
#### Linux
- Place the "OracleWaits" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/OracleWaits

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "OracleWaits" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\OracleWaits


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.



## Supported Metrics
The following metrics are captured in the OracleWaits Plugin:

- **Free Buffer Waits**

- **Buffer Busy Waits**

- **Latch Free**

- **Library Cache Pin**

- **Library Cache Load Lock**

- **Log Buffer Space**

- **Library Object Reloads Count**

- **Enqueue Waits**

- **DB File Parallel Read**

- **DB File Parallel Write**

- **Control File Sequential Read**

- **Control File Parallel Write**

- **Write Complete Waits**

- **Log File Sync**

- **Sort Segment Request**

- **Direct Path Read**

- **Direct Path Write**

