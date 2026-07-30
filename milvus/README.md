# Milvus Monitoring

Milvus is an open-source vector database built for high-performance similarity search and AI applications. This plugin collects health, performance, and resource metrics from a Milvus deployment's Prometheus `/metrics` endpoint and reports them to Site24x7 as a custom plugin monitor.

## Prerequisites

- Download and install the latest version of the Site24x7 Server Monitoring agent on the server where you plan to run the plugin.
- Python 3 must be available on the host running the plugin.
- The Milvus instance must expose its Prometheus metrics endpoint (enabled by default on most Milvus deployments) and it must be reachable from the plugin host.

### Metrics Endpoint Access

By default, Milvus exposes Prometheus-formatted metrics at:

```
http://<milvus-host>:9091/metrics
```

Confirm the endpoint is reachable before installing the plugin:

```bash
curl http://localhost:9091/metrics
```

If Milvus is running remotely, in a container, or behind a different port mapping, update the `HOSTNAME` and `PORT` values at the top of `milvus.py` (see Configuration below).

## Plugin Installation

### Linux

1. Create a directory named `milvus`.

   ```bash
   mkdir milvus
   cd milvus/
   ```

2. Download the plugin file and place it under the `milvus` directory.

   ```bash
   wget https://raw.githubusercontent.com/site24x7/plugins/milvus/milvus/milvus.py
   ```

3. Execute the script to verify it returns valid JSON output.

   ```bash
   python3 milvus.py
   ```

4. Move the `milvus` directory under the Site24x7 Linux Agent plugin directory.

   ```bash
   mv milvus /opt/site24x7/monagent/plugins/
   ```

### Windows

1. Create a directory named `milvus`.

2. Download `milvus.py` and place it under the `milvus` directory.

3. Since it's a Python plugin, follow the steps in [this link](https://www.site24x7.com/help/admin/monitoring-agent/windows-plugin-monitor.html) to run Python plugins on a Windows server.

4. Execute the script in `cmd` to verify it returns valid JSON output.

   ```cmd
   python milvus.py
   ```

5. Move the `milvus` folder under the Site24x7 Windows Agent plugin directory.

   ```
   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
   ```

The agent will automatically execute the plugin within five minutes, and you can view the plugin monitor under **Site24x7 > Plugins > Plugin Integrations**.

## Configuration

The plugin connects using constants defined at the top of `milvus.py`:

```python
HOSTNAME = "localhost"
PORT = "9091"
TIMEOUT = 10
```

Update `HOSTNAME` and `PORT` to match your Milvus deployment before moving the plugin into the agent's plugin directory.

## Diagnostics

To list every raw metric name exposed by the Milvus `/metrics` endpoint (useful for troubleshooting or extending the plugin), run:

```bash
python3 milvus.py --list-metrics
```

## Supported Metrics

### Cluster Health

| Name | Description |
|---|---|
| Milvus_Status | Whether the plugin could successfully reach and parse the Milvus metrics endpoint (1 = up, 0 = down) |
| QueryNodes | Number of QueryNodes registered with the QueryCoord |
| Collections_Loaded | Number of collections currently loaded into memory across QueryNodes |
| DataNodes_Count | Number of DataNodes registered with the DataCoord |
| IndexNode_Count | Number of IndexNodes registered with the DataCoord |
| Proxy_Nodes_Count | Number of active proxy nodes registered with the RootCoord |
| DML_Channels_Count | Number of DML (data manipulation) channels managed by the RootCoord |

### Component Availability

| Name | Description |
|---|---|
| RootCoord_Collections | Total number of collections tracked by the RootCoord |
| RootCoord_Partitions | Total number of partitions tracked by the RootCoord |
| Process_Open_FDs | Number of file descriptors currently open by the Milvus process |
| Process_Max_FDs | Maximum number of file descriptors allowed for the Milvus process |

### Search

