# clickhouse monitoring

### Prerequisites
- Download and install the latest version of the Site24x7 agent on the server where you plan to run the plugin.
- Python 3 must be installed.
- Install the **clickhouse-driver** module for Python:

```bash
pip install clickhouse-driver
```

### Create a Dedicated User for Monitoring

#### Steps to Create and Grant Permissions

Log in to ClickHouse as an admin or a user with sufficient privileges:

   ```bash
   clickhouse-client -u default --password
```
Run the following SQL query to create a new user and grant the required privileges:

```sql
-- Create a new user for monitoring
CREATE USER <username> IDENTIFIED BY 'your_password';

-- Grant SELECT privileges on system tables (read-only access)
GRANT SELECT ON system.* TO <username>;
```

## Installation

- Create a directory named `clickhouse`:

```bash
mkdir clickhouse
cd clickhouse/
```
### Download Plugin Script

Download the plugin `clickhouse.py`, `clickhouse.cfg` and place it under the `clickhouse` directory:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/clickhouse/clickhouse.py
sed -i "1s|^.*|#! $(which python3)|" clickhouse.py

wget https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/clickhouse/clickhouse.cfg
```
### Execute Plugin

Run the below command with appropriate arguments to check for valid JSON output:

```bash
python3 clickhouse.py --host "localhost" --port "9000" --username "default" --password "" --database "default"
```
### Move Plugin to Agent Directory

#### For Linux:

Place the `clickhouse` folder under the Site24x7 Linux Agent plugin directory:

```bash
mv clickhouse /opt/site24x7/monagent/plugins
```
#### For Windows:

Since it’s a Python plugin, follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers) to run Python plugins on Windows. 

Move the `clickhouse` folder into the Site24x7 Windows Agent plugin directory:

```powershell
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
```
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Metrics Captured

Name                                | Description
---                                 | ---
CompiledExpressionCacheCount         | Number of compiled expressions cached for query execution. Helps speed up repeated query computations.
FailedQuery                          | Total number of queries that failed during execution. Indicates issues or errors in query processing.
FailedSelectQuery                     | Total number of SELECT queries that failed. Helps identify problems specifically with SELECT statements.
Inserted rows                         | Total number of rows inserted into tables. Shows the amount of new data being added.
InsertedBytes                         | Total bytes inserted into tables. Measures the data volume inserted in the database.
MarkCacheBytes                         | Memory used for storing marks in MarkCache. Optimizes reading data from MergeTree tables.
MarkCacheFiles                         | Number of files cached in MarkCache. Helps reduce disk I/O during queries.
Max parts for partition                 | Maximum number of parts for a single partition in MergeTree tables. Indicates table fragmentation.
Merges running                          | Number of merges currently running. Helps monitor background merge operations in MergeTree tables.
MergesTimeMilliseconds                  | Total time spent on merges in milliseconds. Measures the performance cost of merges.
NetworkReceiveElapsedMicroseconds       | Time spent receiving data from the network in microseconds. Monitors network latency for data reception.
NetworkSendElapsedMicroseconds          | Time spent sending data over the network in microseconds. Monitors network latency for data sending.
Queries running                          | Number of currently running queries. Shows current database workload.
Queries/second                           | Number of queries executed per second. Measures query throughput.
Query                                    | Current active query count. Helps monitor database activity at a glance.
SelectQuery                              | Total number of SELECT queries executed. Measures read/query load on the server.
Selected bytes/second                     | Number of bytes read per second during queries. Indicates data read throughput.
Total MergeTree parts                     | Total parts present in all MergeTree tables. Reflects table storage fragmentation.
UncompressedCacheBytes                    | Memory used by uncompressed cache. Helps speed up data access without decompressing repeatedly.

## Database
Name                                | Description
---                                 | ---
NumberOfDatabases                    | Total number of databases in ClickHouse. Helps monitor how many databases are being managed.
NumberOfTables                       | Total number of tables in ClickHouse. Indicates the volume of data structures present.
ReplicasMaxQueueSize                  | Maximum size observed in replication queues. Shows the heaviest replication load.
ReplicasSumInsertsInQueue             | Total number of inserts currently in all replication queues. Helps track replication backlog.
ReplicasSumMergesInQueue              | Total number of merges currently in all replication queues. Monitors replication operations pending merges.
ReplicasMaxRelativeDelay              | Maximum relative replication delay observed among replicas. Measures replication lag in relative terms.
ReplicasMaxMergesInQueue              | Maximum number of merges waiting in any replication queue. Shows peak merge backlog for replicas.
ReplicasMaxInsertsInQueue             | Maximum number of inserts waiting in any replication queue. Indicates peak insert backlog.
ReplicasSumQueueSize                  | Sum of all replication queue sizes across replicas. Monitors overall replication queue load.
ReplicasMaxAbsoluteDelay              | Maximum absolute replication delay observed among replicas. Helps track the worst-case replication lag.

## Memory
Name                                    | Description
---                                     | ---
MemoryResident                          | Amount of physical memory currently used by ClickHouse. Shows how much RAM is actively being consumed.
MemoryVirtual                           | Total virtual memory allocated by ClickHouse. Helps track overall memory footprint including swap.
MemoryShared                            | Amount of memory shared with other processes. Indicates shared resource usage.
Memory (tracked)                         | Memory tracked internally by ClickHouse. Useful for monitoring memory used by internal structures.
jemalloc.allocated                       | Memory allocated by jemalloc allocator. Helps monitor memory usage by ClickHouse processes.
jemalloc.retained                        | Memory retained by jemalloc but not currently used. Shows potential memory overhead.
jemalloc.resident                        | Resident memory managed by jemalloc. Reflects physical memory actually in use.
jemalloc.background_thread.num_threads   | Number of jemalloc background threads running. Indicates memory management activity.
jemalloc.arenas.all.dirty_purged         | Total memory purged from dirty jemalloc arenas. Helps reclaim unused memory.
Uptime                                   | Total uptime of ClickHouse server in seconds. Useful for monitoring server stability and availability.

## Events
Name                                | Description
---                                 | ---
CompressedReadBufferBlocks           | Number of blocks read from compressed buffers. Shows how much data is read in compressed form.
CompressedReadBufferBytes            | Total bytes read from compressed buffers. Measures the volume of compressed data processed.
ContextLock                          | Number of times ClickHouse contexts are locked. Helps monitor concurrency and thread contention.
DiskReadElapsedMicroseconds          | Time spent reading data from disk in microseconds. Indicates disk I/O performance.
DiskWriteElapsedMicroseconds         | Time spent writing data to disk in microseconds. Measures disk write latency.
FileOpen                             | Number of files currently opened by ClickHouse. Helps monitor file descriptor usage.
ReadCompressedBytes                   | Total bytes read in compressed form from storage. Shows efficiency of compressed data reads.
Merge                                | Total number of merge operations executed. Indicates background merges in MergeTree tables.
RWLockAcquiredReadLocks               | Number of read locks acquired on RWLocks. Shows read concurrency activity.
RWLockReadersWaitMilliseconds         | Time readers waited for acquiring RWLocks in milliseconds. Indicates read lock contention.
SoftPageFaults                        | Number of soft page faults occurred. Shows memory paging activity without disk access.

## System
Name                                | Description
---                                 | ---
ReplicatedFetch                     | Number of fetch operations from replicas. Helps track replication reads.
ReplicatedSend                      | Number of data blocks sent to replicas. Monitors replication writes.
ReplicatedChecks                    | Number of consistency checks performed on replicas. Ensures data integrity.
MySQLConnection                     | Number of active MySQL connections. Useful if ClickHouse connects to MySQL sources.
PostgreSQLConnection                | Number of active PostgreSQL connections. Useful if ClickHouse connects to PostgreSQL sources.
OpenFileForRead                     | Number of files opened for reading. Monitors file descriptor usage for read operations.
OpenFileForWrite                    | Number of files opened for writing. Monitors file descriptor usage for write operations.
Read                                | Total read operations performed. Tracks overall read activity.
Write                               | Total write operations performed. Tracks overall write activity.
ReadonlyReplica                      | Number of read-only replicas. Indicates replication configuration.
ZooKeeperSession                     | Number of active ZooKeeper sessions. Shows coordination status with ZooKeeper.
ZooKeeperRequest                     | Number of requests sent to ZooKeeper. Helps monitor ZooKeeper activity.
DelayedInserts                        | Number of inserts delayed for background processing. Tracks insert backlog.
ContextLockWait                       | Time spent waiting for context locks. Monitors thread contention.
StorageBufferRows                      | Number of rows in the storage buffer. Indicates buffering activity for writes.
RWLockWaitingReaders                   | Number of readers waiting for RWLocks. Shows read contention.
RWLockWaitingWriters                   | Number of writers waiting for RWLocks. Shows write contention.
OS CPU Usage (userspace)               | CPU usage in userspace. Monitors CPU consumed by application code.
OS CPU Usage (kernel)                  | CPU usage in kernel mode. Monitors CPU consumed by OS operations.
CPU usage (cores)                      | Number of CPU cores currently utilized. Tracks overall CPU utilization.
IO wait                                | Time CPU waits for I/O operations to complete. Indicates I/O bottlenecks.
CPU wait                               | Time threads wait for CPU availability. Measures CPU contention.
Read from disk                          | Number of reads from disk. Tracks disk I/O activity.
Read from filesystem                     | Number of reads from the filesystem cache. Indicates cached read efficiency.
clickhouse_rss_bytes                     | Resident Set Size in bytes for ClickHouse. Shows memory currently used in RAM.

## Sample Image:

<img width="1636" height="861" alt="image" src="https://github.com/user-attachments/assets/a7676e43-569a-434c-8fbb-6fcc30df5f38" />


