# Monitoring Lighttpd Servers

### This plugin in python monitors the performance metrics of Lighttpd servers


It uses the inbuilt Lighttpd monitoring options to get the monitoring data.
Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server

### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu

# Steps to enable monitoring in Lighttpd Server 

1. Open Lighttpd config file.  E.g: /etc/lighttpd/lighttpd.conf
2. Add "mod_status" to server.modules
3. Add status urls if not present  
		status.status-url="/server-status"
4. Restart Lighttpd Server

# Update Lighttpd Server configuration details . Retain the "?auto" suffix.
URL = "http://localhost:80/server-status?auto"
USERNAME = None
PASSWORD = None

# Monitored Attributes
accesses 	 - Total number of requests handled 
traffic 	 - Overall outgoing traffic in KB
uptime 		 - Server uptime in seconds
busy_servers - Total number of active connections
idle_servers - Total number of inactive connections


### Changes in the plugin will be reflected in Site24x7 only when there is a change in plugin_version.

### HEARTBEAT - false : Site24x7 will alert as down only when plugin status is down
### HEARTBEAT - true  : Site24x7 will alert as down 1. When plugin status is down 2. When there is no data from plugin



Learn more about the plugin installation steps and the various performance metrics that you can monitor here
https://www.site24x7.com/plugins.html