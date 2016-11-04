Plugin for Hadoop NameNode Monitoring
=====================================

For monitoring the space metrics of your Hadoop NameNode setup using Site24x7 Server Monitoring Plugins. 
  
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu

Prerequisites
=============

Download hadoop plugin from https://github.com/site24x7/plugins/hadoop_namenode/hadoop_namenode.py
Place the plugin folder 'hadoop_namenode/hadoop_namenode.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configure the agent plugin
==========================
 
1. Make the following changes in the hadoop_namenode plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of HADOOP_HOST and HADOOP_PORT to match your configuration.
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report Hadoop NameNode statistics in the plugins tab under the site24x7.com portal.


Hadoop Plugin Attributes:
===========================

Some of the collected Hadoop attributes are as follows:

		'configured_capacity': Total amount of space configured for hadoop namenode, 
		'used_space': Amount of space already used, 
       'free_space': Remaining space available for use, 
       'percent_remaining': percentage of space remaining for use in namenode, 
       'total_blocks': Number of blocks currently been created in namenode, 
       'total_files': Total number of files in the namenode,
       'missing_blocks': Total number of blocks missing in the namenode,
       'number_of_threads': Number of threads currently running in the namenode  