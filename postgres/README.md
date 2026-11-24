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

Metrics are grouped by the tab they appear in. "Per Sec" metrics are averaged over the poll interval, and "New" metrics count what happened since the previous poll.

### Summary

| **Metric Name** | **Description** |
| :--- | :--- |
| Uptime | Time since the server started |
| Active Connections | Number of connections to the databases |
| Connection Utilization | Active connections as a percentage of max connections |
| Transactions Per Sec | Number of commits per second |
| Buffer Cache Hit Percent | Percentage of block reads served from shared buffers |
| Cluster Health | 0 healthy, 1 warning, 2 critical (see Health Codes) |
| Nodes Up | Number of reachable cluster nodes |
| Collection Time | Time taken to collect the metrics |
| Failed Queries | Number of queries that failed in this poll |
| Permission Gaps | Number of queries the monitoring user is not permitted to run |

### Cluster

| **Metric Name** | **Description** |
| :--- | :--- |
| Cluster Type | Detected cluster type |
| Health Code, Health Reason | Cluster status and its cause (see Health Codes) |
| Primary Node | Current primary node |
| Nodes Total, Nodes Down | Number of known nodes, and nodes that are down or not streaming |
| Standbys Streaming, Sync Standbys | Number of standbys streaming from the primary, and synchronous standbys |
| Timeline | Current timeline, incremented at each promotion |
| Last Failover Age | Time since the last failover |
| Failovers 24h | Number of failovers in the last 24 hours |

### Replication

| **Metric Name** | **Description** |
| :--- | :--- |
| WAL Receiver Connected | 1 if the standby is streaming from its primary |
| Replay Lag | Replication delay on a standby |
| Replay Backlog | WAL received by a standby but not yet replayed |
| Last WAL Message Age | Time since a standby last heard from its primary |
| Max Standby Replay Lag, Max Standby Backlog | Highest replication delay and backlog across standbys |
| Replication Slots, Inactive Replication Slots | Number of replication slots, and slots not in use |
| Max Slot Retained WAL | Largest WAL volume retained by a slot |
| Subscriptions, Active Subscriptions | Number of logical subscriptions, and those running |
| Last Subscription Message Age | Time since a subscription last heard from its publisher |
| Subscription Apply Errors, Subscription Sync Errors | Logical replication errors |

### Activity

| **Metric Name** | **Description** |
| :--- | :--- |
| Server Version | PostgreSQL version |
| Node Role | Primary or standby |
| Max Connections | Maximum number of concurrent connections allowed |
| Active Queries | Number of client sessions running a query |
| Active Waiting Queries | Number of active queries waiting on an event |
| Idle Connections | Number of idle client connections |
| Long Running Queries | Number of queries running for more than 5 minutes |
| Longest Transaction | Age of the oldest open transaction |
| Blocked Sessions | Number of sessions waiting on a lock held by another session |
| Locks Count | Number of locks held or awaited |
| Waiting Locks | Number of lock requests not yet granted |

### Transactions and Sessions

| **Metric Name** | **Description** |
| :--- | :--- |
| Total Commits, Total Rollbacks | Number of transactions committed and rolled back |
| Rollbacks Per Sec | Number of rollbacks per second |
| Transactions Open | Number of sessions with an open transaction |
| Transactions Idle In Transaction | Number of sessions idle inside an open transaction |
| New Deadlocks | Number of deadlocks |
| New Conflicts | Number of queries cancelled due to recovery conflicts |
| Total Sessions, Total Sessions Abandoned, Total Sessions Fatal, Total Sessions Killed | Number of sessions by outcome (PostgreSQL 14+) |

### DB and IO stats

| **Metric Name** | **Description** |
| :--- | :--- |
| Database Count | Number of databases |
| Table Count | Number of tables in the configured database |
| Total Database Size | Total size of all databases |
| Rows Inserted / Updated / Deleted / Fetched / Returned Per Sec | Rows processed per second |
| Block Reads Per Sec | Disk blocks read per second |
| Total Block Hits | Number of blocks found in shared buffers |
| Index Scans Per Sec, Sequential Scans Per Sec | Scans of user tables per second |
| Index Hit Percent | Percentage of index block reads served from shared buffers |
| Total Temp Files | Number of temporary files written by queries |
| Temp Data Per Sec | Temporary file data written per second |
| New Checksum Failures | Number of data checksum failures (PostgreSQL 12+) |

### Vacuum and Wraparound

| **Metric Name** | **Description** |
| :--- | :--- |
| Dead Tuples, Live Tuples | Number of dead and live rows in user tables |
| Tables Never Vacuumed | Number of tables never vacuumed |
| Oldest Table Vacuum Age | Time since the least recently vacuumed table was vacuumed |
| Max XID Age, Max Multixact Age | Age of the oldest unfrozen transaction and multixact ID |
| XID Wraparound Percent | Max XID age as a percentage of `autovacuum_freeze_max_age` |

### WAL and Archiving

| **Metric Name** | **Description** |
| :--- | :--- |
| WAL Generated Per Sec | WAL generated per second |
| WAL Files, WAL Directory Size | Number and size of WAL files |
| New WAL Buffers Full | Number of times WAL buffers filled up (PostgreSQL 14+) |
| Archived Count | Number of WAL files archived |
| New Archive Failures | Number of failed archive attempts |
| Last Archive Age | Time since the last successful archive |
| Archiving Failing | 1 if the last archive attempt failed |
| Archive Ready Files | Number of WAL files waiting to be archived (PostgreSQL 12+) |

### BG Writer

| **Metric Name** | **Description** |
| :--- | :--- |
| Checkpoints Timed | Number of scheduled checkpoints |
| New Requested Checkpoints | Number of checkpoints requested before their schedule |
| Checkpoint Write Time, Checkpoint Sync Time | Time spent writing and syncing checkpoint files |
| Buffers Checkpoint, Buffers Clean, Buffers Backend | Buffers written by checkpoints, the background writer and backends |
| Buffers Backend Fsync | Number of fsync calls made by backends (up to PostgreSQL 16) |
| Buffers Alloc | Number of buffers allocated |
| Maxwritten Clean | Number of times the background writer stopped for writing too many buffers |

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

The following version 1 metrics are no longer sent. The second column lists the nearest version 2 metric, which is measured differently, so its values are not directly comparable:

| **Version 1** | **Version 2** |
| :--- | :--- |
| Cache Hit Ratio | Buffer Cache Hit Percent |
| Heap Blocks Read, Heap Blocks Hit | Block Reads Per Sec, Total Block Hits |
| Index Rows Read, Index Rows Fetched | Index Scans Per Sec |
| Total Rows Inserted, Updated, Deleted, Fetched, Returned | Rows Inserted, Updated, Deleted, Fetched, Returned Per Sec |
| Total Block Reads | Block Reads Per Sec |
| Index Scans | Index Scans Per Sec |
| Total Conflicts | New Conflicts |
| Checkpoints Req | New Requested Checkpoints |

The table `Tranasctions_and_Session_per_Database` is renamed `Transactions_and_Sessions_per_Database`. Active Queries now counts client sessions only.
