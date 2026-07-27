# Weaviate Monitoring
Weaviate is an open-source vector database that stores and searches embeddings for AI applications, such as semantic search and Retrieval-Augmented Generation (RAG). It exposes both a REST/GraphQL API and Prometheus-style metrics that this plugin uses to report on cluster health, storage, and vector index performance.

## Prerequisites

- Download and install the latest version of the [Site24x7 Server Monitoring agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) on the server where you plan to run the plugin.
- Weaviate must be running with Prometheus monitoring enabled (`PROMETHEUS_MONITORING_ENABLED: "true"` in its environment/docker-compose configuration), so the metrics endpoint (default port `2112`) is available.

## Authentication Setup

Unlike RabbitMQ, Weaviate does not ship with a built-in user/permission system for its REST API. Depending on how your Weaviate instance is secured, choose one of the following:

**Anonymous Access (default for local/dev setups)**

If your Weaviate instance has `AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "true"` set, no credentials are required. Leave `api_key` blank in the plugin configuration.

**API Key Authentication**

If your Weaviate instance has API key authentication enabled, generate or obtain an API key with read access and provide it as `api_key`. The plugin sends it as a `Bearer` token in the `Authorization` header.

In both cases, the monitoring credentials only require **read-only** access. The plugin only retrieves metrics and metadata from Weaviate and never creates, modifies, or deletes any data.

## Plugin Installation

#### Linux

- Create a directory named `weaviate`.

		mkdir weaviate
		cd weaviate/

- Place the following files under the `weaviate` directory:

		Weaviate_Monitoring.py
		Weaviate_Monitoring.cfg

- Execute the below command with appropriate arguments to check for the valid json output:

		python3 Weaviate_Monitoring.py --host 'localhost' --port '8080' --metrics_port '2112' --api_key '' --ssl 'false' --ssl_verify 'true'

- Provide your Weaviate configurations in the `Weaviate_Monitoring.cfg` file:

		[global_configurations]
		use_agent_python=1

		[weaviate]
		host = "localhost"
		port = "8080"
		metrics_port = "2112"
		api_key = ""
		ssl = "false"
		ssl_verify = "true"

- Move the directory `weaviate` under the Site24x7 Linux Agent plugin directory:

		mv weaviate /opt/site24x7/monagent/plugins/

#### Windows

- Create a directory named `weaviate`.

- Place the files `Weaviate_Monitoring.py` and `Weaviate_Monitoring.cfg` under the `weaviate` directory.

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers).

- Install the required Python packages:

		pip install requests

- Execute the below command with appropriate arguments in cmd to check for the valid json output:

		python Weaviate_Monitoring.py --host 'localhost' --port '8080' --metrics_port '2112' --api_key '' --ssl 'false' --ssl_verify 'true'

- Provide your Weaviate configurations in the `Weaviate_Monitoring.cfg` file:

		[weaviate]
		host = "localhost"
		port = "8080"
		metrics_port = "2112"
		api_key = ""
		ssl = "false"
		ssl_verify = "true"

- Move the folder `weaviate` under the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Supported Metrics

### Summary

| Name | Description | Impact on Weaviate |
|------|-------------|--------------------|
| Batch Duration | Cumulative time spent processing batch insert operations | Higher values indicate slower bulk data ingestion. |
| Batch Delete Duration | Cumulative time spent processing batch delete operations | High values may indicate expensive delete operations or storage cleanup overhead. |
| Object Duration | Cumulative time spent processing single-object operations | Reflects the performance of individual object insert, update, and delete requests. |
| Async Operations Running | Number of asynchronous background operations currently running | A consistently high value may indicate background processing backlog. |
| Startup Duration | Time taken for the Weaviate node to complete startup | Longer startup times may indicate large datasets or slower storage initialization. |
| Response Time | Time taken for the REST readiness check (`/v1/.well-known/ready`) to respond | Higher response times indicate slower API availability and can impact application responsiveness. |
| GraphQL Response Time | Time taken for a GraphQL introspection query against `/v1/graphql` to respond | Higher values indicate slower query execution and may affect search performance. |
| CPU Percent | Current CPU utilization of the Weaviate process as a percentage of the available CPU cores | Sustained high CPU usage can increase query latency and reduce overall throughput. |
| Memory Usage | Resident memory currently used by the Weaviate process | High memory usage may lead to swapping, reduced performance, or out-of-memory failures. |
| Requests Total | Total number of API requests handled by this Weaviate instance | Reflects workload on the server and helps identify traffic spikes. |
| Open File Descriptors | Number of file descriptors currently open by the Weaviate process | Values approaching the operating system limit may prevent new files or network connections from being opened. |
| Total Shard Count | Total number of shards across all nodes in the cluster | Indicates how data is partitioned for scalability and load distribution. |

