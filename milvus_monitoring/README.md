# Milvus Monitoring

Monitor the health, cluster topology, storage, query/search performance, and Go runtime of a [Milvus](https://milvus.io/) vector database instance using Site24x7's plugin integration.

## Prerequisites

* Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) on the server where the plugin will run.

### Enable the Milvus Metrics Endpoint

Milvus exposes Prometheus metrics on port `9091` by default (path `/metrics`). This is enabled out of the box for Milvus standalone and cluster deployments.

* **Docker / Docker Compose** — ensure the metrics port is published:
  ```yaml
  ports:
    - "9091:9091"
  ```

## Installation

1. Create a directory named `milvus_monitoring`:
   ```bash
   mkdir milvus_monitoring
   cd milvus_monitoring/
   ```

2. Download `milvus_monitoring.py` and `milvus_monitoring.cfg` into the directory:
   ```bash
   wget https://raw.githubusercontent.com/site24x7/plugins/master/milvus_monitoring/milvus_monitoring.py 
   wget https://raw.githubusercontent.com/site24x7/plugins/master/milvus_monitoring/milvus_monitoring.cfg
   ```

3. Run the plugin manually to confirm it returns valid JSON:
   ```bash
   python3 milvus_monitoring.py --host "localhost" --metrics_port "9091" --ssl "false" --insecure "false"
   ```

4. Once the manual run returns the expected output, set the connection parameters in `milvus_monitoring.cfg`:
   ```ini
   [milvus_monitoring]
   host = "localhost"
   metrics_port = "9091"
   ssl = "false"
   insecure = "false"
   ```

### Linux

* Place the `milvus_monitoring` folder under the Site24x7 Linux Agent plugin directory:
  ```bash
  mv milvus_monitoring /opt/site24x7/monagent/plugins/
  ```

### Windows

* Since this is a Python plugin, follow the steps in [this guide](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers) to run Python plugin scripts on a Windows server.

* Move the `milvus_monitoring` folder into the Site24x7 Windows Agent plugin directory:
  ```cmd
  C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\milvus_monitoring
  ```

The agent automatically executes the plugin within five minutes and sends performance data to the Site24x7 data center.

## Configuration Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `host` | Hostname or IP address of the Milvus instance | `localhost` |
| `metrics_port` | Milvus Prometheus metrics port | `9091` |
| `ssl` | Use HTTPS to connect (`true`/`false`) | `false` |
| `insecure` | Skip SSL certificate verification (`true`/`false`) | `false` |

## Supported Metrics


### Cluster Overview

| Metric Name | Description | Unit |
| --- | --- | --- |
| Total Nodes | Number of distinct physical nodes (counts unique `node_id`; standalone = 1) | nodes |
| Thread Count | Total OS threads in use by Milvus (`milvus_thread_num`) | threads |
| Proxy Components | Number of active Proxy component instances | components |
| Query Components | Number of active QueryNode component instances | components |
| Data Components | Number of active DataNode component instances | components |
| Coordinator Components | Number of active coordinator instances (v3.x `mixcoord`; sums legacy root/data/query/index coords) | components |
| Collection Count | Total collections tracked by DataCoord (`milvus_datacoord_collection_num`) | collections |
| Partition Count | Total partitions registered in RootCoord | partitions |
| DML Channels | Number of DML channels registered in RootCoord | channels |
| Message Streams | Number of message stream objects registered in RootCoord | streams |

### Storage

| Metric Name | Description | Unit |
| --- | --- | --- |
| Data Segments | Total data segments managed by DataCoord | segments |
| Growing Segments | Active mutable segments currently accepting inserts | segments |
| Sealed Segments | Sealed segments closed to further insertions | segments |
| Flushed Segments | Segments safely persisted to object storage | segments |
| Stored Rows | Total number of entity rows stored | entities |
| Loaded Entities | Entities loaded into QueryNode runtime memory | entities |
| Storage KV Size | Size of the meta Key-Value store (`milvus_meta_kv_size`) | MB |
| QueryNode Disk Used | Local disk space used by QueryNode(s) for caching/loading segments | MB |


