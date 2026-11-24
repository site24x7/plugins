Plugin for PostgreSQL Monitoring
=============================

PostgreSQL is an ORDBMS server whose primary function is to store data securely, and allows retrieval at the request of other software applications. Analyze and optimize your Postgres server by configuring our Postgres plugin and proactively monitor the availability and performance of business-critical Postgres database servers.

The plugin also monitors PostgreSQL clusters. Configure any one address of the cluster and the plugin discovers the remaining nodes, identifies the primary, and tracks replication health and failovers. Supported setups include streaming replication, Patroni, repmgr, pgpool-II, Citus, pg_auto_failover and logical replication.

Learn more https://www.site24x7.com/plugins/postgres-monitoring.html

## Quick installation

If you're using Linux servers, use the postgres plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/installer/Site24x7PostgresPluginInstaller.sh && sudo bash Site24x7PostgresPluginInstaller.sh
```

> **Note:** To upgrade from version 1, run the same command. The installer replaces the plugin files and keeps the existing `postgres.cfg`.

### Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.6 or higher.
- The psycopg2 module. The Site24x7 Linux agent includes it. On Windows, install it with:

		pip3 install psycopg2-binary

- PostgreSQL 9.6 or higher.
- A database user with the `pg_monitor` role. To monitor a cluster, create the user on every node with the same password.

	```sql
	CREATE USER site24x7 WITH PASSWORD 'site24x7';
	GRANT pg_monitor TO site24x7;
	```

> **Note:** Version 1 required the `pg_read_all_stats` role. When upgrading, grant `pg_monitor` to the existing user:
>
> ```sql
> GRANT pg_monitor TO <user>;
> ```

### Plugin Installation

- Create a directory named `postgres`.

	```bash
	mkdir postgres
	cd postgres/
	```

- Download all the files and place them under the `postgres` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/postgres.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/postgres.cfg
	```

- Execute the below command with appropriate arguments to check for the valid json output:

	```bash
	python3 postgres.py --host "localhost" --port "5432" --username "username" --password "password" --db "postgres"
	```

- Provide your Postgres DB configurations in the postgres.cfg file.

	```ini
	[postgres]
	host="localhost"
	port="5432"
	username="None"
	password="None"
	db="postgres"
	```

	To monitor a cluster, set `host` to any node, a VIP, a DNS name or an HAProxy port. To monitor more than one server from the same agent, add one section per server.

#### Linux

- Move the directory `postgres` under the Site24x7 Linux Agent plugin directory:

	```bash
	mv postgres /opt/site24x7/monagent/plugins/
	```

#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.
- Set `use_agent_python=0` in the `[global_configurations]` section of postgres.cfg.
- Move the folder `postgres` under the Site24x7 Windows Agent plugin directory:

	```bash
	C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
	```

The agent will automatically execute the plugin within five minutes and the user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Cluster Monitoring

| **Cluster Type** | **Configure host as** |
| :--- | :--- |
| Streaming replication | The primary, any standby, or a VIP |
| Patroni | Any node, with `patroni_port` set |
| repmgr | Any node |
| pgpool-II | The pgpool port |
| Citus | The coordinator |
| pg_auto_failover | The monitor node |
| Logical replication (native, pglogical, Spock, BDR) | Any node |

The role of each node is read from PostgreSQL. If a cluster manager reports a different role, the plugin raises it as a health issue.

## Configuration Options

| **Option** | **Description** |
| :--- | :--- |
| host, port | PostgreSQL server address. Default `localhost`, `5432`. |
| username, password | Monitoring user. |
| db | Database to connect to. Default `postgres`. |
| sslmode | `disable`, `require`, `verify-ca` or `verify-full`, with optional `sslrootcert`, `sslcert` and `sslkey`. |
| timeout | Connection timeout in seconds. Default `10`. |
| patroni_port | Patroni REST API port, usually `8008`. Required to use Patroni. |
| patroni_scheme, patroni_verify, patroni_cafile | HTTPS settings for the Patroni REST API. |
| patroni_certfile, patroni_keyfile | Client certificate for a Patroni API that requires one. |
| patroni_username, patroni_password | Basic authentication for a proxy in front of the Patroni API. |
| address_map | Maps node addresses reported by the cluster to addresses reachable from the agent. Example: `10.0.0.5:5432=192.168.1.5:6432`. |
| logs_enabled | Set to `true` to send cluster events to Site24x7 AppLogs. |
| log_type_name, log_file_path | AppLogs log type and file name. |

## Health Codes

| **Health Code** | **Description** |
| :--- | :--- |
| 0 | Healthy |
| 1 | A node is down or a standby is not streaming |
| 2 | No primary is reachable |
| 3 | More than one primary (split brain) |
| 4 | A cluster manager and PostgreSQL report different roles |

## PostgreSQL Server Monitoring Plugin Metrics