### Vector Index Performance

| Name | Description | Impact on Weaviate |
|------|-------------|--------------------|
| Vector Index Size | Number of vectors currently stored in the vector index | Larger indexes require more memory and may increase search time. |
| Vector Index Operations | Total number of operations performed against the vector index | High values indicate increased indexing or search activity. |
| Vector Index Duration | Cumulative time spent performing vector index operations | Rapid growth may indicate slower indexing or vector search performance. |
| Vector Index Maintenance | Cumulative time spent on background vector index maintenance tasks | Increased maintenance activity can temporarily consume CPU and I/O resources. |
| Vector Index Tombstones | Number of tombstoned (deleted but not yet cleaned up) entries in the vector index | Excessive tombstones can reduce search efficiency until cleanup is completed. |
| Vector Index Tombstone Threads | Number of background threads currently cleaning up index tombstones | Indicates background cleanup activity after delete operations. |

### LSM(Log-Structured-Merge) Storage

| Name | Description | Impact on Weaviate |
|------|-------------|--------------------|
| LSM Active Segments | Number of currently active segments in the LSM storage engine | A large number of active segments can increase disk reads and query latency. |
| LSM Segment Count | Total number of segments in the LSM store | High segment counts may indicate pending compaction and additional storage overhead. |
| LSM Segment Size | Total on-disk size of LSM segments | Reflects disk space consumed by stored data. |
| LSM Bloom Filter Duration | Cumulative time spent evaluating bloom filters during LSM lookups | Higher values may indicate increased storage lookup overhead. |

### Cluster Topology

### Collection,Object and NOde count

| Name | Description | Impact on Weaviate |
|------|-------------|--------------------|
| Collection Count | Number of collections (classes) defined in the Weaviate schema | Indicates the number of datasets managed by Weaviate. |
| Object Count | Total number of objects stored across all nodes | Reflects database size and storage growth over time. |
| Node Count | Number of nodes in the Weaviate cluster | Helps monitor cluster availability and scalability. |

#### Collection Details

| Name | Description | Impact on Weaviate |
|------|-------------|--------------------|
| Name | Name of the collection (class) in the Weaviate schema | Identifies the collection being monitored and used for storing related objects. |
| Vectorizer | Vectorizer module configured for the collection (`none` if vectorization is handled externally) | Determines how vectors are generated and affects indexing and semantic search behavior. |

#### Node Details

| Name | Description | Impact on Weaviate |
|------|-------------|--------------------|
| Name | Unique identifier for the node in the Weaviate cluster | Identifies the node for monitoring, diagnostics, and cluster management. |
| Shard Count | Number of shards hosted on the node | Indicates how data is distributed and balanced across cluster nodes. |
| Object Count | Total number of objects stored on the node | Helps monitor data distribution and identify storage imbalance. |

#### Shard Details

| Name | Description | Impact on Weaviate |
|------|-------------|--------------------|
| Name | Unique identifier of the shard | Identifies the specific shard being monitored. |
| Class | Collection (class) to which the shard belongs | Indicates which collection's data is stored in the shard. |
| Node | Node currently hosting the shard | Shows the physical location of the shard within the cluster. |
| Object Count | Number of objects stored in the shard | Helps monitor shard utilization and detect uneven data distribution. |

## Sample Images
<img width="1060" height="494" alt="image" src="https://github.com/user-attachments/assets/49915a3f-1e94-4d0b-8d45-dc16a745a0e4" />
<img width="1066" height="445" alt="image" src="https://github.com/user-attachments/assets/66e07cbf-e9dc-4db8-b815-cf547090f645" />