### Query & Search

| Metric Name | Description | Unit |
| --- | --- | --- |
| Search Requests | Total count of vector similarity search requests (`search_latency`, `module="cardinal"`) | requests |
| Search Latency | Average execution latency for search requests | ms |
| Query Requests | Total count of requests that passed through the request queue (`queue_latency`, `module="cardinal"`) | requests |
| Query Latency | Average time requests spend queued before execution | ms |
| Execution Latency | Average per-request execution latency (`exec_latency`, `module="cardinal"`) | ms |


### Process & Memory

| Metric Name | Description | Unit |
| --- | --- | --- |
| Memory Usage | Resident memory consumed by the process (RSS) | MB |
| Virtual Memory | Total virtual memory allocated by the process | MB |
| Heap Usage | Heap memory currently in use by the Go runtime | MB |
| Heap Idle | Heap memory waiting to be used or returned to the OS | MB |
| Heap Sys | Total heap memory obtained from the operating system | MB |
| Next GC Threshold | Target heap size for the next garbage collection cycle | MB |
| CPU Seconds | Cumulative CPU time consumed by the process | s |
| Open File Descriptors | Current number of open file descriptors | fds |
| Max File Descriptors | Maximum allowed file descriptors for the process | fds |
| Process Uptime | Time elapsed since the Milvus process started | s |

### Go Runtime

| Metric Name | Description | Unit |
| --- | --- | --- |
| Goroutines | Number of active Go goroutines running concurrently | goroutines |
| OS Threads | Number of operating system threads used by the Go runtime | threads |
| GC Pause Duration | Cumulative garbage collection pause time | ms |
| GC Cycle Count | Total number of completed garbage collection cycles | cycles |

### Network & Storage I/O

| Metric Name | Description | Unit |
| --- | --- | --- |
| Network Received | Cumulative bytes received by the process over the network | MB |
| Network Transmitted | Cumulative bytes sent by the process over the network | MB |
| Storage Read Bytes | Total bytes read from the underlying object storage | MB |
| Storage Write Bytes | Total bytes written to the underlying object storage | MB |
| Storage Read Ops | Number of object storage read operations | ops |
| Storage Write Ops | Number of object storage write operations | ops |
| Storage Failed Ops | Number of failed object storage operations | ops |

### Cluster Health & Tasks

| Metric Name | Description | Unit |
| --- | --- | --- |
| Meta Store Operations | Total metastore (etcd) operations across get/put/txn | ops |
| Meta Store Latency | Average metastore request latency | ms |
| Data Nodes (Managed) | Number of DataNodes managed by DataCoord | nodes |
| Index Nodes (Managed) | Number of IndexNodes managed by DataCoord | nodes |
| Query Nodes (Managed) | Number of QueryNodes managed by QueryCoord | nodes |
| Proxy Nodes (Managed) | Number of Proxy nodes managed by RootCoord | nodes |
| QueryCoord Pending Tasks | Number of tasks in QueryCoord's scheduler | tasks |
| Index/Stats Tasks In Progress | Index build / stats jobs currently in progress in DataCoord | tasks |
| DDL Requests | Total DDL operations processed by RootCoord | requests |
| Segment GC Runs | Number of segment garbage-collection runs | runs |

### Components

Per-component summary of the roles running on the Milvus node. One row per active role.

| Attribute | Description |
| --- | --- |
| name | Milvus component/role name as reported by Milvus (proxy, querynode, datanode, mixcoord, etc.) |
| Instance Count | Number of active instances for the component |
| State | Health status of the component |

## Sample Images

<img width="3282" height="1689" alt="image" src="https://github.com/user-attachments/assets/6694f773-226c-4ab7-bec7-b0cdcbabd2e1" />

<img width="3282" height="1689" alt="image" src="https://github.com/user-attachments/assets/b45402b3-cc29-461c-a85e-bd4319b4076b" />
