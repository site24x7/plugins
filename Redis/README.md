# Redis Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Execute the following command in your server to install Redis: 

		pip install redis
---

### Plugin Installation  

- Download all the files in the "Redis" folder and place it under the "Redis" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/redis/Redis.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/redis/Redis.cfg

- Execute the below command with appropriate arguments to check for the valid JSON output:

		python Redis.py --host=<REDIS_HOST> --port=<REDIS_PORT> --password=<REDIS_PASSWORD> --dbs=<REDIS_DBS> 
		
- Provide your Redis configurations in Redis.cfg file.

		[redis]
		host = <REDIS_HOST>
		port = <REDIS_PORT>
		password = <REDIS_PASSWORD>
		dbs = <REDIS_DBS>

- Move the "Redis" directory to the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


