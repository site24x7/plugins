# Monitoring Glassfish Servers - JVM Memory Details

### This plugin in python monitors the JVM Memory Metrics of Glassfish servers

It uses the inbuilt Glassfish monitoring options to get the monitoring data.

### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu


# PreRequisites : Install Site24x7 Server Agents
1. Download and Install Site24x7 Server Agent 
2. Download plugin from github
3. Create a folder glassfish_jvm_memory and place the plugin in the created folder under agent plugins directory (/opt/site24x7/monagent/plugins/)
4. The agent will execute the plugin and push the data to the Site24x7 server

# Steps to enable monitoring in Glassfish Server 

1. cd <Glassfish-Installation-dir>/bin/asadmin
2. ./asadmin
3. set server.monitoring-service.module-monitoring-levels.jvm=LOW

# Update Glassfish Server configuration details
HOST = "localhost"
ADMINPORT = "4848"
USERNAME = None
PASSWORD = None

# Monitored Attributes

### MEMORY

usednonheapsize 				- Amount of used non-heap memory in bytes
maxheapsize 					- Maximum amount of heap memory in bytes that can be used for memory management
initheapsize 					- Amount of heap memory in bytes that the JVM initially requests from OS for memory management
initnonheapsize 				- Amount of non-heap memory in bytes that the JVM initially requests from OS for memory management
usedheapsize 					- Amount of used heap memory in bytes
committednonheapsize 			- Amount of non-heap memory in bytes that is committed for the JVM to use
objectpendingfinalizationcount 	- Approximate number of objects for which finalization is pending
maxnonheapsize 					- Maximum amount of non-heap memory in bytes that can be used for memory management
committedheapsize 				- Amount of heap memory in bytes that is committed for the JVM to use     


### Changes in the plugin will be reflected in Site24x7 only when there is a change in plugin_version.

### HEARTBEAT - false : Site24x7 will alert as down only when plugin status is down
### HEARTBEAT - true  : Site24x7 will alert as down 1. When plugin status is down 2. When there is no data from plugin


Learn more about the plugin installation steps and the various performance metrics that you can monitor in https://www.site24x7.com/plugins.html