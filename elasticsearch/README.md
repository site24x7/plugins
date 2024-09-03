# Elasticsearch

Install and configure the Elasticsearch plugin to monitor the open source, distributed document store and search engine. It depends strongly on Apache Lucene, a full text search engine in Java. Keep a pulse on the performance of the Elasticsearch environment to ensure you are up to date with the internals of your working cluster.

Get to know how to configure the Elasticsearch plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Elasticsearch clusters.
                                                                                              
---

## Quick installation

If you're using Linux servers, use the Elasticsearch plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/installer/Site24x7ElasticSearchPluginInstaller.sh && sudo bash Site24x7ElasticSearchPluginInstaller.sh
```

## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python version 3 or higher

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
  
	```bash
	[elasticsearch]
	host = "localhost"
	port = "9200"
	username = "elasticsearch_username"
	password = "elasticsearch_password"
	ssl_option = "No" #Yes if you are using https
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

## Supported Metrics

- **CPU used (%)**

- **OS memory free(%)**

- **OS memory used(%)**

- **CPU used (%)**
 
- **Total queries**

- **Time spent on queries**

- **Queries in progress**

- **Number of fetches**

- **Time spent on fetches**

- **Fetches in progress**
    
- **Documents indexed**

- **Time of indexing documents**

- **Documents currently indexed**

- **Index refreshes**

- **Time spent on refreshing indices**

- **Index flushes to disk**
    
- **Time spent on flushing indices to disk**

- **Indices docs count**

- **Indices docs deleted**

- **HTTP connections currently open**

- **HTTP connections opened over time**

- **Cluster Name**
    
- **Cluster status**

- **Number of Nodes**

- **Initializing shards**

- **Unassigned shards**

- **Active primary shards**

- **Relocating shards**

- **Delayed unassigned shards**

- **Number of GET requests where the document was missing**

- **Total time on GET requests where the document was missing**
  
- **JVM heap memory used (%)**

- **JVM heap memory committed**

- **JVM garbage collector old generation count**

- **JVM garbage collector old generation time**

- **Average JVM memory usage in garbage collector(%)**

- **Fetch to query ratio**

- **Latency of the query**

- **Queries hit count**

- **Query cache memory size**

- **Query cache miss count**

- **Request cache hit count**

- **Number of evictions**

- **Request cache memory size**



