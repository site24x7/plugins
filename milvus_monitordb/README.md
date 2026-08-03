# Milvus Monitoring

Milvus is an open-source vector database built to power AI applications, vector search, and Retrieval-Augmented Generation (RAG). It exposes Prometheus-style metrics that this plugin uses to report on cluster topology, collection segments, storage usage, search latency, and request throughput.

## Prerequisites

- Download and install the latest version of the [Site24x7 Server Monitoring agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) on the server where you plan to run the plugin.
- Milvus must be running and exposing its metrics endpoint (default port `9091`).

---

# Plugin Installation

## Linux

### Step 1

Create a directory named `milvus_monitordb`.

```bash
mkdir milvus_monitordb
cd milvus_monitordb/
```

### Step 2

Place the following files under the `milvus_monitordb` directory:

- `milvus_monitordb.py`
- `milvus_monitordb.cfg`

### Step 3

Execute the below command with appropriate arguments to check for valid JSON output:

```bash
python3 milvus_monitordb.py host='127.0.0.1' metrics_port='9091'
```

### Step 4

Provide your Milvus configurations in the `milvus_monitordb.cfg` file:

```ini
[milvus_monitordb]
host = "127.0.0.1"
metrics_port = "9091"
```

### Step 5

Move the directory `milvus_monitordb` under the Site24x7 Linux Agent plugin directory:

```bash
mv milvus_monitordb /opt/site24x7/monagent/plugins/
```

---

## Windows

### Step 1

Create a directory named `milvus_monitordb`.

### Step 2

Place the files:

- `milvus_monitordb.py`
- `milvus_monitordb.cfg`

under the `milvus_monitordb` directory.

### Step 3

Create a PowerShell wrapper file `milvus_monitordb.ps1` in the same directory:

```powershell
& "python.exe" "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\milvus_monitordb\milvus_monitordb.py" $args
```

### Step 4

Execute the below command with appropriate arguments in PowerShell to check for valid JSON output:

```powershell
powershell.exe -ExecutionPolicy Bypass -File "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\milvus_monitordb\milvus_monitordb.ps1" host="127.0.0.1" metrics_port="9091"
```

### Step 5

Provide your Milvus configurations in the `milvus_monitordb.cfg` file:

```ini
[milvus_monitordb]
host = "127.0.0.1"
metrics_port = "9091"
```

### Step 6

Move the folder `milvus_monitordb` under the Site24x7 Windows Agent plugin directory:

```text
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
```

The agent will automatically execute the plugin within five minutes, and users can see the plugin monitor under **Site24x7 > Plugins > Plugin Integrations**.

---

# Supported Metrics

## Overview

| Metric Name | Description | Impact on Milvus |
|------------|-------------|------------------|
| Response Time | Time taken to execute the metric collection request. | Higher values indicate latency in communicating with the Milvus metrics endpoint. |
| CPU Percent | Process CPU utilization of the Milvus instance. | Sustained high CPU usage can lead to search latency spikes and ingestion bottlenecks. |
| Memory Usage | Total resident memory consumed by the Milvus process. | High memory utilization can lead to host swapping or OOM (Out-Of-Memory) kills. |
| Active Goroutines | Number of active Go routines in the runtime. | Unusually high counts can indicate thread leakage or high concurrency backlogs. |
| OS Threads | Number of operating system threads allocated by Go runtime. | Reflects system context switching and thread resource allocation. |
| Open File Descriptors | Number of file handles opened by Milvus. | Values approaching system limits (ulimit) can block file I/O and network sockets. |

---

## Nodes and Topology

| Metric Name | Description | Impact on Milvus |
|------------|-------------|------------------|
| Total Nodes | Total number of nodes participating in the Milvus cluster. | Tracks cluster scale and node membership availability. |
| Proxy Nodes | Count of active Proxy coordinator nodes handling client requests. | Low proxy counts relative to traffic can bottleneck incoming API connections. |
| Query Nodes | Count of active QueryNodes executing vector search tasks. | Lower QueryNode availability reduces search capacity and throughput. |
| Data Nodes | Count of active DataNodes handling vector data ingestion and flush. | Unavailability degrades data persistence and binlog generation capabilities. |
| Index Nodes | Count of active IndexNodes processing vector index building. | Fewer index nodes slow down vector index construction times. |
| Streaming Nodes | Count of active StreamingNodes processing WAL/streaming requests. | Affects stream ingestion latency and real-time message stream routing. |
| gRPC Active Conns | Current active gRPC connection count across cluster components. | High counts reflect heavy internal inter-node communication. |
| Proxy Active Conns | Active client connections connected directly to Proxy nodes. | High active connections indicate heavy incoming SDK client traffic. |

---

## Collections and Segments

