# Oracle RAC Database Monitoring

## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Prerequisites
- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.7 or higher version should be installed.
- Install **oracledb** module for python
	```
	pip3 install oracledb
	```

### Database User and Required Privileges

Create a dedicated Oracle RAC user for the RAC monitoring plugin and grant the required privileges.

```sql
CREATE USER {username} IDENTIFIED BY "{password}";

GRANT CREATE SESSION TO {username};

GRANT SELECT ON SYS.V_$PARAMETER TO {username};
GRANT SELECT ON SYS.V_$DATABASE TO {username};
GRANT SELECT ON SYS.V_$INSTANCE TO {username};

GRANT SELECT ON SYS.GV_$SYSMETRIC TO {username};
GRANT SELECT ON SYS.GV_$SYSSTAT TO {username};
GRANT SELECT ON SYS.GV_$STATNAME TO {username};
GRANT SELECT ON SYS.GV_$SYSTEM_EVENT TO {username};
GRANT SELECT ON SYS.GV_$INSTANCE TO {username};
```

### Installation  

- Create a directory named `oracle_rac`.

	```bash
 	mkdir oracle_rac
 	cd oracle_rac/
 	```
 
- Install the **oracledb** python module.
	```bash
	pip3 install oracledb
	```
	
- Download the below files [oracle_rac.cfg](https://github.com/site24x7/plugins/blob/master/oracle_rac/oracle_rac.cfg) and [oracle_rac.py](https://github.com/site24x7/plugins/blob/master/oracle_rac/oracle_rac.py) place it under the `oracle_rac` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_rac/oracle_rac.py && sed -i "1s|^.*|#! $(which python3)|" oracle_rac.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_rac/oracle_rac.cfg
	```
 
- Execute the below command with appropriate arguments to check for the valid json output:

	```bash
	 python3 oracle_rac.py --hostname "localhost" --port "1521" --sid "SID" --username "USERNAME" --password "PASSWORD" --oracle_home "ORACLE_HOME"
	 ```

- After the above command with parameters gives the expected output, please configure the relevant parameters in the oracle_rac.cfg file.

	```bash
	[RAC1]
	hostname = "localhost"
	port = "1521"
	sid = "ORCL"
	username = "oracle_rac_username"
	password = "oracle_rac_password"
	tls = "false"
	wallet_location = "/opt/oracle/product/19c/dbhome_1/network/admin/wallets"
	oracle_home = "/opt/oracle/product/19c/dbhome_1/"

 	[RAC2]
	hostname = "localhost"
	port = "1521"
	sid = "ORCL"
	username = "oracle_rac_username"
	password = "oracle_rac_password"
	tls = "false"
	wallet_location = "/opt/oracle/product/19c/dbhome_1/network/admin/wallets"
	oracle_home = "/opt/oracle/product/19c/dbhome_1/"
	```
 
#### Linux

- Place the `oracle_rac` under the Site24x7 Linux Agent plugin directory:
  
	```bash
 	mv oracle_rac /opt/site24x7/monagent/plugins
 	```
 
#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

-  Further, move the folder `oracle_rac` into the  Site24x7 Windows Agent plugin directory:

        C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\oracle_rac


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Oracle RAC Metrics

### Global Cache Metrics
| Name                                 | Description                                                                                    |
| ------------------------------------ | ---------------------------------------------------------------------------------------------- |
| GC CR Block Received Per Second      | Number of consistent read blocks received per second from other RAC instances via Global Cache |
| GC Current Block Received Per Second | Number of current blocks received per second from other RAC instances                          |
| GC Average CR Get Time               | Average time taken to retrieve consistent read blocks from another RAC instance                |
| GC Average Current Get Time          | Average time taken to retrieve current blocks from another RAC instance                        |
| GC CR Blocks Served Total            | Total number of consistent read blocks served to other RAC instances                           |
| GC Current Blocks Served Total       | Total number of current blocks served to other RAC instances                                   |
| GC CR Block Received Total           | Total number of consistent read blocks received from other instances                           |
| GC Current Block Received Total      | Total number of current blocks received from other instances                                   |
| Global Cache Blocks Lost             | Number of blocks lost during interconnect transmission between RAC nodes                       |
| Global Cache Blocks Corrupted        | Number of corrupted blocks detected during inter-instance communication                        |

### Global Cache Performance Metrics

| Name                                    | Description                                                        |
| --------------------------------------- | ------------------------------------------------------------------ |
| Global Cache Average Block Receive Time | Average time required to receive blocks from other RAC instances   |
| Global Cache Block Access Latency       | Latency experienced when accessing blocks via the Global Cache     |
| Global Cache Service Utilization        | Total number of global cache blocks exchanged across RAC instances |

### GC Wait Analysis

| Name                                 | Description                                            |
| ------------------------------------ | ------------------------------------------------------ |
| GC CR Request Avg Wait Time          | Average wait time for consistent read block requests   |
| GC Current Request Avg Wait Time     | Average wait time for current block requests           |
| GC CR Block Busy Avg Wait Time       | Average wait time when consistent read blocks are busy |
| GC Current Block Busy Avg Wait Time  | Average wait time when current blocks are busy         |
| GC Buffer Busy Acquire Avg Wait Time | Average wait time while acquiring global cache buffers |
| GC Buffer Busy Release Avg Wait Time | Average wait time while releasing global cache buffers |
| GC CR Request Wait Count             | Total number of consistent read block request waits    |
| GC Current Request Wait Count        | Total number of current block request waits            |
| GC CR Block Busy Wait Count          | Number of waits due to busy consistent read blocks     |
| GC Current Block Busy Wait Count     | Number of waits due to busy current blocks             |
| GC Buffer Busy Acquire Wait Count    | Number of waits while acquiring global cache buffers   |
| GC Buffer Busy Release Wait Count    | Number of waits while releasing global cache buffers   |

### RAC Interconnect Metrics

| Name                                   | Description                                                        |
| -------------------------------------- | ------------------------------------------------------------------ |
| Interconnect Bytes Received Per Second | Amount of data received per second through the RAC interconnect    |
| Interconnect Bytes Sent Per Second     | Amount of data transmitted per second through the RAC interconnect |

### RAC Cluster Health Metrics

| Name             | Description                                   |
| ---------------- | --------------------------------------------- |
| cluster_name     | Name of the Oracle RAC cluster database       |
| Active RAC Nodes | Number of active RAC instances in the cluster |
| RAC Nodes Down   | Number of RAC nodes currently unavailable     |

### RAC Node Discovery

| Name             | Description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| RAC_Node_Details | Per-instance details including instance name, host name, instance number, and status |
