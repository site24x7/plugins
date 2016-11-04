
Plugin for Hadoop DataNode Monitoring
=====================================

For monitoring the space metrics of your Hadoop datanode setup using Site24x7 Server Monitoring Plugins. 
  
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu


Hadoop DataNode plugin installation
===================================

Create a directory with the name "hadoop\_datanode", under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/hadoop\_datanode

Download the file ["hadoop\_datanode.py" from our GitHub repository](https://github.com/site24x7/plugins/tree/master/hadoop\_datanode "")  and place it under the "hadoop\_datanode" directory

Commands to perform the above steps:

	cd /opt/site24x7/monagent/plugins/
	mkdir hadoop_datanode
	cd hadoop_datanode
	wget https://raw.githubusercontent.com/site24x7/plugins/master/hadoop_datanode/hadoop_datanode.py


Configure the agent plugin
==========================
 
1. Make the following changes in the hadoop\_datanode plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of HADOOP_HOST and HADOOP_PORT to match your configuration.
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report Hadoop DataNode statistics in the plugins tab under the site24x7.com portal.


Hadoop DataNode Plugin Attributes:
===========================

Some of the collected Hadoop attributes are as follows:

		"total_space_" : Measure of total space in the datanode 
       "remaining_space_": Measure of remaining space available in the datanode 
      	"dfs_used_space_": Measure of used space in the datanode 
       "non_dfs_used_space_": Measure of space used by others
       and it also monitors blocks w.r.t cache details  
       
Monitoring additional metrics:
==============================
To monitor additional metrics, edit the "hadoop\_datanode.py" file and add the new metrics that need monitoring
 
Increment the plugin version value in the file "hadoop\_datanode.py" to view the newly added metrics ( For e.g. Change the default plugin version from PLUGIN_VERSION = "1" to "PLUGIN_VERSION = "2") 