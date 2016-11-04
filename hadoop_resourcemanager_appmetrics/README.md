Resource Manager APP Metrics Plugin
====================================

The ResourceManager REST API's allow the user to get information about the cluster - status on the cluster, metrics on the cluster, scheduler information, information about nodes in the cluster, and information about applications on the cluster.

An application resource contains information about a particular application that was submitted to a cluster.  

For monitoring the metrics of a node in  resource manager cluster setup, using Site24x7 Server Monitoring Plugins.

For more info, refer to [Application API](https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Application_API "app metrics")  
  
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu


Resource Manager APP Metrics Plugin installation
=============

Download resource manager appmetrics plugin from https://github.com/site24x7/plugins/hadoop\_resourcemanager\_appmetrics/hadoop\_resourcemanager\_appmetrics.py

Place the plugin folder 'hadoop\_resourcemanager\_appmetrics/hadoop\_resourcemanager\_appmetrics.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)

Commands to perform the above steps:

	cd /opt/site24x7/monagent/plugins/
	mkdir hadoop_resourcemanager_appmetrics
	cd hadoop_resourcemanager_appmetrics
	wget https://raw.githubusercontent.com/site24x7/plugins/master/hadoop_resourcemanager_appmetrics/hadoop_resourcemanager_appmetrics.py


Configure the agent plugin
==========================
 
1. Make the following changes in the hadoop\_resourcemanager\_appmetrics.py plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of HADOOP_HOST and HADOOP_PORT and APP_ID to match your configuration.
	
	Change the APP_ID to the app for which the metrics has to be retrived. Details regaring the app info can be found here 
	(https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Applications_API) 
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report hadoop resource manager application statistics in the plugins tab under the site24x7.com portal.

For more information kindly refer to the following url,
[Appliction Info API](https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Application_API "app Info API") 


Resource Manager Plugin Attributes:
===========================

Sample result of the above plugin,
		
	{
    "allocatedMB": -1,
    "allocatedVCores": -1,
    "elapsedTime": 63545,
    "memorySeconds": 482735,
    "preemptedResourceMB": 0,
    "preemptedResourceVCores": 0,
    "progress": 100.0,
    "runningContainers": -1,
    "units": {
        "allocatedMB": "MB",
        "elapsedTime": "ms",
        "memorySeconds": "ms",
        "preemptedResourceMB": "MB",
        "progress": "%",
        "vcoreSeconds": "ms"
    }
	}
	
Monitoring additional metrics:
==============================
To monitor additional metrics, edit the "hadoop\_resourcemanager\_appmetrics.py" file and add the new metrics that need monitoring
 
Increment the plugin version value in the file "hadoop\_resourcemanager\_appmetrics.py" to view the newly added metrics ( For e.g. Change the default plugin version from PLUGIN_VERSION = "1" to "PLUGIN_VERSION = "2") 


		 