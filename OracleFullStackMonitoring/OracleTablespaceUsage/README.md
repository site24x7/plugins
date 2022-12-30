# Oracle TablespaceUsage Monitoring


                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install cx_Oracle module for python
```
  pip3 install cx_Oracle
```
---


### Plugin Installation  

- Create a directory named "OracleTablespaceUsage" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/OracleTablespaceUsage
      
- Download all the files in the "OracleTablespaceUsage" folder and place it under the "OracleTablespaceUsage" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleTablespaceUsage/OracleTablespaceUsage.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleTablespaceUsage/OracleTablespaceUsage.cfg

- Execute the following command in your server to install OracleTablespaceUsage: 

		pip3 install cx_Oracle

- Execute the below command with appropriate arguments to check for the valid json output:
```
 python3 OracleTablespaceUsage.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME> --tablespace_name=<TABLESPACE_NAME>
 ```

---

### Configurations

- Provide your OracleTablespaceUsage configurations in OracleTablespaceUsage.cfg file.
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

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.



## Supported Metrics
The following metrics are captured in the OracleTablespaceUsage Plugin:

- **Usage Percent**

    Memory usage of oracle tablespace in Percentage

- **Status**

    Status of oracle tablespace

