Plugin for Oracle Weblogic Server 12c Monitoring
================================================

For monitoring the performance metrics of your Weblogic setup using Site24x7 Server Monitoring Plugins. 
  
### Author: Krishnaraj, Zoho Corp
### Language : Python
### Tested in Ubuntu

Prerequisites
=============

Download weblogic plugin from https://github.com/site24x7/plugins/weblogic/weblogic.py
Place the plugin folder 'weblogic/weblogic.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configure the agent plugin
==========================
 
1. Make the following changes in the weblogic plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of WEBLOGIC_HOST, WEBLOGIC_PORT, WEBLOGIC_USERNAME and WEBLOGIC_PASSWORD to match your configuration.
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report Weblogic statistics in the plugins tab under the site24x7.com portal.


Weblogic Plugin Attributes:
===========================

Some of the collected Weblogic attributes are as follows:

		"heap_size_current" : The current size of Java heap memory in GB.
		
		The health status of all the servers.
		Note: Whenever a new server is added, the PLUGIN_VERSION needs to be incremented by 1.

