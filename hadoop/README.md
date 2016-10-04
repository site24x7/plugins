
Plugin for Hadoop Monitoring
============================

For monitoring the performance metrics of your Hadoop setup using Site24x7 Server Monitoring Plugins. 
  

Prerequisites
=============

Download hadoop plugin from https://github.com/site24x7/plugins/hadoop/hadoop.py
Place the plugin folder 'hadoop/hadoop.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configure the agent plugin
==========================
 
1. Make the following changes in the activemq plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of HADOOP_HOST and HADOOP_PORT to match your configuration.
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report Hadoop statistics in the plugins tab under the site24x7.com portal.


Hadoop Plugin Attributes:
===========================

Some of the collected Hadoop attributes are as follows:

		"total_load" : Measure of file access across all DataNodes
		"missing_blocks" : Number of missing blocks.
		"corrupt_blocks" : Number of corrupt blocks.

