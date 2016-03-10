
Plugin for Monitoring wordpress servers
=======================================

For monitoring the performance metrics of your Wordpress servers using Site24x7 Server Monitoring Plugins. 
  

PreRequisites
=============

Download wordpress plugin from https://github.com/site24x7/server-plugins/wordpress/wordpress.sh
Place the plugin folder 'wordpress/wordpress.sh' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Our plugin requires 'Curl' tool to fetch the statistics. Have this installed to use this feature.


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


1. Now change the following values in the plugin file (copied to agent plugin's directory earlier):
	"APACHE_STATS" to "ENABLED" ("DISABLED" by default)

2. Enter your stats URL as added in httpd.conf file in previous step to the variable "APACHE_STATUS_URL".
	The final stats URL should contain "?auto" in the end as this is required to fetch the statistics from our agent.
	Sample value - 
		APACHE_STATUS_URL="http://localhost:80/whm-server-status?auto"

3. Save and close the file. Site24x7 Agent willl now monitor your wordpress server.


Wordpress Plugin Attributes:
==========================

Some of the collected attributes are as follows:

		"apache_version" : Version of apache (httpd) running in your server (Sample Value: "Apache/2.2.31 (Unix)"
		"php_version" : Version of the PHP running in your WordPress server (Sample Value: "5.6.16")
		"mysql_version" : Version of mysql server running in your WordPress server (Sample Value: "5.6.29"
		"php_cpu" : The percentage of CPU occupied by PHP processes in the server (Sample Value: "1.2")
		"php_mem" : The percentage of memory occupied by PHP processes in the server (Sample Value: "0.8")
		"apache_status" : Status of apache server in your WordPress server 
		"php_status" : Status of php process in your WordPress server 
		"mysql_status" : Status of MYSQL server in your WordPress server 
		"mysql_mem" : The percentage of memory occupied by the MySQL processes in the server (Sample Value: "0.8")
		"mysql_cpu" : The percentage of CPU occupied by the MySQL processes in the server (Sample Value: "1.2")

Apache server (httpd) attributes :

		"Apache Total Accesses" : The total number of accesses of your apache server
		"Apache Total kBytes" : The total number of bytes count served by your apache server
		"Apache CPULoad" : The current percentage of CPU used by all apache worker threads combined
		"Apache Uptime" : The running time of the server
		"Apache ReqPerSecond" : Average number of requests per second
		"Apache BytesPerSecond" : Average number of bytes served per second
		"Apache BytesPerReq" : Average number of bytes per request
		"Apache BusyWorkers" : The number of workers serving requests
		"Apache IdleWorkers" : The number of idle workers
