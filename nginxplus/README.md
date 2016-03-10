
Plugin for Nginx Monitoring
===========================

NginxPlus Plugin is for monitoring the performance metrics of NginxPlus Server.
  

PreRequisites
=============

Ensure that the NGINX server is installed and is up and running
Make sure the status URL is configured in your NGINX server
Download NGINX plugin from https://github.com/site24x7/plugins/blob/master/nginxplus/nginxplus.py
Place it in the plugin folder 'nginxplus/nginxplus.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configurations:
==============
In order to change the monitoring configurations, go to plugins directory and edit the required plugin file.

For e.g. nginxplus => /opt/site24x7agent/monagent/plugins/nginxplus/nginxplus.py

#Config Section:
NGINX_STATUS_URL = "http://localhost/status"


NginxPlus Plugin Attributes:
=======================

Some of the collected nginx server attributes are as follows:

"connections_accepted" : Total number of connections available

"connections_active" : Total number of current connections

"connections_dropped" : Total number of open cursors

"connections_idle" : Total heap usage 

"handshakes" : Total number of handshakes

"handshakes_failed" : Total number of handshakes failed

"requests_total" : Total number of requests to the NGINX server

"requests_current" : Total number of current requests

"zone_backend-servers_responses_1xx" : Number of responses with status code 1xx

"zone_backend-servers_responses_2xx" : Number of responses with status code 2xx

"zone_backend-servers_responses_3xx" : Number of responses with status code 3xx

"zone_backend-servers_responses_4xx" : Number of responses with status code 4xx

"zone_backend-servers_responses_5xx" : Number of responses with status code 5xx
