Plugin for Tomcat Monitoring
=============================

For monitoring the performance metrics of your Tomcat server using Site24x7 Server Monitoring Plugins. 
  

PreRequisites
======================

Download tomcatOverallmemory plugin from https://github.com/site24x7/server-plugins/tomcatOverallmemory/tomcatOverallmemory.py
Place the plugin folder ‘tomcatOverallmemory/tomcatOverallmemory.py’ under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configure Tomcat to support statistics
=======================================

1. Edit your tomcat-users.xml file to provide access to /manager url 


Configure the agent plugin
==========================
 
1. Now make the following changes in the tomcat plugin file ( copied to agent's plugin directory earlier ).
 
	Replace the shebang character "#!" in line 1 to the appropriate path for python in your system. Eg : 
		#!/usr/local/bin/python3

2. You can configure the following for the plugin
	TOMCAT_HOST = 'localhost'

	TOMCAT_PORT = '8080'

	TOMCAT_USERNAME = 'admin'

	TOMCAT_PASSWORD = 'admin'

	TOMCAT_URL = '/manager'

	TOMCAT_CONNECTOR = 'http-nio-8080'

	TOMCAT_TIMEOUT = '5'

	 
3. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report tomcat statistics in the plugins tab under the site24x7.com portal.


Tomcat Plugin Attributes:
==========================

Some of the collected tomcat attributes are as follows:
free_memory - total free memory
total_memory - total memory
max_memory - max memory allowed
available_memory - free memory
used_memory - used memory
percent_used_memory - used memory percent
