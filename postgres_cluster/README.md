# Plugin for PostgreSQL Cluster Monitoring

PostgreSQL Cluster monitoring plugin provides **cluster-level visibility** including replication health, WAL activity, checkpoints, connection usage, and recovery conflicts — all in one place.

### This plugin is designed to monitor **Primary and Standby nodes together as a cluster**, giving deep insights into replication status and overall system performance across your entire PostgreSQL setup.
---

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) on the server where you plan to run the plugin.
- Python 3 or higher.
- Install the required Python library:

```bash
pip3 install psycopg2-binary
```

---

## Plugin Installation

### Step 1 — Create the plugin directory

```bash
mkdir postgres_cluster
cd postgres_cluster/
```

### Step 2 — Download the plugin files

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres_cluster/postgres_cluster.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres_cluster/postgres_cluster.cfg
```

### Step 3 — Grant the required database permissions

Ensure the monitoring user has the necessary roles. For example, to grant permissions to the user `admin`:

```sql
GRANT pg_read_all_settings TO admin;
GRANT pg_monitor TO admin;
```

### Step 4 — Configure the plugin

Edit `postgres_cluster.cfg` and provide your PostgreSQL cluster details:

```ini
[global_configurations]
use_agent_python = 1

[pg_primary]
host = hostname
port = 5433
username = user name
password = password

[pg_replica]
host = hostname
port = 5433
username = user name
password = password
```

### Step 5 — Test the plugin

Run the following command to verify the plugin produces valid output before deployment:

```bash
 python3 postgres_cluster.py  --host "localhost" --port "5432" --username "username" --password "password"
```

---

## Deploying the Plugin

### Linux

Follow [this guide](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the plugin script, then move the directory to the Site24x7 agent plugin folder:

```bash
mv postgres_cluster /opt/site24x7/monagent/plugins/
```

### Windows

Since this is a Python plugin, follow [these steps](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers) to configure Python plugins on Windows. Then move the folder to the Site24x7 Windows agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```

The agent will automatically execute the plugin within five minutes. You can view the monitor under:

**Site24x7 → Plugins → Plugin Integrations**

---

# PostgreSQL Metrics Reference

---

## Cluster Configuration Metrics

| **Metric Name** | **Description** |
|---|---|
| Max Connections | The maximum number of concurrent client connections allowed to the PostgreSQL server, as set by the `max_connections` configuration parameter. |
| Superuser Reserved Connections | The number of connection slots reserved exclusively for superuser access, as configured by `superuser_reserved_connections`, ensuring administrators can always connect even when the server is at capacity. |

---

## Cluster Identity & Status Metrics

| **Metric Name** | **Description** |
|---|---|
| Cluster Name | The name assigned to the PostgreSQL cluster, used to identify and group the primary and replica nodes being monitored. |
| Cluster Status | The current overall health status of the cluster, reflecting whether replication and node connectivity are operating normally. |
| PostgreSQL Version | The full version string of the PostgreSQL server software currently installed and running on the node. |
| Timeline ID | The current WAL timeline identifier of the PostgreSQL instance, which increments each time a failover or point-in-time recovery occurs, helping track the history of the cluster's recovery events. |

---

## Node Information Metrics

| **Metric Name** | **Description** |
|---|---|
| Is In Recovery | Indicates whether the current node is operating in recovery mode, which is true for standby/replica nodes that are replaying WAL from the primary. |
| Node Role | The role of the monitored node within the cluster, either Primary (accepting writes) or Replica (read-only standby). |
| Replica Count | The total number of standby/replica nodes currently connected and replicating from the primary node. |
| Replication State | The current state of the replication stream, such as `streaming`, `catchup`, or `disconnected`, indicating the health of the replication connection. |
| Server PID | The operating system process ID of the PostgreSQL server's postmaster process. |
| Server Uptime | The total elapsed time since the PostgreSQL server was last started, indicating how long it has been running without a restart. |
| Sync State | The replication synchronization mode for the standby, either `sync` (the primary waits for the replica to confirm WAL receipt) or `async` (the primary does not wait). |

---

## Replication Lag Metrics

| **Metric Name** | **Description** |
|---|---|
| Replication Lag | The total delay between the primary node writing WAL data and the replica applying it, representing the overall end-to-end replication latency. |
| Write Lag | The elapsed time between the primary flushing a WAL record to disk and receiving confirmation that the standby has written it to its own WAL file, but not yet flushed or applied it. |
| Flush Lag | The elapsed time between the primary flushing a WAL record and receiving confirmation that the standby has flushed it to durable storage, but not yet replayed it into the database. |
| Replay Lag | The elapsed time between the primary flushing a WAL record and receiving confirmation that the standby has fully replayed (applied) it to its database state. |

---

## Replication Slot Metrics

| **Metric Name** | **Description** |
|---|---|
| Replication Slot Count | The total number of replication slots currently defined on the PostgreSQL instance, including both active and inactive slots. |
| Active Replication Slots | The number of replication slots that currently have an active consumer (e.g., a replica or logical subscriber) connected and consuming WAL data. |
| Inactive Replication Slots | The number of replication slots with no active consumer connected, which may cause WAL accumulation and disk pressure if left unattended. |
| Slot Lag | The amount of WAL data (in bytes) retained on the primary due to replication slots, representing how far behind the slowest slot consumer is from the current WAL position. |
| Physical Slots | The number of physical replication slots defined, used by streaming standby replicas to ensure the primary retains the WAL segments they need. |
| Logical Slots | The number of logical replication slots defined, used by logical replication subscribers or tools like pglogical and Debezium to decode and stream row-level changes. |

