
Plugin for Apache ActiveMQ Monitoring
=====================================

For monitoring the performance metrics of your ActiveMQ setup using Site24x7 Server Monitoring Plugins. 
  

Prerequisites
=============

Download activemq plugin from https://raw.githubusercontent.com/site24x7/plugins/master/activemq/activemq.py
Place the plugin folder 'activemq/activemq.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configure the agent plugin
==========================
 
1. Make the following changes in the activemq plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of ACTIVEMQ_HOST, ACTIVEMQ_PORT, ACTIVEMQ_USERNAME and ACTIVEMQ_PASSWORD to match your configuration.
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report ActiveMQ statistics in the plugins tab under the site24x7.com portal.


ActiveMQ Plugin Attributes:
===========================

Some of the collected ActiveMQ attributes are as follows:

		"total_message_count" : Total number of messages in queue
		"total_connections_count" : Total number of connections.
		"total_consumer_count" : Total number of consumers.
		"total_producer_count" : Total number of producers.

