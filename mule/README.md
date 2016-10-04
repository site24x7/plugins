# Monitoring Mule Servers

This plugin in shell script executes a Java file to get performance metrics of Mule servers using JMX

### Author: Anita, Zoho Corp
### Language : Java

# Update Lighttpd Server configuration details . Retain the "?auto" suffix.

Uncomment the jmxCredetials and update user and pswd

	jmxCredentials = new HashMap<String, Object>();
	jmxCredentials.put("jmx.remote.credentials", new String[]{"user","pswd"});

# Monitored Attributes
	 memory_usage
	 min_processing_time
	 max_processing_time
	 avg_processing_time
	 processed_events
	 sync_events_received
	 async_events_received
	 execution_errors
	 fatal_errors


### Changes in the plugin will be reflected in Site24x7 only when there is a change in plugin_version.

### HEARTBEAT - false : Site24x7 will alert as down only when plugin status is down
### HEARTBEAT - true  : Site24x7 will alert as down 1. When plugin status is down 2. When there is no data from plugin



Learn more about the plugin installation steps and the various performance metrics that you can monitor here
https://www.site24x7.com/plugins.html