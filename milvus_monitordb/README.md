
# Milvus Database Monitoring



### Prerequisites

* Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

* Python 3.7 or higher version should be installed.

### Installation

1. Create a directory named `milvus`:
```bash
mkdir milvus
cd milvus/
```


2. Download the files `milvus.py` and `milvus.cfg` and place them under the `milvus` directory:
```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/milvus/milvus.py && sed -i "1s|^.*|#! $(which python3)|" milvus.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/milvus/milvus.cfg
```


3. Execute the below command with appropriate arguments to check for the valid JSON output:
```bash
python3 milvus.py --host "localhost" --port "9091"
```


4. After the command with parameters gives the expected output, please configure the relevant parameters in the `milvus.cfg` file:
```ini
[milvus]
host = "127.0.0.1"
port = 9091
```



#### Linux

- Place the `milvus` folder under the Site24x7 Linux Agent plugin directory:

```bash
mv milvus /opt/site24x7/monagent/plugins/
```

#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.


- Move the folder `milvus` into the Site24x7 Windows Agent plugin directory:

```cmd
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\milvus
```

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---

## Supported Metrics

### System Health

| Metric Name | Description |
| --- | --- |
| Response Time | Time taken in milliseconds to fetch metrics from the Milvus endpoint. |
| Milvus Status | Current availability status of the Milvus instance (1 for up, 0 for down). |
| Metrics Total | Total number of Prometheus metric series parsed from the endpoint. |
| CPU Percent | CPU utilization or total CPU seconds used by the process. |
| Memory Usage | Resident memory currently consumed by the process in MB. |
| Active Goroutines | Number of active Go goroutines running concurrently. |
| OS Threads | Number of operating system threads used by the Go runtime. |
| Open File Descriptors | Current number of open file descriptors for the process. |
| Process Max FDs | Maximum allowed file descriptors for the process. |
| Resident Memory MB | Physical RAM consumed by the process (RSS) in MB. |
| Virtual Memory MB | Total virtual memory allocated by the process in MB. |
| Heap Usage MB | Heap memory currently in use by the Go runtime in MB. |
| Heap Idle MB | Heap memory waiting to be used or returned to OS in MB. |
| Heap Sys MB | Total heap memory obtained from the operating system in MB. |
| MMap InUse MB | Memory space actively used for memory-mapped files in MB. |
| Next GC Threshold MB | Target heap size for the next garbage collection cycle in MB. |
| GC Duration Avg ms | Average duration of garbage collection pauses in milliseconds. |
| GC Cycle Count | Total number of completed garbage collection cycles. |
| Mallocs Count | Cumulative count of heap memory allocations. |
| Write Blocks | Counter indicating forced write-denial or block states in RootCoord. |

### Nodes

| Metric Name | Description |
| --- | --- |
| Total Nodes | Total number of active nodes across the Milvus cluster. |
| Proxy Nodes | Number of active Proxy component nodes. |
| Query Nodes | Number of active QueryNode component nodes. |
| Data Nodes | Number of active DataNode component nodes. |
| Index Nodes | Number of active IndexNode component nodes. |
| Streaming Nodes | Number of active StreamingNode component nodes. |
| gRPC Active Conns | Number of active gRPC connections. |
| Proxy Active Conns | Number of active client connections handled by Proxies. |
| DML Channels Count | Number of data manipulation language (DML) channels. |
| Collections Loaded | Number of collections currently loaded into query memory. |
| RootCoord Collections | Total collections registered in RootCoord. |
| RootCoord Partitions | Total partitions registered in RootCoord. |
| QN Entity Count | Total number of entities loaded or managed in QueryNodes. |
| QN Entity Memory MB | Memory size consumed by entities in QueryNodes in MB. |
| QN Flowgraph Count | Number of active processing flowgraphs in QueryNodes. |
| QN DML Channel Count | Number of DML virtual channels assigned to QueryNodes. |
| DN Flowgraph Count | Number of active processing flowgraphs in DataNodes. |
| DN Consume Bytes | Total bytes consumed from message streams by DataNodes. |
| DN Consume Msg Count | Total message count consumed by DataNodes. |
| DN AutoFlush Op Count | Number of auto-flush operations executed by DataNodes. |

### Query & Search

