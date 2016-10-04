# Monitoring DB2 Servers

### This plugin in python monitors the bufferpool performance metrics of IBM DB2 Servers
It uses the DB2 Queries to get the monitoring data.Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server.

### Author: Shobana, Zoho Corp
### Language : Python
### Tested in Ubuntu

# Update DB2 Server configuration details
DB2_HOST = "localhost"  
DB2_PORT="50000"   
DB2_USERNAME="db2admin"  
DB2_PASSWORD="admin"   
DB2_SAMPLE_DB="SAMPLE"

# Monitored Attributes

# BUFFERPOOL METRICS
	Total logical reads - Total logical reads from bufferpool which is the total of data,index and xda logical reads.
	Total physical reads - Total physical reads from bufferpool which is the total phyiscal reads of data,index and XDA.
	Total hit ratio percent-Buffer pool hit ratio is a measure of how often a page access (a getpage) is satisfied without requiring an I/O operation.
	Data logical reads -  Bufferpool data logical reads
	Data_physical_reads - Bufferpool data physical reads
	Data hit ratio percent - Individual hit ratio for data bufferpool
	Index logical reads - Bufferpool index logical reads
	Index hit ratio percent - Bufferpool index hit ratio
	XDA logical reads - BufferpooLog utilization percent hit ratio percent - Bufferpool XDA hit ratio percent

### LOG UTILIZATION METRICS
	Log utilization percent - The LOG_UTILIZATION administrative view returns information about log utilization for the currently connected database.Percent utilization of total log space. 
	Total log used - Total log space used in KB
	Total log available - Total log space available in KB


### Changes in the plugin will be reflected in Site24x7 only when there is a change in plugin_version.

### HEARTBEAT - false : Site24x7 will alert as down only when plugin status is down
### HEARTBEAT - true : Site24x7 will alert as down 1. When plugin status is down 2. When there is no data from plugin

### Learn more about the plugin installation steps and the various performance metrics that you can monitor in https://www.site24x7.com/plugins.html