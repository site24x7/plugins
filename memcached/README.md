
Plugin for MemCache Monitoring
==============================

Memcached is a free and open-source, general purpose distributed memory caching system. Analyze the performance of your Memcached server and take informed troubleshooting descisions by keeping track of critical metrics.

Get to know how to configure the Memcached plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Memcached servers.
  
Learn more https://www.site24x7.com/plugins/memcached-monitoring.html

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Execute the following command in your server to install Redis: 

		pip install python-memcached
---

### Plugin Installation  

- Create a directory named "memcached"

- Download the below files and place it under the "memcached" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/memcached/memcached.py

- Execute the below command with appropriate arguments to check for the valid JSON output:

		python memcached.py
  
  #### Linux

- Place the "memcached" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/memcached

  ##### Windows 

- Move the folder "memcached" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\memcached