| Metric Name | Description | Impact on Milvus |
|------------|-------------|------------------|
| Data Collections | Total number of collections registered in DataCoord. | Indicates the logical schema scale managed by the cluster. |
| Query Collections | Number of collections loaded into QueryCoord for searching. | Unloaded collections cannot serve search/query traffic. |
| Query Replicas | Total number of loaded collection replicas across QueryNodes. | More replicas improve search concurrency and fault tolerance. |
| Data Segments | Total count of segments managed by DataCoord. | Higher segment counts increase metadata coordination overhead. |
| Loaded Segments | Total segments currently loaded in memory for query processing. | High counts consume QueryNode RAM; must fit within available memory. |
| Growing Segments | Segments currently receiving new vector insertions in real time. | Large numbers of growing segments increase search latency before indexing. |
| Sealed Segments | Segments closed for insertion and queued/ready for indexing. | Indicates segments awaiting background index building. |
| Flushed Segments | Segments completely persisted to object storage/disk. | Assures durability and completion of data sync processes. |

---

## Storage and Memory

| Metric Name | Description | Impact on Milvus |
|------------|-------------|------------------|
| Total Indexed Rows | Total number of vector entity rows persisted in DataCoord storage. | Primary indicator of overall vector database size over time. |
| Loaded Entities QN | Count of vector entities currently loaded into QueryNodes. | Tracks active search-ready entities loaded in memory. |
| Binlog Size | Total size of raw unindexed insert binlogs on storage. | High binlog volume without indexing increases memory overhead. |
| Index Files Size | Total disk space consumed by built vector index structures. | Directly influences disk capacity planning for index storage. |
| Storage KV Size | Storage footprint consumed by key-value storage engine backend. | Reflects underlying KV metadata and system state disk footprint. |
| Meta KV Size | Memory/disk space used for metadata KV state store. | Excessive meta size can slow down cluster coordination tasks. |
| Raw Data Size | Total uncompressed raw vector data size across DataNodes. | Measures raw ingestion data scale before compaction and indexing. |
| QN CGO Memory | Memory allocated by QueryNode C++ core via CGO for vector search engines. | Primary driver of QueryNode RAM utilization (Knowhere engine usage). |

---

## Latency

| Metric Name | Description | Impact on Milvus |
|------------|-------------|------------------|
| Search Query Latency | End-to-end vector search latency measured at the Proxy level. | Directly impacts end-user application query responsiveness. |
| Core Search Latency | Time spent inside the execution C++ vector search engine (Knowhere). | Isolates vector index search speed from network/framework overhead. |
| QN Search Latency | Time taken by QueryNode to process and return vector search results. | Higher values point to QueryNode compute or memory bottlenecks. |
| Proxy Req Latency | Average latency for general proxy client request processing. | Measures overall frontend API gateway responsiveness. |
| DataNode Flush Lat | Time taken for DataNode to flush segment memory buffers to disk. | Slow flushes can delay data durability and segment sealing. |
| Index Build Latency | Duration taken by IndexNodes to generate vector index structures. | Longer durations delay search availability on newly inserted vectors. |
| gRPC Request Latency | Average latency of inter-component gRPC communications. | Indicates internal network latency between proxy, coordinators, and worker nodes. |

---

## Throughput and Queues

| Metric Name | Description | Impact on Milvus |
|------------|-------------|------------------|
| Proxy Request Count | Total number of requests processed by Proxy nodes. | Reflects overall system traffic volume. |
| Ingestion Volume | Total volume of vector data ingested through Proxy nodes. | Measures raw bandwidth and data ingestion throughput. |
| Delete Vectors Count | Cumulative count of deleted vector entities processed. | High deletion rates trigger compaction tasks and tombstone overhead. |
| Flush Request Count | Total segment flush requests issued across DataNodes. | Tracks segment lifecycle transition frequency. |
| Flushed Rows Count | Total number of rows successfully written during flush operations. | Measures persistence throughput. |
| Searched Vector Count | Total number of target search query vectors processed. | High values indicate heavy batch search workloads. |
| Query Request Count | Cumulative scalar/entity query requests executed. | Measures non-vector scalar query workload. |
| Insert Request Count | Cumulative vector insert API requests received by Proxy. | Reflects bulk ingestion request activity. |
| Search QPS Rate | Current vector search Queries Per Second rate. | Core measure of search throughput. |
| Insert QPS Rate | Current vector insert Queries Per Second rate. | Core measure of ingestion throughput. |
| Proxy Queue Length | Number of search/query tasks waiting in Proxy execution queues. | Non-zero values indicate proxy worker pool saturation. |
| QN Queue Length | Number of vector execution tasks queued inside QueryNodes. | Queue backlogs directly increase search latency. |