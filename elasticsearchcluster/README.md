Plugin for monitoring your Elasticsearch cluster
================================================

For monitoring the performance metrics of your Elasticsearch cluster using Site24x7 Server Monitoring Plugins. 
  
### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu

Before you start
======================

1. Have the site24x7 server monitoring agent up and running.
2. Download the plugin from github https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/
3. Create a folder in name of the plugin under agent plugins directory (/opt/site24x7/monagent/plugins/)
4. Place the plugin inside the folder 


Configure the agent plugin
==========================
 
Make the following changes in the escluster plugin file ( copied to agent's plugin directory earlier ).

- Replace the shebang character "#!" in line1 to the appropriate path for python in your system.
		#!/usr/bin/python2
- Change the values of url, username, password according to your Elasticsearch cluster's hostname and port.

- Save the changes and restart the agent.
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report Elasticsearch cluster statistics in the plugins tab under the site24x7.com portal.

For further monitoring all your Elasticsearch nodes, we suggest adding our linux server monitoring agent in each node.


ESCluster Attributes:
=====================

	active_primary_shards: number of primary shards in the cluster
	active_shards: an aggregate total of all shards across all indices, which includes replica shards
	cluster_name: Name of the cluster
	delayed_unassigned_shards: number of currently active connections
	initializing_shards: number of shards that are being freshly created
	number_of_data_nodes: number of data nodes in the cluster
	number_of_nodes: number of nodes in a cluster
	relocating_shards: number of shards that are currently moving from one node to another node
	status: Status of the cluster Red : 0 , Green : 1, Yellow : 2
	unassigned_shards: number of shards in the cluster state, but cannot be found in the cluster itself        

Overall Elasticsearch Cluster Attributes:
=========================================

Some of the collected elasticsearch cluster attributes across all nodes are as follows:
		
- Status:
		
        "status" : Will have a value of either 0(Red), 1(Green) or 2(Red) which represents the status of your cluster.
		
- Nodes :
        
        "num_nodes" : Number of nodes in your cluster.
		 "num_data_nodes" : Number of data nodes in your cluster.

- Shards :
		
        "active_prim_shards" : Number of primary shards in your cluster
		 "active_shards" : Aggregate total of all shards across all indices, which includes replica shards.
		 "relocating_shards" : Shows the number of shards that are currently moving from one node to another node.
		 "init_shards" : Count of shards that are being freshly created.
		 "unassigned_shards" :  Shards that exist in the cluster state, but cannot be found in the cluster itself

- JVM stats across all nodes :
		
        "jvm_mem_pool_old_used_perc" : Average of each node's JVM memory usage % of old generation in the GC.
		 "jvm_gc_old_coll_time" : Garbage collection time (in millis) of old generation in all the nodes since last poll (5 minutes by default).
		"jvm_gc_old_coll_count" : Garbage collection count of old generation in all the nodes since last poll (5 minutes by default).

- Indices stats across all nodes:
		
        "query_latency" : The ratio between the amount of time spent on queries and the total number of queries. High value of this metric can be an indicator of lower efficiency of your queries.
		 "fetch_to_query_ratio" : Ratio of time spent in fetching the queries to the time spent in querying. High value of this metric can be an indicator of slow disks or very large documents being fetched.

- Disk i/o stats across all nodes :
		
        "disk_write_read_ratio" : The ratio of disk write operations to disk read operations. High value of this metric can be an indicator for requirement of indexing optimizations.

We recommend having a look at the following Elastisearch API docs for better understanding of the above metrics and their significance
`https://www.elastic.co/guide/en/elasticsearch/guide/master/_cluster_health.html`
`https://www.elastic.co/guide/en/elasticsearch/guide/master/_monitoring_individual_nodes.html`


Attributes : Node Details of a Elasticsearch Cluster:
======================================================

	host: ESCluster Host
	transport_address: ESCluster address
	cpu_used: CPU Used
    cpu_percent: CPU Used Percent
    mem_used: Memory Used
    mem_free: Memory Free
    resident_mem: Resident Memory in Bytes
    shared_mem: Shared Memory in Bytes
    vitual_mem: Total Virtual Memory in Bytes


### Changes in the plugin will be reflected in Site24x7 only when there is a change in plugin_version.

### HEARTBEAT - false : Site24x7 will alert as down only when plugin status is down
### HEARTBEAT - true  : Site24x7 will alert as down 1. When plugin status is down 2. When there is no data from plugin


Learn more about the plugin installation steps and the various performance metrics that you can monitor in https://www.site24x7.com/plugins.html        