| Metric Name | Description |
| --- | --- |
| Query Requests | Total count of processed vector query requests. |
| Query Latency ms | Average execution latency for vector queries in milliseconds. |
| Query Queue Latency ms | Average time query requests spend waiting in queue in milliseconds. |
| Query Reduce Latency ms | Average time spent reducing/merging query results in milliseconds. |
| Query CoreSearch Latency ms | Core vector search operation execution latency in milliseconds. |
| Search Requests | Total count of vector similarity search requests. |
| Search Latency ms | Average execution latency for vector search requests in milliseconds. |
| Search Queue Latency ms | Average time search requests spend waiting in queue in milliseconds. |
| Search TopK Avg | Average Top-K value requested in vector searches. |
| Search WaitResult Latency ms | Average time proxy waits for search result shards in milliseconds. |
| Search DecodeResult Latency ms | Average time taken to decode search results in milliseconds. |
| QN ReadTask Concurrency | Current concurrency level of read tasks in QueryNodes. |
| QN ReadTask Ready Queue | Length of the ready queue for QueryNode read tasks. |
| QN ReadTask Unsolved Queue | Length of the unsolved/pending queue for QueryNode read tasks. |
| QN LoadSegment Concurrency | Concurrency level of segment loading tasks in QueryNodes. |
| QN LoadSegment Latency ms | Average latency for loading segments into QueryNodes in milliseconds. |
| QN MsgDispatcher Lag ms | Time lag of message dispatchers in QueryNodes in milliseconds. |
| Search QPS Rate | Current rate of search queries per second (QPS). |
| Insert QPS Rate | Current rate of insert requests per second (QPS). |
| Searched Vector Count | Total number of individual vectors scanned during searches. |

### Storage & Memory

| Metric Name | Description |
| --- | --- |
| Data Collections | Number of collections managed by DataCoord. |
| Query Collections | Number of collections managed by QueryCoord. |
| Query Replicas | Total number of collection replicas loaded for queries. |
| Data Segments | Total number of data segments managed by DataCoord. |
| Loaded Segments | Total number of segments loaded into memory across QueryNodes. |
| Growing Segments | Number of active, mutable segments currently accepting inserts. |
| Sealed Segments | Number of sealed segments closed to further insertions. |
| Flushed Segments | Number of flushed segments safely persisted to object storage. |
| Total Indexed Rows | Total number of entity rows indexed across storage. |
| Loaded Entities QN | Total entities loaded into QueryNode runtime memory. |
| Binlog Size MB | Total size of generated binlog files in MB. |
| Index Files Size MB | Total storage size consumed by vector index files in MB. |
| Storage KV Size MB | Storage space utilized by Key-Value storage components in MB. |
| Meta KV Size MB | Storage space utilized by metadata Key-Value stores in MB. |
| Raw Data Size MB | Raw uncompressed size of ingested vector and scalar data in MB. |
| QN CGO Memory MB | Memory allocated via CGO (C bindings) in QueryNodes in MB. |
| Insert Size MB | Total data size received for insertions in MB. |
| Insert Request Count | Total number of insert API requests processed. |
| Delete Vectors Count | Total number of vector deletion entries processed. |
| Flushed Rows Count | Total number of entity rows flushed to persistent storage. |

### Runtime & Queues

| Metric Name | Description |
| --- | --- |
| Proxy Request Count | Total number of incoming requests handled by Proxy nodes. |
| Ingestion Volume | Total volume of data ingested into the system in MB. |
| Flush Request Count | Total number of data flush operations requested. |
| Flushed Bytes MB | Total data size successfully flushed to storage in MB. |
| Mutation Send Latency ms | Average latency for sending data mutations to message queues in milliseconds. |
| DN EncodeBuffer Latency ms | Average buffer encoding latency in DataNodes in milliseconds. |
| DN Save Latency ms | Average data persistence/save latency in DataNodes in milliseconds. |
| Storage Op Count | Total count of storage read/write operations performed. |
| Storage Request Latency ms | Average response latency for storage layer interactions in milliseconds. |
| MQ Consumer Count | Number of active message queue consumers. |
| MsgStream Op Count | Total operations processed through message streams. |
| MsgStream Request Latency ms | Average message stream request processing latency in milliseconds. |
| Proxy TT Lag ms | Time-Travel (TT) synchronization lag tracked by Proxies in milliseconds. |
| Consumer Lag ms | Message consumption time lag in DataNodes in milliseconds. |
| Proxy Queue Length | Current backlog item count inside Proxy request queues. |
| QN Queue Length | Current backlog item count inside QueryNode execution queues. |
| Index Build Latency ms | Average time taken to build vector indexes in IndexNodes in milliseconds. |
| Index Save Latency ms | Average time taken to save built indexes to storage in milliseconds. |
| Index Task Count | Total number of active or processed index tasks. |
| Index TaskQueue Latency ms | Average time index tasks spend waiting in the queue before execution in milliseconds. |