| Name | Description |
|---|---|
| Search_Vectors | Total number of vectors submitted across all search requests |
| Search_Requests | Total number of search-type requests processed |
| Search_Latency.ms | Average end-to-end latency for search requests, in milliseconds |
| Search_Queue_Latency.ms | Average time search requests spend waiting in the QueryNode queue |
| Search_TopK_Avg | Average TopK value requested across search operations |
| Search_WaitResult_Latency.ms | Average time the proxy waits for search results from QueryNodes |
| Search_DecodeResult_Latency.ms | Average time spent decoding search results on the proxy |

### Query

| Name | Description |
|---|---|
| Query_Latency.ms | Average end-to-end latency for query (non-search) requests |
| Query_Requests | Total number of query-type requests processed |
| Loaded_Segments | Number of sealed segments currently loaded in QueryNodes |
| Query_Queue_Latency.ms | Average time query requests spend waiting in the proxy queue |
| Query_Reduce_Latency.ms | Average time spent reducing/merging query results on QueryNodes |
| Query_CoreSearch_Latency.ms | Average latency of the internal core search operation |

### QueryNode Performance

| Name | Description |
|---|---|
| QN_Entity_Count | Number of entities currently loaded on QueryNodes |
| QN_Entity_Memory.MB | Memory consumed by loaded entities on QueryNodes, in MB |
| QN_Flowgraph_Count | Number of active flowgraphs on QueryNodes |
| QN_DML_Channel_Count | Number of DML channels subscribed to by QueryNodes |
| QN_ReadTask_Concurrency | Current concurrency level for read tasks on QueryNodes |
| QN_ReadTask_Ready_Queue | Number of read tasks ready to be executed |
| QN_ReadTask_Unsolved_Queue | Number of read tasks still waiting to be scheduled |
| QN_LoadSegment_Concurrency | Current concurrency level for segment loading operations |
| QN_LoadSegment_Latency.ms | Average time taken to load a segment into a QueryNode |
| QN_MsgDispatcher_Lag.ms | Lag of the QueryNode message dispatcher behind the latest timestamp |

### Index Performance

| Name | Description |
|---|---|
| Index_Build_Latency.ms | Average time taken by IndexNodes to build an index |
| Index_Save_Latency.ms | Average time taken to persist a built index to storage |
| Index_Task_Count | Number of index build tasks currently tracked |
| Index_TaskQueue_Latency.ms | Average time index tasks spend waiting in queue before execution |
| Index_Load_Latency.ms | Average time taken to load an index into memory |
| Index_DataCoord_Tasks | Number of index-related tasks tracked by the DataCoord |

### Data Ingestion

| Name | Description |
|---|---|
| Insert_Size.MB | Total size of data received via insert requests, in MB |
| Insert_Request_Count | Total number of insert requests processed by the proxy |
| Delete_Vector_Count | Total number of vectors removed via delete operations |
| Flush_Request_Count | Total number of flush requests processed by DataNodes |
| Flushed_Rows_Count | Total number of rows persisted to storage via flush operations |
| Flushed_Bytes.MB | Total size of data persisted via flush operations, in MB |
| Mutation_Send_Latency.ms | Average latency for sending mutation (insert/delete) requests |

### DataNode Performance

| Name | Description |
|---|---|
| DN_Flowgraph_Count | Number of active flowgraphs on DataNodes |
| DN_Consume_Bytes | Total bytes consumed from the message queue by DataNodes |
| DN_Consume_Msg_Count | Total number of messages consumed from the message queue by DataNodes |
| DN_EncodeBuffer_Latency.ms | Average time taken to encode insert buffers before flush |
| DN_Save_Latency.ms | Average time taken by DataNodes to save data to storage |
| DN_AutoFlush_Op_Count | Number of automatic buffer-flush operations triggered |

### Storage Usage

| Name | Description |
|---|---|
| Binlog_Size.MB | Total size of stored binlog (write-ahead log) files, in MB |
| Index_Files_Size.MB | Total size of stored index files, in MB |
| Storage_KV_Size.MB | Size of data stored in the underlying key-value storage layer |
| Storage_Op_Count | Total number of operations performed against the storage layer |
| Storage_Request_Latency.ms | Average latency of requests to the storage layer |

### Memory Usage

