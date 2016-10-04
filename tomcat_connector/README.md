Plugin for Tomcat Monitoring
=============================

For monitoring the performance metrics of your Tomcat server using Site24x7 Server Monitoring Plugins. 
  

PreRequisites
======================

Download tomcatConnector plugin from https://github.com/site24x7/server-plugins/tomcatConnector/tomcatConnector.py
Place the plugin folder ‘tomcatConnector/tomcatConnector.py’ under agent plugins directory (/opt/site24x7/monagent/plugins/)


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

name  - Connector name
thread_count  - Total number of threads
thread_busy  - Busy threads count
thread_allowed - total number of threads allowed
bytes_received - number of bytes received
bytes_sent  - number of bytes sent
error_count - number of errors
processing_time - time taken for processing the request
request_count - number of requests
