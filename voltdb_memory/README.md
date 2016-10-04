Plugin for VoltDB Monitoring
=============================

For monitoring the performance metrics of your VoltDB using Site24x7 Server Monitoring Plugins. 
  

PreRequisites
===============

Download volt_memory plugin from https://github.com/site24x7/server-plugins/voltMemory/voltMemory.py
Place the plugin folder ‘voltMemory/voltMemory.py’ under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configure Voltdb plugin to support statistics
=======================================

1. voltdbclient.py file must also be downloaded from https://github.com/site24x7/server-plugins/voltMemory/ and placed inside plugins folder


Configure the agent plugin
==========================
 
1. Now make the following changes in the voltdb plugin file ( copied to agent's plugin directory earlier ).
 
	Replace the shebang character "#!" in line 1 to the appropriate path for python in your system. Eg : 
		#!/usr/local/bin/python3

2. You can configure the following for the plugin
	VOLTDB_HOST = 'localhost'

	VOLTDB_PORT = '21212'

	 
3. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report voltdb statistics in the plugins tab under the site24x7.com portal.


Voltdb Plugin Attributes:
==========================

Some of the collected voltdb attributes are as follows:
RSS - RSS of the table
java_used - Used memory for java
java_unused - Available memory for java
tuple_used_mem - Used memory of data
tuple_alloc_mem - Allocated memory for tuples
tuple_count - number of tuples
pooled_mem - pooled memory
max_heap_java - max heap memory of java
indexed_mem - indexed memory 
