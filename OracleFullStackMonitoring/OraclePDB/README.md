# Oracle PDB Monitoring


                                                                                              
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

- Create a directory named "OraclePDB".
- Install the **oracledb** python module.
	```
	pip3 install oracledb
	```

	
- Download the below files in the "OraclePDB" folder and place it under the "OraclePDB" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OraclePDB/OraclePDB.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OraclePDB/OraclePDB.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```
	 python3 OraclePDB.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME>
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the OraclePDB.cfg file.
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
- Move the "OraclePDB" folder into the Site24x7 Linux Agent plugin directory: 
	```
	Linux             ->   /opt/site24x7/monagent/plugins/OraclePDB
	```
	```
	Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\OraclePDB
	```

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics
The following metrics are captured in the OraclePDB Plugin:

- **PDB_ID**

    ID of the PDB

- **Status**

    Status of the PDB

- **OpenMode**

    Mode of the PDB

- **Restricted**

    Status of restricted mode in PDB

- **OpenTime**

  Open time of PDB
