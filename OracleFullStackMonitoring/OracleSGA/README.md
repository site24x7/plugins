# Oracle SGA Monitoring


                                                                                              
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

- Create a directory named "OracleSGA".
- Install the **oracledb** python module.
	```
	pip3 install oracledb
	```

	
- Download the below files in the "OracleSGA" folder and place it under the "OracleSGA" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleSGA/OracleSGA.py && sed -i "1s|^.*|#! $(which python3)|" OracleSGA.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleSGA/OracleSGA.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```
	 python3 OracleSGA.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME>
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the OracleSGA.cfg file.
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
- Place the "OracleSGA" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/OracleSGA
  
#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "OracleSGA" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\OracleSGA


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.



## Supported Metrics
The following metrics are captured in the OracleSGA Plugin:

- **SGA Database Buffers**

- **SGA Fixed Size**

- **SGA Hit Ratio**

- **SGA Log Alloc Retries**

- **SGA Redo Buffers**

- **SGA Shared Pool Dict Cache Ratio**

- **SGA Shared Pool Lib Cache Hit Ratio**

- **SGA Shared Pool Lib Cache Reload Ratio**

- **SGA Shared Pool Lib Cache Sharable Statement**

- **SGA Shared Pool Lib Cache Shareable User**

- **SGA Variable Size**

- **Total Memory**
