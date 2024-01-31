
Plugin for Haproxy Monitoring
=============================

HAProxy is free, open source software that provides a high availability load balancer and proxy server for TCP and HTTP-based applications that spreads requests across multiple servers. Monitor the performance metrics of your Haproxy setup using this plugin. 
  
Get to know how to configure the HAProxy plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of HAProxy servers.

Learn more https://www.site24x7.com/plugins/haproxy-monitoring.html

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.

---

### Plugin Installation  

- Create a directory named "haproxy"

- Download the below files and place it under the "haproxy" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/haproxy/haproxy.py
  		wget https://raw.githubusercontent.com/site24x7/plugins/master/haproxy/haproxy.cfg

  #### Note:
  	- The cfg file given here is different from the /etc/haproxy/haproxy.cfg. This file is for plugin configuration and used only by site24x7 agent.

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the haproxy.py script.
  
- Execute the below command with appropriate arguments to check for the valid JSON output:
  
	```
	python haproxy.py --username "username" --password "password" --url "http://localhost:80/stats;csv"
	```

- Example configuration for haproxy.cfg. The password given here will be encrypted.
	```
	[haproxy]
	username="username"
	password="password"
	url="http://localhost:80/stats;csv"
	logs_enabled="True"
	log_type_name="haproxy"
	log_file_path="/var/log/haproxy.log"
	```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
