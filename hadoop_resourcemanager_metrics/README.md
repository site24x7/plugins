Resource Manager cluster Metrics Plugin:
================================

The ResourceManager REST API's allow the user to get information about the cluster - status on the cluster, metrics on the cluster, scheduler information, information about nodes in the cluster, and information about applications on the cluster.

The cluster information resource provides overall information about the cluster. 

For monitoring the metrics of resource manager cluster setup using Site24x7 Server Monitoring Plugins. 
  
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu

Resource Manager Cluster Metrics Plugin installation
=============

Download hadoop plugin from https://github.com/site24x7/plugins/hadoop_resourcemanager_metrics/hadoop_resourcemanager_metrics.py
Place the plugin folder 'hadoop_resourcemanager_metrics/hadoop_resourcemanager_metrics.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)

Commands to perform the above steps:

	cd /opt/site24x7/monagent/plugins/
	mkdir hadoop_resourcemanager_metrics
	cd hadoop_resourcemanager_metrics
	wget https://raw.githubusercontent.com/site24x7/plugins/master/hadoop_resourcemanager_metrics/hadoop_resourcemanager_metrics.py


Configure the agent plugin
==========================
 
1. Make the following changes in the hadoop_resourcemanager_metrics.py plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of HADOOP_HOST and HADOOP_PORT to match your configuration.
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report hadoop resource manager statistics in the plugins tab under the site24x7.com portal.

For more information kindly refer to the following url,
[https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Information_API](url "ResourceManager cluster metrics") 


Resource Manager Plugin Attributes:
===========================

Sample result of the above plugin,
		
###### {
		    "activeNodes": 1,
		    "allocatedMB": 0,
		    "allocatedVirtualCores": 0,
		    "appsCompleted": 5,
		    "appsFailed": 0,
		    "appsKilled": 0,
		    "appsPending": 0,
		    "appsRunning": 0,
		    "appsSubmitted": 5,
		    "availableMB": 8192,
		    "availableVirtualCores": 8,
		    "containersAllocated": 0,
		    "containersPending": 0,
		    "containersReserved": 0,
		    "decommissionedNodes": 0,
		    "lostNodes": 0,
		    "rebootedNodes": 0,
		    "reservedMB": 0,
		    "reservedVirtualCores": 0,
		    "totalMB": 8192,
		    "totalNodes": 1,
		    "totalVirtualCores": 8,
		    "unhealthyNodes": 0,
		    "units": {
		        "allocatedMB": "MB",
		        "allocatedVirtualCores": "Units",
		        "appsCompleted": "Units",
		        "appsPending": "Units",
		        "appsSubmitted": "Units",
		        "availableMB": "MB",
		        "availableVirtualCores": "Units",
		        "totalMB": "MB",
		        "totalNodes": "Units",
		        "totalVirtualCores": "Units"
		    }
		}

where the detailed explanation of each attribute can be found here,
[https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Metrics_API](https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Metrics_API "metric details") 

Monitoring additional metrics:
==============================
To monitor additional metrics, edit the "hadoop\_resourcemanager\_metrics.py" file and add the new metrics that need monitoring
 
Increment the plugin version value in the file "hadoop\_resourcemanager\_metrics.py" to view the newly added metrics ( For e.g. Change the default plugin version from PLUGIN_VERSION = "1" to "PLUGIN_VERSION = "2") 


		 