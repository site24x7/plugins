# Oracle Blocking Locks Monitoring


                                                                                              
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

- Create a directory named "OracleBlockingLocks".
- Download the cx_Oracle python module in the "OracleBlockingLocks".
	- For Linux 	
		```
		wget https://github.com/site24x7/plugins/raw/master/OracleFullStackMonitoring/cx_Oracle/cx_Oracle_linux/cx_Oracle.cpython-36m-x86_64-linux-gnu.so
		```
	- For Windows download the module file from below link.
	
		https://github.com/site24x7/plugins/raw/master/OracleFullStackMonitoring/cx_Oracle/cx_Oracle_windows/cx_Oracle.cp38-win32.pyd
	
- Download the below files in the "OracleBlockingLocks" folder and place it under the "OracleBlockingLocks" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleBlockingLocks/OracleBlockingLocks.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleBlockingLocks/OracleBlockingLocks.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```
	 python3 OracleBlockingLocks.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME>
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the OracleBlockingLocks.cfg file.
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
- Move the "OracleBlockingLocks" folder into the Site24x7 Linux Agent plugin directory: 
	```
	Linux             ->   /opt/site24x7/monagent/plugins/OracleBlockingLocks
	```
	```
	Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\OracleBlockingLocks
	```

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics
The following metrics are captured in the OracleBlockingLocks Plugin

- **Blocking Session**

    Session identifier of the blocking session

- **SID**

    Session Identifier

- **Serial**

    Session serial number


- **Seconds Waited**

    Amount of time waited for the current wait

- **Username**

    Oracle Username




