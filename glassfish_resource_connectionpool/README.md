# Monitoring Glassfish Servers - Resource Details 

This plugin in python monitors the JVM Threads of Glassfish servers

It uses the inbuilt Glassfish monitoring options to get the monitoring data.
Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server

### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu

# PreRequisites : Install Site24x7 Server Agents
1. Download and Install Site24x7 Server Agent 
2. Download plugin from https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/
3. Place the plugin in the created folder under agent plugins directory (/opt/site24x7/monagent/plugins/)
4. Ensure Glassfish is installed in the server and it should be up and running.
5. The agent will execute the plugin and push the data to the Site24x7 server

# Steps to enable monitoring in Glassfish Server 

1. cd <Glassfish-Installation-dir>/bin/asadmin
2. ./asadmin
3. set server.monitoring-service.module-monitoring-levels.jdbc-connection-pool=LOW

# Update Glassfish Server configuration details
HOST = "localhost"
ADMINPORT = "4848"
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


Learn more about the plugin installation steps and the various performance metrics that you can monitor in https://www.site24x7.com/plugins.html