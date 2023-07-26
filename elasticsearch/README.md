# Elasticsearch

Install and configure the Elasticsearch plugin to monitor the open source, distributed document store and search engine. It depends strongly on Apache Lucene, a full text search engine in Java. Keep a pulse on the performance of the Elasticsearch environment to ensure you are up to date with the internals of your working cluster.

Get to know how to configure the Elasticsearch plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Elasticsearch clusters.
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

---


### Plugin Installation  

- Create a directory named "elasticsearch".
      
- Download all the files in the "elasticsearch" folder and place it under the "elasticsearch" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/elasticsearch.cfg
		wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/elasticsearch.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the elasticsearch.py script.
		
- Since it's a python plugin, to run in windows server please follow the steps given [here](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers), remaining configuration steps are exactly the same. 


- Execute the below command with appropriate arguments to check for the valid json output:

		python3 elasticsearch.py --host=<host name> --port=<port no> --node_name=<node name> --username=<elasticsearch username> --password=<elasticsearch password> --sslpath=<ssl file path> --ssl=<ssl option("YES/NO")>

### Configurations

- Provide your elasticsearch configurations elasticsearch.cfg file.
```
[elasticsearch]
host = <ELASTICSEARCH_HOST>
port = <ELASTICSEARCH_PORT>
node_name=<ELASTICSEARCH_NODE_NAME>
username=<ELASTICSEARCH_USERNAME>
password = <ELASTICSEARCH_PASSWORD>
sslpath= <ELASTICSEARCH_SSL_PATH>
ssl=<ELASTICSEARCH_SSL_OPTION>
logs_enabled = "false"
log_type_name = None
log_file_path = None
```	
	
  
- Move the directory "elasticsearch" under the Site24x7 Linux Agent plugin directory: 

		Linux       ->  /opt/site24x7/monagent/plugins/elasticsearch
		
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



