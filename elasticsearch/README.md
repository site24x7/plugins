# Elasticsearch

Install and configure the Elasticsearch plugin to monitor the open source, distributed document store and search engine. It depends strongly on Apache Lucene, a full text search engine in Java. Keep a pulse on the performance of the Elasticsearch environment to ensure you are up to date with the internals of your working cluster.

Get to know how to configure the Elasticsearch plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Elasticsearch clusters.
                                                                                              
---

### Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python version 3 or higher
- Python packages required: `urllib3`, `requests`

Install them using the following commands:

```bash
pip3 install urllib3
```

```bash
pip3 install requests
```

## The connecting Elasticsearch user must have the following privileges:

### Cluster-Level Privileges:
- `monitor`
- `manage`

### Index-Level Privileges:
- `read`
- `monitor`
- `view_index_metadata`

## Quick installation

If you're using Linux servers, use the Elasticsearch plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/installer/Site24x7ElasticSearchPluginInstaller.sh && sudo bash Site24x7ElasticSearchPluginInstaller.sh
```

## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Plugin Installation  


- Create a directory named `elasticsearch`.

	```bash
	mkdir elasticsearch
 	cd elasticsearch/
	```
 
- Download all the files [elasticsearch.cfg](https://github.com/site24x7/plugins/blob/master/elasticsearch/elasticsearch.cfg), [elasticsearch.py](https://github.com/site24x7/plugins/blob/master/elasticsearch/elasticsearch.py) and place it under the `elasticsearch` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/elasticsearch.cfg
	wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/elasticsearch.py
	```

- Execute the below command with appropriate arguments to check for the valid json output:

	```bash
	python3 elasticsearch.py --host "host" --port "port no" --username "elasticsearch username" --password "elasticsearch password" --ssl_option "YES/NO"
	```
 
#### Configurations

- Provide your elasticsearch configurations elasticsearch.cfg file.

#### For Linux 
  
```bash
[global_configurations]
use_agent_python=1

[elasticsearch]
host = "localhost"
port = "9200"
username = "elasticsearch_username"
password = "elasticsearch_password"
ssl_option = "No" #True if you are using https
cafile = "None"
```

#### For Windows 
  
```bash
[elasticsearch]
host = "localhost"
port = "9200"
username = "elasticsearch_username"
password = "elasticsearch_password"
ssl_option = "No" #True if you are using https
cafile = "None"
```
 
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the elasticsearch.py script.

- Move the directory `elasticsearch` under the Site24x7 Linux Agent plugin directory: 

		mv elasticsearch /opt/site24x7/monagent/plugins/
#### Windows
		
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Move the folder `elasticsearch` under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins

		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---
# Elasticsearch Monitoring Plugin Metrics

## Summary

| **Metric Name**                                  | **Description**                                                              |
|--------------------------------------------------|------------------------------------------------------------------------------|
| Cluster Name                                     | Name of the Elasticsearch cluster.                                           |
| Cluster status                                   | Health status of the cluster (`green`, `yellow`, or `red`).                  |
| Number of Nodes                                  | Total number of nodes in the cluster.                                        |
| Number of data nodes                             | Number of nodes that store data in the cluster.                              |
| Initializing shards                              | Count of shards currently in the initializing state.                         |
| Unassigned shards                                | Number of shards that are currently not assigned to any node.               |
| Active primary shards                            | Number of active primary shards in the cluster.                              |
| Relocating shards                                | Count of shards that are currently being moved between nodes.                |
| Delayed unassigned shards                        | Number of shards delayed from being assigned due to allocation delays.       |
| JVM garbage collector old generation count       | Number of old generation garbage collection events.                          |
| JVM garbage collector old generation time        | Time spent in old generation garbage collection (in ms).                     |
| Average JVM memory usage in garbage collector(%) | Average percentage of memory used during garbage collection.                 |
| Status of the node                               | Numeric indicator of node status (1 = Available, 0 = Unavailable).           |
| Node Availability                                | Human-readable node availability status (e.g., "Available", "Unavailable").  |


## Search and Query Performance

| **Metric Name**                                              | **Description**                                                              |
|--------------------------------------------------------------|------------------------------------------------------------------------------|
| Total queries                                                | Total number of queries executed.                                           |
| Time spent on queries                                        | Cumulative time spent executing queries (in ms).                            |
| Queries in progress                                          | Number of queries currently in progress.                                    |
| Number of fetches                                            | Total number of fetch phases executed.                                      |
| Time spent on fetches                                        | Cumulative time spent on fetch phases (in ms).                              |
| Fetches in progress                                          | Number of fetches currently in progress.                                    |
| Queries hit count                                            | Number of queries that returned cached results.                             |
| Query cache memory size                                      | Memory used by the query cache.                                             |
| Query cache miss count                                       | Number of queries that resulted in cache misses.                            |
| Request cache hit count                                      | Number of request cache hits.                                               |
| Number of evictions                                          | Number of evictions from the query or request cache.                        |
| Request cache memory size                                    | Memory used by the request cache.                                           |
| Number of GET requests where the document was missing        | Count of GET requests for missing documents.                                |
| Total time on GET requests where the document was missing    | Time spent on GET requests for missing documents.                           |

## Index Performance

| **Metric Name**                          | **Description**                                                              |
|------------------------------------------|------------------------------------------------------------------------------|
| Documents indexed                        | Number of documents indexed.                                                |
| Time of indexing documents               | Cumulative time spent indexing documents (in ms).                           |
| Documents currently indexed              | Number of documents currently being indexed.                                |
| Index refreshes                          | Total number of index refreshes.                                            |
| Time spent on refreshing indices         | Time spent on index refresh operations (in ms).                             |
| Index flushes to disk                    | Number of index flushes.                                                    |
| Time spent on flushing indices to disk  | Time spent flushing index data to disk (in ms).                             |
| Indices docs count                       | Total number of documents across all indices.                               |
| Indices docs deleted                     | Number of documents deleted from indices.                                   |

## System Performance

| **Metric Name**                         | **Description**                                                              |
|-----------------------------------------|------------------------------------------------------------------------------|
| CPU used (%)                            | CPU usage percentage of the node.                                            |
| OS memory free(%)                       | Percentage of free system memory.                                            |
| OS memory used(%)                       | Percentage of system memory used.                                            |
| HTTP connections currently open         | Number of currently open HTTP connections.                                  |
| HTTP connections opened over time       | Total number of HTTP connections opened.                                    |
| JVM heap memory used (%)                | Percentage of heap memory used by the JVM.                                  |
| JVM heap memory committed               | Amount of memory committed to the JVM heap.                                 |

## Node Availability

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| name                        | Name of the Elasticsearch node.                                       |
| time_spent_on_queries     | Time spent on queries on this specific node.                   |
| queries_in_progress       | Number of queries currently running on this node.                      |
| number_of_fetches         | Number of fetch operations on this node.                               |
| documents_indexed         | Number of documents indexed on this node.                              |
| cpu_used                  | CPU usage percentage of this node.                                     |


## Sample images

![image](https://github.com/user-attachments/assets/c6ad2369-146d-4605-8ee9-1e762bd4cd81)

![image](https://github.com/user-attachments/assets/1545adf5-ec3d-491f-92e6-f6b152e990f1)

