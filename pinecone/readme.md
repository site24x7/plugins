# Pinecone Monitoring

[Pinecone](https://www.pinecone.io/) is a managed vector database used for similarity search, retrieval-augmented generation (RAG), and other embedding-based workloads. This plugin auto-discovers every index in a Pinecone project and reports index health, capacity, configuration, and (where available) Prometheus-based request/latency telemetry to Site24x7 - no index names or endpoints need to be entered manually.

## Prerequisites

- Download and install the latest version of the [Site24x7 Server Monitoring agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) on the server where you plan to run the plugin.
- Python 3.7 or later, with the `requests` library installed.
- A Pinecone API key with read access to the project you want to monitor.
- (Optional) A Pinecone **project ID**, required only if you want the Telemetry, Serverless Operations, and Latency tabs populated. These come from Pinecone's Prometheus metrics endpoint, which is available on **Standard and Enterprise** Pinecone plans only. On other plans the plugin still reports full index health/capacity/configuration data - the telemetry fields simply stay at their default values.

## API Key Creation

1. Log in to the [Pinecone console](https://app.pinecone.io/).
2. Go to your project, then **API Keys**.
3. Create a new key (or use an existing one) with at least read access.
4. Copy the key - it will only be shown once.
5. If you want telemetry metrics as well, copy your **Project ID** from the same console (found in your project's settings).

## Plugin Installation

### Linux

- Create a directory named `pinecone`.

		mkdir pinecone
		cd pinecone/

- Place `pinecone.py` and `pinecone.cfg` under the `pinecone` directory.

- Install the required Python package:

		pip3 install requests

- Execute the below command with appropriate arguments to check for valid JSON output:

		python3 pinecone.py --api_key 'your-real-pinecone-api-key' --api_version '2025-10' --project_id 'your-project-id'

-  Provide your Pinecone configuration in the `pinecone.cfg` file:

		[global_configurations]
		use_agent_python=1

		[pinecone]
		api_key="your-real-pinecone-api-key"
		api_version="2025-10"
		project_id="your-project-id"
		logs_enabled="False"
		log_type_name=None
		log_file_path=None

- Move the directory `pinecone` under the Site24x7 Linux Agent plugin directory:

		mv pinecone /opt/site24x7/monagent/plugins/

### Windows

> **Note:** Site24x7's Windows agent supports plugins written in **Batch, PowerShell, VB, or DLL** - Python is not invoked directly on Windows the way it is on Linux. To run a Python-based plugin on a Windows server, follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers) to set up the required wrapper before continuing below.

- Create a directory named `pinecone`.

- Place `pinecone.py` and `pinecone.cfg` under the `pinecone` directory.

- Install the required Python package:

		pip install requests

- Execute the below command with appropriate arguments in `cmd` or PowerShell to check for valid JSON output:

		python pinecone.py --api_key "your-real-pinecone-api-key" --api_version "2025-10" --project_id "your-project-id"

- Provide your Pinecone configuration in the `pinecone.cfg` file:

		[pinecone]
		api_key="your-real-pinecone-api-key"
		api_version="2025-10"
		project_id="your-project-id"
		logs_enabled="False"
		log_type_name=None
		log_file_path=None

- Move the folder `pinecone` under the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins

The agent will automatically execute the plugin within five minutes, and you can see the plugin monitor under **Site24x7 > Plugins > Plugin Integrations**.

## Configuration Reference

| Parameter | Required | Description |
| --- | --- | --- |
| `api_key` | Yes | Your Pinecone API key. |
| `api_version` | No | Pinecone API version header to send with every request. Defaults to `2025-10`. |
| `project_id` | No | Pinecone project ID. Only needed to populate the Telemetry, Serverless Operations, and Latency tabs (Prometheus metrics, Standard/Enterprise plans only). Leave unset to skip these. |
| `logs_enabled` | No | Enable log collection for this plugin application. Defaults to `False`. |
| `log_type_name` | No | Display name of the log type, if log collection is enabled. |
| `log_file_path` | No | Comma-separated list of log file paths, if log collection is enabled. |

## Supported Metrics

### Health Snapshot

Name | Description
--- | ---
Database Available | Whether the Pinecone API responded successfully (1) or not (0)
HTTP Status | HTTP status code returned by the last list-indexes call
Total Indexes | Total number of indexes found in the project
Indexes Ready | Number of indexes currently in a ready state
Indexes Not Ready | Number of indexes not yet ready
Number Of Indexes Monitored | Number of indexes actually reported in the child table (max 25)

### Capacity

Name | Description
--- | ---
Total Vectors Stored | Sum of vector counts across all indexes
Total Namespaces | Sum of namespace counts across all indexes
Largest Index Vector Count | Vector count of the largest index
Largest Index Name | Name of the largest index
Smallest Index Vector Count | Vector count of the smallest index
Smallest Index Name | Name of the smallest index
Average Vector Count Per Index | Average vectors per index across the project
Indexes With Zero Vectors | Number of indexes currently holding no vectors

### Configuration

Name | Description
--- | ---
Serverless Indexes | Number of serverless-type indexes
Pod Based Indexes | Number of pod-based indexes
Average Dimension Across Indexes | Average vector dimension across all indexes
Unique Regions In Use | Number of distinct cloud regions in use
Regions In Use | Comma-separated list of regions
Unique Cloud Providers In Use | Number of distinct cloud providers in use
Cloud Providers In Use | Comma-separated list of cloud providers

### Fullness

Name | Description
--- | ---
Average Index Fullness Percent | Average index fullness across all indexes
Maximum Index Fullness Percent | Highest fullness percentage among all indexes

### Embedding And Security

Name | Description
--- | ---
Indexes With Embedding Configured | Number of indexes with integrated embedding configured
Embedding Models In Use | Comma-separated list of embedding models in use
Indexes With Deletion Protection Enabled | Number of indexes with deletion protection turned on

### Performance And Reliability

Name | Description
--- | ---
Total Scan Time Seconds | Total time taken to collect all metrics for this poll
Average Index Response Time Seconds | Average per-index response time for stats calls
Indexes That Failed To Respond | Number of indexes whose stats call failed or timed out

### Telemetry

*Populated only when `project_id` is set and the Pinecone plan supports Prometheus metrics (Standard/Enterprise).*

Name | Description
--- | ---
Telemetry Available | Whether telemetry data was successfully retrieved (1) or not (0)
Total Upsert Requests | Total number of upsert requests recorded
Average Upsert Latency Milliseconds | Average upsert latency
Total Read Units Consumed | Total read units consumed
Total Write Units Consumed | Total write units consumed
Average CPU Usage Percent | Average CPU usage across dedicated read node shards
Total Data Plane Requests | Total data plane requests across all operations
Total Data Plane Errors | Total data plane requests that resulted in errors
Data Plane Error Rate Percent | Error rate as a percentage of total requests
Total Storage Size Bytes | Total index storage size in bytes
Total Records (Telemetry) | Total record count reported via telemetry
Telemetry Vector Count | Vector count as reported via telemetry (cross-checks Capacity tab)

### Serverless Operations

*Populated only when `project_id` is set and the Pinecone plan supports Prometheus metrics.*

Name | Description
--- | ---
Query Requests | Number of query requests made
Fetch Requests | Number of fetch requests made
Update Requests | Number of update requests made
Delete Requests | Number of delete requests made
List Requests | Number of list requests made
Query Requests Duration Milliseconds | Total time spent processing query requests
Fetch Requests Duration Milliseconds | Total time spent processing fetch requests
Update Requests Duration Milliseconds | Total time spent processing update requests
Delete Requests Duration Milliseconds | Total time spent processing delete requests
Upsert Requests Duration Milliseconds | Total time spent processing upsert requests
List Requests Duration Milliseconds | Total time spent processing list requests

### Latency

*Populated only when `project_id` is set and the Pinecone plan supports Prometheus metrics.*

Name | Description
--- | ---
Request Latency Min Milliseconds | Minimum server-side processing latency
Request Latency Max Milliseconds | Maximum server-side processing latency
Request Latency Avg Milliseconds | Average server-side processing latency
Request Latency P50 Milliseconds | 50th percentile latency
Request Latency P90 Milliseconds | 90th percentile latency
Request Latency P95 Milliseconds | 95th percentile latency
Request Latency P99 Milliseconds | 99th percentile latency
Request Latency P999 Milliseconds | 99.9th percentile latency
Request Latency Sample Count | Number of latency samples the above percentiles are based on

### Indexes

Name | Description
--- | ---
name | Name of the index
Vector Count | Number of vectors in this index
Dimension | Vector dimension configured for this index
Index Fullness | Fullness percentage for this index
Ready Status | Whether this index is ready (1) or not (0)
Is Serverless | Whether this index is serverless (1) or pod-based (0)
Has Embedding Configured | Whether this index has integrated embedding configured (1) or not (0)
Telemetry Vector Count | Vector count for this index as reported via telemetry
Telemetry Index Fullness Percent | Fullness percentage for this index as reported via telemetry

## Notes

- The plugin retries transient network failures once before giving up, and applies an internal timeout budget so it always returns a result well within Site24x7's default 50-second script execution timeout.
- If `project_id` is left blank, or the Pinecone plan doesn't support Prometheus telemetry, the Telemetry, Serverless Operations, and Latency tabs will simply show zero values rather than causing the plugin to fail - core index health and capacity data is unaffected either way.
- Up to 25 indexes are reported in the Indexes child table per Site24x7's plugin table row limit; projects with more than 25 indexes will still have their totals correctly reflected in the Capacity tab, but only the first 25 will appear as individual rows.