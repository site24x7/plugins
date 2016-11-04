
Plugin for Hadoop DataNode Monitoring
=====================================

For monitoring the space metrics of your Hadoop datanode setup using Site24x7 Server Monitoring Plugins. 
  
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu

Prerequisites
=============

Download hadoop plugin from https://github.com/site24x7/plugins/hadoop_datanode/hadoop_datanode.py
Place the plugin folder 'hadoop_datanode/hadoop_datanode.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configure the agent plugin
==========================
 
1. Make the following changes in the hadoop_datanode plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of HADOOP_HOST and HADOOP_PORT to match your configuration.
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report Hadoop DataNode statistics in the plugins tab under the site24x7.com portal.


Hadoop Plugin Attributes:
===========================

Some of the collected Hadoop attributes are as follows:

		"total_space_" : Measure of total space in the datanode 
       "remaining_space_": Measure of remaining space available in the datanode 
      	"dfs_used_space_": Measure of used space in the datanode 
       "non_dfs_used_space_": Measure of space used by others
       and it also monitors blocks w.r.t cache details  