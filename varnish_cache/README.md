Plugin for Varnish Cache Monitoring
=============================

Varnish Cache is a web application accelarator which is installed in front of an HTTP server to cache the contents. Analyze and optimize your Varnish Cache servers by configuring our plugin. Proactively monitor the availability and performance of caches and work objects created.

Get to know how to configure the Varnish Cache plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Varnish Cache ecosystems.

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.
- Ensure the Python module "psycopg2" is installed to fetch the stats from the Varnish Cache server.
 

Learn more https://www.site24x7.com/plugins/varnish-cache-monitoring.html

### Plugin Installation  

- Create a directory named "varnish_cache"

- Download the below files and place it under the "varnish_cache" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/varnish_cache/varnish_cache.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the varnish_cache.py script.

- Edit the varnish_cache.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python varnish_cache.py
  #### Linux

- Place the "varnish_cache" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/varnish_cache

  #### Windows 

- Move the folder "varnish_cache" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\varnish_cache