---

## WAL Archive Metrics

| **Metric Name** | **Description** |
|---|---|
| Archive Status Success | The cumulative count of WAL segment files that have been successfully archived by the `archive_command` since the server started. |
| Archive Status Failed | The cumulative count of WAL segment archiving attempts that have failed, indicating issues with the `archive_command` or the archive destination. |
| Last Archived WAL File | The name of the most recently archived WAL segment file, useful for confirming that archiving is progressing and identifying the last known safe recovery point. |
| Archive Ready Files Count | The number of WAL segment files in `pg_wal/archive_status/` that are ready to be archived but have not yet been processed, indicating archiving backlog. |

---

## WAL Metrics

| **Metric Name** | **Description** |
|---|---|
| Current WAL LSN | The current Log Sequence Number (LSN) representing the latest write position in the WAL stream on the primary node. |
| WAL Insert LSN | The LSN up to which WAL records have been inserted into the WAL buffers in memory, which may be ahead of what has been flushed to disk. |
| WAL Flush LSN | The LSN up to which WAL data has been durably flushed to disk, ensuring that all records up to this point survive a server crash. |
| WAL Files Count | The total number of WAL segment files currently present in the `pg_wal` directory, reflecting the volume of unarchived or retained WAL data. |
| WAL Total Size | The total disk space consumed by WAL segment files in the `pg_wal` directory, useful for monitoring storage usage and detecting unusual WAL growth. |

---

## Checkpoint Metrics

| **Metric Name** | **Description** |
|---|---|
| Checkpoints Timed | The number of checkpoints that were triggered automatically by the `checkpoint_timeout` interval, indicating routine scheduled checkpoint activity. |
| Checkpoints Requested | The number of checkpoints that were requested explicitly (e.g., due to `max_wal_size` being reached), which may indicate the system is under heavy write load. |
| Checkpoint Write | The total time (in milliseconds) spent writing dirty buffers to disk during checkpoint operations, contributing to overall checkpoint duration. |
| Checkpoint Sync | The total time (in milliseconds) spent syncing files to disk (via `fsync`) during checkpoints, ensuring data durability after write completion. |
| Buffers Checkpoint | The total number of shared buffers written to disk specifically during checkpoint operations since the last statistics reset. |

---

## Buffer Metrics

| **Metric Name** | **Description** |
|---|---|
| Buffers Clean | The number of dirty buffers written to disk by the background writer process during its regular cleaning passes, outside of checkpoint operations. |
| Buffers Backend Direct Writes | The number of buffers written directly by backend processes rather than the background writer or checkpointer, which may indicate the background writer is not keeping up. |
| Buffers Allocated | The total number of shared memory buffers allocated since the last statistics reset, reflecting buffer pool usage and cache pressure. |
| Maxwritten Clean | The number of times the background writer stopped its cleaning scan early because it had written the maximum number of buffers allowed per round (`bgwriter_lru_maxpages`). |

---

## WAL Receiver Metrics

| **Metric Name** | **Description** |
|---|---|
| WAL Receiver Status | The current operational status of the WAL receiver process on the standby node, indicating whether it is actively streaming, stopped, or in an error state. |
| Last Received LSN | The LSN of the last WAL byte received by the standby's WAL receiver from the primary, showing how current the received WAL stream is. |
| Last Replayed LSN | The LSN of the last WAL record that has been replayed (applied) to the standby's database, reflecting the actual data consistency point of the replica. |
| Replay Lag Time | The time elapsed since the last WAL record was replayed on the standby, providing a human-readable measure of how stale the replica's data is. |
| Receive Apply Lag | The gap between the last received LSN and the last replayed LSN on the standby, indicating how much received WAL is still pending application to the database. |

---

## Connection Metrics

| **Metric Name** | **Description** |
|---|---|
| Active Connections | The current number of client connections actively connected to the PostgreSQL server, including idle, active, and waiting connections. |
| Available Connections | The number of remaining connection slots available for new client connections, calculated as `max_connections` minus currently used connections and superuser reserved slots. |
| Connection Utilization Percent | The percentage of total available connection slots currently in use, helping to identify when the server is approaching its connection limit. |

---

## Conflict & Transaction Metrics

| **Metric Name** | **Description** |
|---|---|
| Recovery Conflicts Total | The cumulative total number of queries cancelled on the standby due to any type of recovery conflict with WAL replay operations, aggregating all individual conflict types. |
| Conflicts Tablespace | The number of queries cancelled on the standby due to a conflict with a tablespace drop operation being replayed from the primary's WAL stream. |
| Conflicts Lock | The number of queries cancelled on the standby due to a lock conflict arising from WAL replay, where a replayed operation required a lock held by a running query. |
| Conflicts Snapshot | The number of queries cancelled on the standby because their snapshot became too old due to WAL replay advancing the database state beyond what the query could see. |
| Conflicts Buffer Pin | The number of queries cancelled on the standby because WAL replay needed to update a page that was being held (pinned) in a buffer by a running query. |
| Conflicts Deadlock | The number of queries cancelled on the standby as a result of a deadlock detected during WAL replay operations. |
| Oldest Running Transaction Age | The age (in transaction IDs or elapsed time) of the oldest currently active transaction on the server, useful for detecting long-running transactions that may cause table bloat or replication conflicts. |


<img width="1480" height="716" alt="Screenshot (722)" src="https://github.com/user-attachments/assets/983f0b00-697b-4df3-8789-fdd0b0a7790c" />
