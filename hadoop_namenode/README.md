Plugin for Hadoop NameNode Monitoring
=====================================

For monitoring the space metrics of your Hadoop NameNode setup using Site24x7 Server Monitoring Plugins. 
  
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu



Hadoop NameNode plugin installation
===================================

Create a directory with the name "hadoop\_namenode", under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/hadoop\_namenode

Download the file ["hadoop_namenode.py" from our GitHub repository](https://github.com/site24x7/plugins/tree/master/hadoop_namenode "")  and place it under the "hadoop_namenode" directory

Command to perform the above steps:

	cd /opt/site24x7/monagent/plugins/
	mkdir hadoop_namenode
	cd hadoop_namenode
	wget https://raw.githubusercontent.com/site24x7/plugins/master/hadoop_namenode/hadoop_namenode.py


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
       
Monitoring additional metrics:
==============================
To monitor additional metrics, edit the "hadoop\_namenode.py" file and add the new metrics that need monitoring
 
Increment the plugin version value in the file "hadoop\_namenode.py" to view the newly added metrics ( For e.g. Change the default plugin version from PLUGIN_VERSION = "1" to "PLUGIN_VERSION = "2") 