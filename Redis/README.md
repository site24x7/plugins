# Redis Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
---

### Plugin Installation  

- Create a directory named "Redis" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/Redis
      
- Download all the files in the "Redis" folder and place it under the "Redis" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/Redis/Redis.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/Redis/Redis.cfg

- Execute the following command in your server to install redis: 

		pip install redis

- Execute the below command with appropriate arguments to check for the valid json output:

		python Redis.py --host=<REDIS_HOST> --port=<REDIS_PORT> --password=<REDIS_PASSWORD> --dbs=<REDIS_DBS> --queues=<REDIS_QUEUES>


---

### Configurations

- Provide your Redis configurations in Redis.cfg file.

		[redis]
		host = <REDIS_HOST>
		port = <REDIS_PORT>
		password = <REDIS_PASSWORD>
		dbs = <REDIS_DBS>
		queues = <REDIS_QUEUES>
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

