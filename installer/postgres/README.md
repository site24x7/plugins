Plugin for PostGres Monitoring
=============================

PostgreSQL is an ORDBMS server whose primary function is to store data securely, and allows retrieval at the request of other software applications. Analyze and optimize your Postgres server by configuring our Postgres plugin and proactively monitor the availability and performance of business-crtical Postgres database server.

Get to know how to configure the PostgreSQL plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Postgres servers.

Learn more https://www.site24x7.com/plugins/postgres-monitoring.html

## Quick installation

If you're using Linux servers, use the postgres plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/installer/Site24x7PostgresPluginInstaller.sh && sudo bash Site24x7PostgresPluginInstaller.sh
```

### Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python version 3 or higher.
- Execute the following command in your server to install psycopg2: 

		pip3 install psycopg2-binary

### Plugin Installation  

- Create a directory named `postgres`.

	```bash
	mkdir postgres
	cd postgres/
	```
  
- Download all the files and place it under the `postgres` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/postgres.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/postgres.cfg
	```
 
- Execute the following command in your server to install psycopg2: 

	```bash
	pip3 install psycopg2-binary
	```
 
- Ensure **pg_read_all_stats** permission is provided to the user. For example, create a user `site24x7` with password `site24x7` and provide `pg_read_all_stats` permission to the `site24x7` user created.
  
- Execute the below command with appropriate arguments to check for the valid json output:

	```bash
	python3 postgres.py  --host "localhost" --port "5432" --username "username" --password "password" --db "postgres"
	```
 
- Provide your Postgres DB configurations in postgres.cfg file.

    ```ini
    [postgres]
    host="localhost"
    port="5432"
    username="None"
    password="None"
    db="postgres"
    plugin_version="1"
    ```
    
  #### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the postgres.py script.
- Move the directory `postgres` under the Site24x7 Linux Agent plugin directory: 
	```bash
	mv postgres /opt/site24x7/monagent/plugins/
 	```
 
  #### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.


- Move the folder `postgres` under Site24x7 Windows Agent plugin directory: 
	```bash
	C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
 	```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## PostgreSQL Server Monitoring Plugin Metrics

| **Metric Name**                    | **Description**                                                                        |
|-------------------------------------|----------------------------------------------------------------------------------------|
| Table Count                         | The total number of tables in the database.                                            |
| Active Queries                      | The number of queries that are currently active.                                        |
| Transactions Open                   | The number of transactions currently open.                                             |
| Transactions Idle In Transaction    | The number of transactions that are idle within a transaction.                         |
| Active Connections                  | The number of active connections to the database.                                      |
| Total Commits                       | The total number of commits executed in the database.                                  |
| Total Rollbacks                     | The total number of rollbacks executed in the database.                                |
| Total Conflicts                     | The number of conflicts that occurred during database operations.                      |
| Checkpoints Timed                   | The total number of timed checkpoints.                                                 |
| Checkpoints Req                     | The total number of requested checkpoints.                                             |
| Checkpoint Write Time               | The total time spent writing during checkpoints in milliseconds.                       |
| Checkpoint Sync Time                | The total time spent syncing during checkpoints in milliseconds.                       |
| Buffers Checkpoint                  | The number of buffers used during checkpoint processes.                                |
| Buffers Clean                       | The number of clean buffers used during checkpoint processes.                          |
| Maxwritten Clean                    | The number of maximum written clean buffers.                                           |
| Buffers Backend                     | The number of buffers used by the backend.                                             |
| Buffers Backend Fsync               | The number of buffers flushed to disk by the backend.                                  |
| Buffers Alloc                       | The number of buffer allocations in the system.                                        |
| Locks Count                         | The total number of locks held by the database.                                        |
| Max Connections                     | The maximum number of allowed connections to the database.                             |
| Total Rows Inserted                 | The total number of rows inserted into the database.                                   |
| Total Rows Updated                  | The total number of rows updated in the database.                                      |
| Total Rows Deleted                  | The total number of rows deleted from the database.                                    |
| Total Rows Fetched                  | The total number of rows fetched from the database.                                    |
| Total Rows Returned                 | The total number of rows returned by queries.                                         |
| Total Block Reads                   | The total number of blocks read from disk.                                             |
| Total Block Hits                    | The total number of block hits (cache hits) in memory.                                 |
| Index Scans                         | The total number of index scans performed.                                             |
| Index Rows Read                     | The total number of rows read through index scans.                                    |
| Index Rows Fetched                  | The total number of rows fetched via index scans.                                      |
| Server Version                      | The version of the PostgreSQL server currently running.                                |
| Uptime                              | The total time the PostgreSQL server has been running since the last restart.         |
| Database Count                      | The total number of databases in the PostgreSQL instance.                              |
| Total Sessions                      | The total number of active sessions in the PostgreSQL server.                          |
| Total Sessions Abandoned            | The number of sessions abandoned by users.                                             |
| Total Sessions Fatal                | The number of sessions that ended with a fatal error.                                 |
| Total Sessions Killed               | The number of sessions that were killed.                                               |
| Heap Blocks Read                    | The total number of heap blocks read from the disk.                                    |
| Heap Blocks Hit                     | The total number of heap blocks found in memory.                                       |
| Cache Hit Ratio                     | The ratio of cache hits versus block reads.                                            |
| Active Waiting Queries              | The number of queries that are currently waiting for resources to become available.    |

## Transactions and Session Metrics per Database

| **Metric Name**                    | **Description**                                                                        |
|-------------------------------------|----------------------------------------------------------------------------------------|
| Commits                            | The total number of commits executed in the specific database.                         |
| Rollbacks                          | The total number of rollbacks executed in the specific database.                       |
| Conflicts                          | The number of conflicts that occurred in the specific database.                        |
| Sessions                           | The total number of active sessions in the specific database.                          |
| Sessions Abandoned                 | The number of sessions abandoned by users in the specific database.                    |
| Sessions Fatal                     | The number of sessions that ended with a fatal error in the specific database.         |
| Sessions Killed                    | The number of sessions that were killed in the specific database.                      |
| Session Time                       | The total session time for all sessions in the specific database.                      |
| Sessions Active Time               | The total active time spent by sessions in the specific database.                      |
| Session Idle In Transaction Time   | The total idle time within transactions in the specific database.                     |

## Stats per Database

| **Metric Name**                    | **Description**                                                                        |
|-------------------------------------|----------------------------------------------------------------------------------------|
| Active Connections                  | The number of active connections in the specific database.                             |
| Size in MB                          | The size of the specific database in megabytes.                                        |
| Rows Inserted                       | The total number of rows inserted into the specific database.                          |
| Rows Updated                        | The total number of rows updated in the specific database.                             |
| Rows Deleted                        | The total number of rows deleted from the specific database.                           |
| Rows Fetched                        | The total number of rows fetched from the specific database.                           |
| Rows Returned                       | The total number of rows returned by queries in the specific database.                 |
| Block Reads                         | The total number of blocks read from disk in the specific database.                    |
| Block Hits                          | The total number of block hits (cache hits) in memory in the specific database.        |

![Image](https://github.com/user-attachments/assets/60577fff-5947-4c96-98ef-2271c9dbce82)
