# Weaviate Monitoring

Weaviate is an open-source vector database designed for AI-native applications such as semantic search, Retrieval-Augmented Generation (RAG), and recommendation systems. This plugin monitors Weaviate cluster health, collection and node topology, object and shard counts, REST/GraphQL API latency, and process-level metrics exposed via Prometheus.

---

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux Server Monitoring agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) on the server where Weaviate is running.

- Weaviate **v1.14 or later** is required for the `/v1/nodes` API endpoint.

---

## Enable Prometheus Metrics in Weaviate

The plugin collects process, memory, and Go runtime metrics from Weaviate's built-in Prometheus endpoint (default port `2112`). Prometheus monitoring must be explicitly enabled before the plugin can collect those metrics.

### Docker Compose

Add the following environment variables to your Weaviate service and expose port `2112`:

```yaml
services:
  weaviate:
    environment:
      PROMETHEUS_MONITORING_ENABLED: "true"
      PROMETHEUS_MONITORING_GROUP: "true"
    ports:
      - "2112:2112"
```

Restart the container.

Verify the Prometheus endpoint is live:

	curl http://localhost:2112/metrics

### Standalone Binary

Set the environment variables before starting Weaviate:

	export PROMETHEUS_MONITORING_ENABLED=true
	export PROMETHEUS_MONITORING_GROUP=true
	./weaviate --config-file=weaviate.yaml

## Authentication

### Anonymous Access (Default)

If your Weaviate instance has anonymous access enabled, no credentials are needed. Leave `api_key` blank in the plugin configuration.

	AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "true"

### API Key Authentication

If API key authentication is enabled, provide a key with **read-only** access.
---

## Plugin Installation

### Linux

1. Create a directory named `Weaviate_monitoring`:

		mkdir Weaviate_monitoring
		cd Weaviate_monitoring/

2. Download the plugin files:

		wget https://raw.githubusercontent.com/site24x7/plugins/master/weaviate/Weaviate_monitoring/Weaviate_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/weaviate/Weaviate_monitoring/Weaviate_monitoring.cfg

3. Run the plugin manually to verify the JSON output:

		python3 Weaviate_monitoring.py --host 'localhost' --port '8080' --metrics_port '2112' --api_key '' --ssl 'false' --insecure 'false'

4. Provide your Weaviate connection details in `Weaviate_monitoring.cfg`:

		[global_configurations]
		use_agent_python=1

		[Weaviate_monitoring]
		host = "localhost"
		port = "8080"
		metrics_port = "2112"
		api_key = ""
		ssl = "false"
		insecure = "false"

5. Move the directory to the Site24x7 Linux agent plugin folder:

		mv Weaviate_monitoring /opt/site24x7/monagent/plugins/

---

### Windows

1. Create a directory named `Weaviate_monitoring`.

2. Download the files [Weaviate_monitoring.py](https://raw.githubusercontent.com/site24x7/plugins/master/weaviate/Weaviate_monitoring/Weaviate_monitoring.py) and [Weaviate_monitoring.cfg](https://raw.githubusercontent.com/site24x7/plugins/master/weaviate/Weaviate_monitoring/Weaviate_monitoring.cfg) and place them inside the `Weaviate_monitoring` directory.

3. Since this is a Python plugin, follow the steps in [this guide](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers) to configure Python plugins on Windows servers.

4. Install the required Python packages:

		pip install requests urllib3

5. Run the plugin manually in Command Prompt to verify the JSON output:

		python Weaviate_monitoring.py --host "localhost" --port "8080" --metrics_port "2112" --api_key "" --ssl "false" --insecure "false"

6. Provide your Weaviate connection details in `Weaviate_monitoring.cfg`:

		[Weaviate_monitoring]
		host = "localhost"
		port = "8080"
		metrics_port = "2112"
		api_key = ""
		ssl = "false"
		insecure = "false"

7. Move the `Weaviate_monitoring` folder to the Site24x7 Windows agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\Weaviate_monitoring

The agent will automatically execute the plugin within five minutes and the monitor will appear under **Site24x7 > Plugins > Plugin Integrations**.

---

## Configuration Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `host` | Hostname or IP address of the Weaviate instance | `localhost` |
| `port` | Weaviate REST API port | `8080` |
| `metrics_port` | Weaviate Prometheus metrics port | `2112` |
| `api_key` | API key for authentication (leave blank if anonymous access is enabled) | `` |
| `ssl` | Set to `true` to connect using HTTPS | `false` |
| `insecure` | Set to `true` to skip SSL certificate verification | `false` |

---

## Supported Metrics

### Cluster Overview

Name					|	Unit		|	Description
---					|	---		|	---
Node Count				|	nodes		|	Total number of active nodes in the Weaviate cluster
Collection Count			|	collections	|	Number of collections (classes) defined in the Weaviate schema
Object Count				|	objects		|	Total number of objects stored across all nodes in the cluster
Shard Count				|	shards		|	Total number of shards across all nodes in the cluster

### Performance

Name					|	Unit		|	Description
---					|	---		|	---
GraphQL Response Time			|	ms		|	Time taken for a GraphQL query to respond — returns `-1` when no schema is defined

### Process & Memory

Name					|	Unit		|	Description
---					|	---		|	---
Memory Usage				|	MB		|	Resident set size (RSS) — physical memory currently used by the Weaviate process
Virtual Memory				|	MB		|	Total virtual memory allocated to the Weaviate process
Heap Alloc				|	MB		|	Currently allocated heap memory used by live Go objects
Heap Sys				|	MB		|	Total heap memory obtained from the OS by the Go runtime
CPU Seconds				|	s		|	Cumulative CPU time consumed by the Weaviate process since startup
Open File Descriptors			|	fds		|	Number of file descriptors currently open by the Weaviate process
Max File Descriptors			|	fds		|	Maximum number of file descriptors the process is allowed to open

### Go Runtime

Name					|	Unit		|	Description
---					|	---		|	---
Goroutines				|	goroutines	|	Number of goroutines currently running inside the Weaviate process
OS Threads				|	threads		|	Number of OS-level threads created by the Go runtime
GC Pause Duration			|	ms		|	Cumulative time the Go garbage collector has paused the application since startup
Heap Objects				|	objects		|	Number of allocated heap objects currently tracked by the Go runtime

### Additional Attributes

Name					|	Description
---					|	---
Weaviate Version			|	Weaviate server version currently running (e.g. `1.26.4`)

### Collection Details

Name					|	Description
---					|	---
name					|	Name of the collection (class) in the Weaviate schema
Vectorizer				|	Vectorizer module configured for this collection (`none` if externally vectorized)
Description				|	Description of the collection as defined in the schema

### Node Details

Name					|	Description
---					|	---
name					|	Unique identifier of the node within the Weaviate cluster
Object_Count				|	Total number of objects stored on this node
Shard_Count				|	Number of shards hosted on this node
Node Status				|	Node health status reported by Weaviate (`HEALTHY`, `UNAVAILABLE`, etc.)

### Shard Details

Name					|	Description
---					|	---
name					|	Shard identifier in the format `Collection / ShardID (NodeName)`
Object_Count				|	Number of objects stored within this shard

---