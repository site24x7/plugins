# Yugabyte Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `yugabyte`.
  
```bash
mkdir yugabyte
cd yugabyte/
```
      
- Download below files and place it under the "yugabyte" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/yugabyte/yugabyte.py && sed -i "1s|^.*|#! $(which python3)|" yugabyte.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/yugabyte/yugabyte.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 yugabyte.py --hostname localhost --port 8080 --username yugabyte --password yugabyte 
```

- Provide your yugabyte configurations in yugabyte.cfg file.

```bash
[yugabyte-server]
hostname = "localhost"
port = "5433"
username = "yugabyte"
password = "yugabyte"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "yugabyte" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv yugabyte /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "yugabyte" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Yugabyte Server Monitoring Plugin Metrics

| Metric                  | Description                                                                                       |
|-------------------------|---------------------------------------------------------------------------------------------------|
| `YugabyteDB_Version`    | The version of YugabyteDB currently running.                                                      |
| `Active_Sessions`       | The number of active sessions currently connected to the database.                                |
| `Total_Connection`      | The total number of connections to the database.                                                  |
| `Database_Details`      | Details about individual databases, including name, size, active connections, transaction stats, and cache hit ratio. |
| `Database_Size_in_bytes`| Size of the specific database in bytes.                                                           |
| `Active_Connections`    | Number of active connections for a particular database.                                           |
| `Transactions_Committed`| Number of transactions committed for a particular database.                                       |
| `Transactions_Rolledback`| Number of transactions rolled back for a particular database.                                    |
| `Cache_Hit_Ratio`       | Cache hit ratio for a particular database, indicating cache efficiency.                          |
| `Database_Locks`        | Number of database locks currently in place.                                                      |
| `Avg_Query_Time`        | Average query execution time in seconds.                                                          |
| `Total_Disk_Usage`      | Total disk usage by the database in bytes.                                                        |
| `Throughput`            | Number of transactions processed per second.                                                      |
| `Total_Queries`         | Total number of queries executed across the databases.                                            |
