# Oracle Tablespace Monitoring

## Overview

Monitor Oracle tablespaces with pagination support. The plugin collects tablespace usage metrics and datafile details, reporting 25 tablespaces per page.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.7 or higher version should be installed.
- Install **oracledb** module for python
	```
	pip3 install oracledb
	```

- Roles need to be granted

	```sql
	grant select_catalog_role to {username}
	```
	```sql
	grant create session to {username}
	```

## Installation

- Create a directory named `oracle_tablespace`.

	```bash
	mkdir oracle_tablespace
	cd oracle_tablespace/
	```

- Install the **oracledb** python module.
	```bash
	pip3 install oracledb
	```

- Download the below files [oracle_tablespace.cfg](https://github.com/site24x7/plugins/blob/master/oracle_tablespace/oracle_tablespace.cfg) and [oracle_tablespace.py](https://github.com/site24x7/plugins/blob/master/oracle_tablespace/oracle_tablespace.py) and place them under the `oracle_tablespace` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_tablespace/oracle_tablespace.py && sed -i "1s|^.*|#! $(which python3)|" oracle_tablespace.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_tablespace/oracle_tablespace.cfg
	```

- Execute the below command with appropriate arguments to check for the valid json output:

	```bash
	python3 oracle_tablespace.py --hostname "localhost" --port "1521" --sid "SID" --username "USERNAME" --password "PASSWORD" --oracle_home "ORACLE_HOME" --get "1"
	```

- After the above command with parameters gives the expected output, please configure the relevant parameters in the oracle_tablespace.cfg file.

	```ini
	[ORCL-1-25]
	hostname = "localhost"
	port = "1521"
	sid = "xe"
	username = "oracle_username"
	password = "oracle_password"
	tls = "false"
	wallet_location = "/opt/oracle/product/19c/dbhome_1/network/admin/wallets"
	oracle_home = "/opt/oracle/product/19c/dbhome_1/"
	get="1"
	```

> [!NOTE]
> The `get` parameter controls pagination. Each page returns up to 25 tablespaces. To monitor more than 25 tablespaces, create additional sections in the `.cfg` file with incremented `get` values (e.g., `get="2"` for tablespaces 26–50).

#### Linux

- Place the `oracle_tablespace` under the Site24x7 Linux Agent plugin directory:

	```bash
	mv oracle_tablespace /opt/site24x7/monagent/plugins
	```

#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Further, move the folder `oracle_tablespace` into the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\oracle_tablespace

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics

### Tablespace Metrics

Name				| Description
---				|   ---
Tablespace_Size			|	Tablespace size in MB
Tablespace_Free_Size		|	Free space available in the tablespace in MB
Used_Space			|	Tablespace used space in MB
Used_Percent			|	Tablespace usage in percent (%)
Contents			|	Type of tablespace contents (PERMANENT, TEMPORARY, UNDO)
Logging				|	Whether logging is enabled for the tablespace
TB_Status			|	Availability of the tablespace (ONLINE/OFFLINE)

### Tablespace Datafile Metrics

Name				| Description
---				|   ---
Data_File_Size			|	Size of the datafile in MB
Data_File_Blocks		|	Number of Oracle blocks in the datafile
Autoextensible			|	Whether the datafile can automatically extend (YES/NO)
Max_Data_File_Size		|	Maximum size the datafile can grow to in MB
Max_Data_File_Blocks		|	Maximum number of blocks the datafile can contain
Increment_By			|	Number of blocks by which the datafile auto-extends
Usable_Data_File_Size		|	Usable size of the datafile in MB
Usable_Data_File_Blocks		|	Number of usable blocks in the datafile
Tablespace			|	Name of the tablespace the datafile belongs to
