# Oracle SGA Monitoring


                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install cx_Oracle module for python
```
  pip3 install cx_Oracle
```
---


### Plugin Installation  

- Create a directory named "OracleSGA" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/OracleSGA
      
- Download all the files in the "OracleSGA" folder and place it under the "OracleSGA" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OraclePDB/OracleSGA.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OraclePDb/OracleSGA.cfg

- Execute the following command in your server to install OracleSGA: 

		pip3 install cx_Oracle

- Execute the below command with appropriate arguments to check for the valid json output:
```
 python3 OracleSGA.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME>
 ```

---

### Configurations

- Provide your OracleSGA configurations in OracleSGA.cfg file.
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

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics
The following metrics are captured in the OraclePDB Plugin:

# Oracle SGA Monitoring


                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install cx_Oracle module for python
```
  pip3 install cx_Oracle
```
---


### Plugin Installation  

- Create a directory named "OracleSGA" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/OracleSGA
      
- Download all the files in the "OracleSGA" folder and place it under the "OracleSGA" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleSGA/OracleSGA.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/OracleFullStackMonitoring/OracleSGA/OracleSGA.cfg

- Execute the following command in your server to install OracleSGA: 

		pip3 install cx_Oracle

- Execute the below command with appropriate arguments to check for the valid json output:
```
 python3 OracleSGA.py --hostname=<name of the host> --port=<port> --sid=<SID> --username=<USERNAME> --password=<PASSWORD> --oracle_home=<ORACLE_HOME>
 ```

---

### Configurations

- Provide your OracleSGA configurations in OracleSGA.cfg file.
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