| **Metric Name** | **Description** |
| :--- | :--- |
| Uptime | Time since the server started |
| Server Version | PostgreSQL version |
| Node Role | Primary or standby |
| Active Connections | Number of connections to the databases |
| Max Connections | Maximum number of concurrent connections allowed |
| Connection Utilization | Active connections as a percentage of max connections |
| Idle Connections | Number of idle client connections |
| Active Queries | Number of client sessions running a query |
| Active Waiting Queries | Number of active queries waiting on an event |
| Long Running Queries | Number of queries running for more than 5 minutes |
| Longest Transaction | Age of the oldest open transaction |
| Blocked Sessions | Number of sessions waiting on a lock held by another session |
| Locks Count | Number of locks held or awaited |
| Waiting Locks | Number of lock requests not yet granted |
| Transactions Per Sec | Number of commits per second |
| Rollbacks Per Sec | Number of rollbacks per second |
| Buffer Cache Hit Percent | Percentage of block reads served from shared buffers |
| Index Hit Percent | Percentage of index block reads served from shared buffers |
| Database Count | Number of databases |
| Table Count | Number of tables in the configured database |
| Total Database Size | Total size of all databases |
| Rows Inserted / Updated / Deleted / Fetched / Returned Per Sec | Rows processed per second |
| Block Reads Per Sec | Disk blocks read per second |
| Index Scans Per Sec, Sequential Scans Per Sec | Scans of user tables per second |
| Temp Data Per Sec | Temporary file data written per second |
| Checkpoints Timed, Checkpoints Req | Number of scheduled and requested checkpoints |
| Checkpoint Write Time, Checkpoint Sync Time | Time spent writing and syncing checkpoint files |
| Buffers Checkpoint, Buffers Clean, Buffers Backend | Buffers written by checkpoints, the background writer and backends |
| Buffers Alloc | Number of buffers allocated |
| Dead Tuples, Live Tuples | Number of dead and live rows in user tables |
| Tables Never Vacuumed | Number of tables never vacuumed |
| Oldest Table Vacuum Age | Time since the least recently vacuumed table was vacuumed |
| Max XID Age, Max Multixact Age | Age of the oldest unfrozen transaction and multixact ID |
| XID Wraparound Percent | Max XID age as a percentage of `autovacuum_freeze_max_age` |
| WAL Generated Per Sec | WAL generated per second |
| WAL Files, WAL Directory Size | Number and size of WAL files |
| Archived Count, Archive Failed Count | Number of WAL files archived and failed |
| Last Archive Age | Time since the last successful archive |
| Archiving Failing | 1 if the last archive attempt failed |
| Archive Ready Files | Number of WAL files waiting to be archived |
| Checksum Failures | Number of data checksum failures |
| Collection Time | Time taken to collect the metrics |
| Failed Queries, Permission Gaps | Number of queries that failed or that the user is not permitted to run |

## Replication and Cluster Metrics

| **Metric Name** | **Description** |
| :--- | :--- |
| Cluster Type | Detected cluster type |
| Cluster Health, Health Code, Health Reason | Overall cluster status |
| Primary Node | Current primary node |
| Nodes Total, Nodes Up, Nodes Down | Number of known, reachable and unreachable nodes |
| Standbys Streaming, Sync Standbys | Number of standbys streaming from the primary, and synchronous standbys |
| Timeline | Current timeline, incremented at each promotion |
| Last Failover Age, Failovers 24h | Time since the last failover, and failovers in the last 24 hours |
| WAL Receiver Connected | 1 if the standby is streaming from its primary |
| Replay Lag, Replay Backlog | Replication delay and pending WAL on a standby |
| Max Standby Replay Lag, Max Standby Backlog | Highest replication delay and pending WAL across standbys |
| Replication Slots, Inactive Replication Slots | Number of replication slots, and slots not in use |
| Max Slot Retained WAL | Largest WAL volume retained by a slot |
| Subscriptions, Active Subscriptions | Number of logical subscriptions, and those running |
| Subscription Apply Errors, Subscription Sync Errors | Logical replication errors |

## Transactions and Sessions per Database

| **Metric Name** | **Description** |
| :--- | :--- |
| commits, rollbacks | Number of transactions committed and rolled back |
| conflicts | Number of queries cancelled due to recovery conflicts |
| sessions, sessions_abandoned, sessions_fatal, sessions_killed | Number of sessions by outcome |
| session_time, sessions_active_time, session_idle_in_transaction_time | Time spent in sessions |

## Stats per Database

| **Metric Name** | **Description** |
| :--- | :--- |
| active_connections | Number of connections to the database |
| size_in_mb | Size of the database |
| rows_inserted, rows_updated, rows_deleted, rows_fetched, rows_returned | Rows processed |
| block_reads, block_hits | Blocks read from disk and found in shared buffers |
| cache_hit_percent | Buffer cache hit percentage |
| deadlocks, temp_files | Number of deadlocks and temporary files |

## Other Tables

| **Table** | **Description** |
| :--- | :--- |
| Nodes | Role, status and replication lag of each cluster node |
| Replication_Links | Replication state and lag of each standby or subscriber |
| Replication_Slots | Replication slots and the WAL they retain |
| Events | Recent failovers and node changes |
| Wait_Events | Active sessions grouped by wait event |
| Top_Queries | Top 10 queries by total time, when `pg_stat_statements` is installed |

## Upgrading from Version 1

The following metrics are renamed or replaced in version 2:

| **Version 1** | **Version 2** |
| :--- | :--- |
| Cache Hit Ratio | Buffer Cache Hit Percent |
| Heap Blocks Read, Heap Blocks Hit | Total Block Reads, Total Block Hits |
| Index Rows Read, Index Rows Fetched | Index Scans |
| Tranasctions_and_Session_per_Database | Transactions_and_Sessions_per_Database |

Active Queries now counts client sessions only.
