Resource Manager Node Metrics Plugin
====================================

The ResourceManager REST API's allow the user to get information about the cluster - status on the cluster, metrics on the cluster, scheduler information, information about nodes in the cluster, and information about applications on the cluster.

A node resource contains information about a node in the cluster.  

For monitoring the metrics of a node in  resource manager cluster setup, using Site24x7 Server Monitoring Plugins.

For more info, refer to [https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Node_API](https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Node_API "resource manager node metrics")  
  
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu


Prerequisites
=============

Download resource manager nodemetrics plugin from https://github.com/site24x7/plugins/hadoop_resourcemanager_nodemetrics/hadoop_resourcemanager_nodemetrics.py

Place the plugin folder 'hadoop_resourcemanager_nodemetrics/hadoop_resourcemanager_nodemetrics.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configure the agent plugin
==========================
 
1. Make the following changes in the hadoop_resourcemanager_metrics.py plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of HADOOP_HOST and HADOOP_PORT and NODE_ID to match your configuration.
	
	Change the Node Id to the node for which the metrics has to be retrived. Details regaring the node info can be found here 
	(https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Nodes_API) 
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report hadoop resource manager node statistics in the plugins tab under the site24x7.com portal.

For more information kindly refer to the following url,
[Node Info API](https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Node_API "Node Info API") 


Resource Manager Plugin Attributes:
===========================

Sample result of the above plugin,
		
###### {
    "availMemoryMB": 8192,
    "availableVirtualCores": 8,
    "lastHealthUpdate": 1477049600392,
    "numContainers": 0,
    "units": {
        "availMemoryMB": "MB",
        "availableVirtualCores": "units",
        "lastHealthUpdate": "ms",
        "numContainers": "units",
        "usedMemoryMB": "MB",
        "usedVirtualCores": "units"
    },
    "usedMemoryMB": 0,
    "usedVirtualCores": 0
}


where the detailed explanation of each attribute can be found here,
[attibute explanation](https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Node_API "attribute explanations") 


		 