| Name | Description |
|---|---|
| Heap_Usage.MB | Heap memory currently in use by the Milvus process, in MB |
| Heap_Idle.MB | Heap memory currently idle but not yet released to the OS |
| Heap_Sys.MB | Total heap memory obtained from the OS |
| Resident_Memory.MB | Resident memory (RSS) used by the Milvus process |
| Virtual_Memory.MB | Total virtual memory used by the Milvus process |
| MMap_InUse.MB | Memory-mapped space currently in use by Milvus |
| Next_GC_Threshold.MB | Heap size target that will trigger the next garbage collection cycle |

### Go Runtime

| Name | Description |
|---|---|
| Threads | Total number of OS threads used by the Milvus process |
| Goroutines | Number of active Go routines running in the Milvus process |
| Go_Threads_Count | Number of OS threads created by the Go runtime |
| GC_Duration_Avg.ms | Average duration of garbage collection cycles |
| GC_Cycle_Count | Total number of garbage collection cycles completed |
| Mallocs_Count | Total number of memory allocations made by the Go runtime |

### Message Queue

| Name | Description |
|---|---|
| Consumer_Lag.ms | Lag between DataNode message consumption and the latest published timestamp |
| MQ_Consumer_Count | Number of active consumers subscribed to the message queue |
| MsgStream_Op_Count | Total number of message stream operations performed |
| MsgStream_Request_Latency.ms | Average latency of message stream requests |
| Proxy_TT_Lag.ms | Lag between the proxy's timestamp and the latest allocated timestamp |

### Proxy Performance

| Name | Description |
|---|---|
| Proxy_Request_Count | Total number of requests handled by the proxy, across all request types |
| Proxy_Request_Latency.ms | Average latency for requests handled by the proxy |
| Proxy_RateLimit_Count | Number of requests rejected due to rate limiting |
| Proxy_SendBytes.MB | Total bytes sent by the proxy to downstream components |
| Proxy_ApplyPK_Latency.ms | Average latency for primary key allocation on the proxy |
| Proxy_ApplyTimestamp_Latency.ms | Average latency for timestamp allocation on the proxy |
| Proxy_MsgStream_Obj_Num | Number of message stream objects currently held by the proxy |

### Cache Performance

| Name | Description |
|---|---|
| Proxy_Cache_Hit_Count | Number of cache hits recorded on the proxy |
| Proxy_Cache_Update_Latency.ms | Average latency for updating the proxy's internal cache |

### Vector Index Algorithms

| Name | Description |
|---|---|
| HNSW_BitsetRatio_Avg | Average ratio of filtered (bitset) entities during HNSW search |
| HNSW_SearchHops_Avg | Average number of graph hops traversed during HNSW search |
| IVF_Search_Count | Total number of IVF index search operations performed |
| DiskANN_SearchHops_Avg | Average number of hops traversed during DiskANN search |
| DiskANN_RangeSearchIters_Avg | Average number of iterations performed during DiskANN range search |
| DiskANN_BitsetRatio_Avg | Average ratio of filtered (bitset) entities during DiskANN search |

### Reliability

| Name | Description |
|---|---|
| Write_Blocks | Number of times writes were force-denied by the RootCoord (e.g. due to quota limits) |
| RootCoord_DDL_Request_Count | Total number of DDL (data definition) requests processed by the RootCoord |
| RootCoord_DDL_Latency.ms | Average latency for DDL requests on the RootCoord |
| RootCoord_SyncTimetick_Latency.ms | Average latency for timestamp synchronization across the cluster |
| QN_Disk_Cache_Evict_Count | Number of entries evicted from the QueryNode disk cache |
| QN_Disk_Cache_Load_Count | Number of entries loaded into the QueryNode disk cache |
| QN_Segment_Access_Wait_Count | Number of times a query had to wait for a segment to be loaded from disk cache |

### Storage & Data Overview

| Name | Description |
|---|---|
| Vectors | Total number of vector rows stored across the cluster |
| Segments | Total number of segments currently tracked by QueryNodes |
| Metrics_Total | Total number of individual metric samples parsed from the `/metrics` endpoint (diagnostic counter) |
| CPU_Time.seconds | Cumulative CPU time consumed by the Milvus process, in seconds |