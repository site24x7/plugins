# Aerospike Monitoring

Install and configure the Aerospike plugin to monitor the performance, availability, and health of your Aerospike database clusters. Keep a pulse on cluster status, node metrics, namespace usage, and system resource consumption to ensure optimal performance of your Aerospike environment.

---

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python version 3 or higher.
- Install the **aerospike** Python client module:

```bash
pip3 install aerospike
```

---

## Create a Monitoring User (Optional — Enterprise Edition Only)

Authentication is only required if **security is enabled** on your Aerospike server (Enterprise Edition with the `security {}` stanza in the configuration).

If security is **not enabled** (Community Edition or Enterprise without `security {}`), the plugin works without any credentials — you can skip this section.

### Privileges Required

Aerospike `info` commands (used by this plugin) require **zero roles** — only a valid authenticated user is needed. No `read`, `write`, or `admin` privileges are required.

### Steps to Create a Monitoring User

#### Using the prerequisites script

Run the included prerequisites script that will check if security is enabled and create a monitoring user if needed:

```bash
bash prerequisites/prerequisites.sh
```

#### Manual setup using asadm

Connect to your Aerospike server using `asadm` with admin credentials:

```bash
asadm -h <host> -p <port> -U <admin_user> -P <admin_password> --enable
```

Run the following command to create a monitoring user:

```
manage acl create user <monitoring_username> password <monitoring_password>
```

> **Note:** No roles or grants are needed. The user only needs to authenticate — Aerospike `info` commands are accessible to any authenticated user.

---

## Installation

### Plugin Installation

- Create a directory named `aerospike_monitoring`:

```bash
mkdir aerospike_monitoring
cd aerospike_monitoring/
```

- Download the plugin files and place them under the `aerospike_monitoring` directory:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/aerospike_monitoring/aerospike_monitoring.py && sed -i "1s|^.*|#! $(which python3)|" aerospike_monitoring.py

