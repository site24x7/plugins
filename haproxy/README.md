
Plugin for Haproxy Monitoring
=============================

For monitoring the performance metrics of your Haproxy setup using Site24x7 Server Monitoring Plugins. 
  

PreRequisites
======================

Download haproxy plugin from https://github.com/site24x7/server-plugins/haproxy/haproxy.py
Place the plugin folder 'haproxy/haproxy.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Our plugin requires Python version 3 and above to fetch the statistics. Have this installed to use this feature.


Configure Haproxy to support statistics
=======================================

1. Edit your /etc/haproxy/haproxy.cfg file and add the following code in the bottom to listen for stats:
 
		listen appname 0.0.0.0:80#to listen for stats on port number 80
			mode http
			stats enable#to enable haproxy stats
			stats uri /haproxy?stats#URL where stats will be displayed
			stats realm Strictly\ Private#Authentication realm. Specify this value without #escape character in plugin file
			stats auth userName:password         #Setup authentication credentials here

2. Save the changes and restart haproxy (take caution while restarting in production servers).
 
		/etc/init.d/haproxy restart



Configure the agent plugin
==========================
 
1. Now make the following changes in the haproxy plugin file ( copied to agent's plugin directory earlier ).
 
	Replace the shebang character "#!" in line1 to the appropriate path for python3 in your system. Eg : 
		#!/usr/local/bin/python3
	Change the values of url, username, password and realm to corresponding values as specified in the haproxy config file in step 1.
	Please make sure you retain the ";csv" prefix at the end of the URL.Required for agent to fetch statistics from the URL.
 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report haproxy statistics in the plugins tab under the site24x7.com portal.


Haproxy Plugin Attributes:
==========================

Some of the collected haproxy attributes are as follows:

		"sessions-total" : Total number of sessions
		"request-errors" : Total number of request errors
		"bytes-in" : Total number of bytes recieved (last 5 seconds).
		"bytes-out" : Total number of bytes sent (last 5 seconds).
		"sessions-active-current" : Total number of current active sessions
		"requests-queue-current" : Total number of currently queued requests
		"servers-active" : Number of active servers
		"sessions-rate-current" : Number of sessions per second over last elapsed second
		"status" : Current status

