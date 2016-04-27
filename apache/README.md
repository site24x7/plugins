
Plugin for Apache Monitoring
=============================

For monitoring the performance metrics of your Apache server using Site24x7 Server Monitoring Plugins. 
  

PreRequisites
====================

Download apache plugin from https://github.com/site24x7/server-plugins/apache/apache.py
Place the plugin folder 'apache/apache.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Our plugin requires Python version 3 and above to fetch the statistics. Have this installed to use this feature.


Configure Apache to support statistics
=======================================

1. Edit your httpd.conf file so that it enables sending statistics. As mentioned at 
	https://httpd.apache.org/docs/2.4/mod/mod_status.html#machinereadable

2. Sample code for stats setup in the file "/usr/local/apache/conf/httpd.conf":

		<Location /server-status>
			SetHandler server-status
			Order deny,allow
			Deny from all
 
			Allow from 127.0.0.1 ::1
		</Location>

3. Restart apache server and check wether the configured URL is receiving apache statistics by opening it in a browser.



Configure the agent plugin
==========================
 
1. Now make the following changes in the apache plugin file ( copied to agent's plugin directory earlier ).
 
	Replace the shebang character "#!" in line 1 to the appropriate path for python3 in your system. Eg : 
		#!/usr/local/bin/python3
	Change the value of global variable "url" to the value configured in above steps. Eg : 
		url = "http://localhost:80/server-status?auto"
	Please retain the "?auto" suffix at the end as this is required.
	 
2. Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report apache statistics in the plugins tab under the site24x7.com portal.


Apache Plugin Attributes:
==========================

Some of the collected apache attributes are as follows:

		"total_accesses" : The total number of accesses of your apache server
		"total_kbytes" : The total number of bytes count served by your apache server
		"cpu_load" : The current percentage of CPU used by all apache worker threads combined
		"uptime" : The running time of the server
		"req_per_sec" : Average number of requests per second
		"bytes_per_sec" : Average number of bytes served per second
		"bytes_per_req" : Average number of bytes per request
		"busy_workers" : The number of workers serving requests
		"idle_workers" : The number of idle workers


