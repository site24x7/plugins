
Plugin for Varnish Cache Monitoring
===================================

For monitoring the performance metrics of your Varnish setup using Site24x7 Server Monitoring Plugins. 
  

Prerequisites
=============

Download varnish plugin from https://github.com/site24x7/plugins/varnish_cache/varnish_cache.py
Place the plugin folder 'varnish_cache/varnish_cache.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configure the agent plugin
==========================
 
1. Make the following changes in the varnish plugin file ( copied to agent's plugin directory earlier ).
 
	Change the values of VARNISH_HOST and VARNISH_PORT to match your configuration.
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report Varnish statistics in the plugins tab under the site24x7.com portal.


Varnish Plugin Attributes:
==========================

Some of the collected Varnish attributes are as follows:

		"cache_hit" : Cache hits.
		"cache_miss" : Cache misses.
		"n_wrk_create" : Number of worker threads created.
		"n_wrk_queued" : Number of queued work requests.
		"sess_pipe_overflow" : Dropped sessions due to session pipe overflow.