wget https://raw.githubusercontent.com/site24x7/plugins/master/aerospike_monitoring/aerospike_monitoring.cfg
```

- Execute the below command with appropriate arguments to check for valid JSON output:

```bash
python3 aerospike_monitoring.py --hostname "localhost" --port "3000" --username "None" --password "None"
```

For TLS-enabled connections:

```bash
python3 aerospike_monitoring.py --hostname "localhost" --port "4000" --tls_enable "true" --tls_name "aerospike-tls" --cafile "/path/to/ca.pem" --ssl_verify "true" --username "None" --password "None"
```

### Configurations

Provide your Aerospike configurations in the `aerospike_monitoring.cfg` file.

```ini
[aerospike_monitoring]
hostname = "localhost"
port = "3000"
tls_enable = "false"
tls_name = "None"
cafile = "None"
ssl_verify = "false"
username = "None"
password = "None"
```

> **Note:** Set `username` and `password` to `"None"` if security is not enabled on the server.

### Move the plugin under the Site24x7 agent directory

#### Linux

Move the `aerospike_monitoring` directory under the Site24x7 Linux Agent plugin directory:

```bash
mv aerospike_monitoring /opt/site24x7/monagent/plugins/
```

#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Move the `aerospike_monitoring` folder under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---

## Metrics Captured

### Summary

| Metric Name                       | Description                                                                                              |
|-----------------------------------|----------------------------------------------------------------------------------------------------------|
| Client Connections                | Number of active client connections currently open to the Aerospike server.                               |
| Cluster Size                      | Total number of nodes currently participating in the cluster.                                             |
| Read Write In Progress            | Number of read and write transactions currently being processed by the server.                            |
| Process CPU                       | CPU percentage consumed exclusively by the Aerospike server process.                                     |
| Cluster Generation                | Cluster generation counter that increments each time the cluster membership changes (node joins/leaves).  |
| Cluster Clock Skew                | Maximum time difference between clocks of nodes in the cluster, measured in minutes.                     |
| Cluster Clock Skew Stop Writes    | Configured maximum clock skew threshold in minutes; writes are stopped if skew exceeds this value.       |
| Long Queries Active               | Number of long-running queries (scans or queries) currently being executed on the server.                |
| Cluster Integrity                 | Indicates whether all partitions in the cluster have the correct number of replicas (`true` / `false`).  |
| Cluster Is Member                 | Indicates whether this node is an active member of the cluster (`true` / `false`).                       |
| Migrate Allowed                   | Indicates whether partition data migration between nodes is currently allowed (`true` / `false`).        |
| Failed Best Practices             | Indicates whether the node configuration violates any Aerospike recommended best practices (`true` / `false`). |
| Threads Pool Total                | Total number of transaction processing threads configured in the thread pool.                            |
| Uptime                            | Time in minutes since the Aerospike server process was started.                                          |
| Cluster Key                       | Unique identifier for the current cluster state; changes whenever cluster membership changes.             |
| Time Since Rebalance              | Time in minutes since the last partition rebalance (data redistribution) completed.                      |

### System Performance

| Metric Name                  | Description                                                                                              |
|------------------------------|----------------------------------------------------------------------------------------------------------|
| Heap Efficiency              | Ratio of heap memory allocated to heap memory mapped, shown as a percentage. Higher values indicate less memory waste. |
| Heap Allocated               | Total heap memory currently allocated by the Aerospike process, measured in megabytes.                   |
| Heap Active                  | Heap memory actively being used by the Aerospike process, measured in megabytes.                         |
| Heap Mapped                  | Total heap memory mapped (reserved from the OS) by the Aerospike process, measured in megabytes.         |
| Threads Pool Active          | Number of threads in the thread pool that are currently actively processing transactions.                |
| Threads Detached             | Number of detached background threads used internally by the Aerospike process.                           |
| Threads Joinable             | Number of joinable threads used internally by the Aerospike process.                                     |

### Connections

| Metric Name                  | Description                                                                                              |
|------------------------------|----------------------------------------------------------------------------------------------------------|
| Client Connections Opened    | Cumulative count of client connections opened since the server started.                                   |
| Client Connections Closed    | Cumulative count of client connections closed since the server started.                                   |
| Admin Connections            | Number of active admin/management connections (asadm, asinfo) currently open to the server.               |
| Admin Connections Opened     | Cumulative count of admin connections opened since the server started.                                    |
| Admin Connections Closed     | Cumulative count of admin connections closed since the server started.                                    |
| Heartbeat Connections        | Number of active heartbeat connections used for cluster node-to-node health checks.                      |
| Heartbeat Connections Opened | Cumulative count of heartbeat connections opened since the server started.                                |
| Heartbeat Connections Closed | Cumulative count of heartbeat connections closed since the server started.                                |
| Fabric Connections           | Number of active fabric connections used for intra-cluster data replication and migration.                |
| Fabric Connections Opened    | Cumulative count of fabric connections opened since the server started.                                   |
| Fabric Connections Closed    | Cumulative count of fabric connections closed since the server started.                                   |

### Operations

| Metric Name                       | Description                                                                                          |
|-----------------------------------|------------------------------------------------------------------------------------------------------|
| Batch Index Complete              | Cumulative count of batch read requests that completed successfully.                                 |
| Batch Index Error                 | Cumulative count of batch read requests that failed due to errors.                                   |
| Batch Index Timeout               | Cumulative count of batch read requests that timed out before completion.                            |
| Proxy In Progress                 | Number of requests currently being proxied to another node that owns the target partition.            |
| Objects                           | Total number of records (objects) currently stored on this node across all namespaces.                |
| Tombstones                        | Total number of tombstone records on this node. Tombstones are markers for deleted records that prevent resurrection during replication. |
| Migrate Partitions Remaining      | Number of data partitions still pending migration to or from this node during a cluster rebalance.   |
| Demarshal Error                   | Cumulative count of errors that occurred while deserializing incoming client request messages.        |
| Early Transaction Service Error   | Cumulative count of transaction errors that occurred before the request reached the transaction processing queue. |
| Reaped File Descriptors           | Cumulative count of idle client connection file descriptors that were closed (reaped) by the server. |
| Info Requests Complete            | Cumulative count of info protocol requests (metadata/stats queries) completed by the server.         |
| Fabric Read Write Receive Rate    | Rate of read/write data replication messages received from other nodes via the fabric network.        |
| Fabric Read Write Send Rate       | Rate of read/write data replication messages sent to other nodes via the fabric network.              |
| Deprecated Requests               | Cumulative count of API requests using deprecated features or protocols.                             |
| Tree GC Queue                     | Number of index tree garbage collection items pending cleanup. High values indicate index cleanup is falling behind. |

### Nodes

Per-node metrics are automatically discovered for all nodes in the cluster.

| Metric Name                  | Description                                                                                          |
|------------------------------|------------------------------------------------------------------------------------------------------|
| Client Connections           | Number of active client connections on this specific node.                                            |
| Process CPU                  | CPU percentage consumed by the Aerospike process on this specific node.                               |
| Heap Efficiency              | Heap memory efficiency (allocated vs mapped ratio) on this specific node.                             |
| Read Write In Progress       | Number of read/write transactions currently being processed on this specific node.                    |
| Objects                      | Total number of records stored on this specific node.                                                 |
| Tombstones                   | Total number of tombstone (deleted record markers) on this specific node.                             |
| Batch Index Error            | Cumulative count of failed batch read requests on this specific node.                                 |
| Migrate Partitions Remaining | Number of partitions still pending migration on this specific node.                                   |
| Long Queries Active          | Number of long-running queries currently being executed on this specific node.                        |
| Demarshal Error              | Cumulative count of message deserialization errors on this specific node.                              |

### Namespaces

Per-namespace metrics are automatically discovered for all namespaces across the cluster.

| Metric Name                              | Description                                                                                  |
|------------------------------------------|----------------------------------------------------------------------------------------------|
| Objects                                  | Total number of records currently stored in this namespace.                                   |
| Master Objects                           | Number of primary (master copy) records stored in this namespace on the connected node.       |
| Dead Partitions                          | Number of partitions in this namespace that have lost all copies and are unrecoverable.       |
| Unavailable Partitions                   | Number of partitions in this namespace that are temporarily inaccessible due to node failures.|
| Client Read Error                        | Cumulative count of client read operations that failed in this namespace.                     |
| Client Write Error                       | Cumulative count of client write operations that failed in this namespace.                    |
| Client Delete Error                      | Cumulative count of client delete operations that failed in this namespace.                   |
| Client UDF Error                         | Cumulative count of client User Defined Function (UDF) execution errors in this namespace.    |
| Expired Objects                          | Cumulative count of records removed due to TTL (Time-To-Live) expiration in this namespace.   |
| Data Used                                | Percentage of storage space currently used by data in this namespace.                         |
| Data Avail                               | Percentage of storage space still available for data in this namespace.                       |
| Primary Index Query Aggregation Error    | Cumulative count of errors during primary index query aggregation operations in this namespace.|
| Stop Writes                              | Indicates whether writes are stopped for this namespace due to storage limits (`true` / `false`). |
| Clock Skew Stop Writes                   | Indicates whether writes are stopped for this namespace due to clock skew exceeding the threshold (`true` / `false`). |
