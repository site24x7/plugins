# Litespeed Monitoring

                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Python version 3 or higher.


## Plugin Installation  

- Create a directory named `litespeed_monitoring`.

	```bash
	mkdir litespeed_monitoring
  	cd litespeed_monitoring/
	```
      
- Download all the files in the "litespeed_monitoring" folder and place it under the "litespeed_monitoring" directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/litespeed_monitoring/litespeed_monitoring.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/litespeed_monitoring/litespeed_monitoring.cfg
	```

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the litespeed_monitoring.py script.

- Execute the below command with appropriate arguments to check for the valid json output:

	```bash
	python3 litespeed_monitoring.py --metric_path "/tmp/lshttpd/" --virtual_host "_AdminVHost"
	```
 
- Provide your litespeed_monitoring configurations in litespeed_monitoring.cfg file.

	```ini
	[ls_monitoring]
	metric_path='/tmp/lshttpd/'
	virtual_host='_AdminVHost'
	logs_enabled='False'
	log_type_name='None'
	log_file_path='None'
	```
 
- Move the directory "litespeed_monitoring" under the Site24x7 Linux Agent plugin directory: 

	```bash
	mv litespeed_monitoring /opt/site24x7/monagent/plugins/
	```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


## Supported Metrics

The following metrics are captured in the litespeed_monitoring Plugin

Name		        	| 	Description
---         			|   	---
**Request Processing**		|	The number of requests being processed
**Request Per Sec**		|	The number of requests per second
**Total Requests**		|	Total number of requests
**Pub Cache Hits Per Sec**	|	Number of public cache hits per sec
**Total Pub Cache Hits**	|	Total number of public cache hits
**Private Cache Hits Per Sec**	|	Total number of private cache hits per sec
**Total Private Cache Hits**	|	Total number of private cache hits
**Static Hits Per Sec**		|	Total number of static hits per sec
**Total Static Hits**		|	Total number of static hits
**Version**			|	Version of the litespeed web server
**Uptime**			|	Uptime of the server
