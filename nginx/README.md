# Nginx Plugin
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 




### Plugin Installation  

- Create a directory named "nginx" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/nginx
      
- Download all the files in the "nginx" folder and place it under the "nginx" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.cfg


- Execute the below command with appropriate arguments to check for the valid json output:

 ```
 python3 nginx.py --nginx_status_url=<nginx stats url> --username=<nginx username> --password=<nginx password> 
 ```




---

### Configurations

- Provide your nginx configurations in nginx.cfg file.
```
  [nginx]
  plugin_version=1
  heartbeat=true
  nginx_status_url="http://localhost/nginx_status"
  username=None
  password=None
  timeout=60
  logs_enabled = "true"
  log_type_name = "Nginx Logs"
  log_file_path = "/var/log/nginx/access*"
```	
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


## Supported Metrics

- **Currently active client connections**

    Current active client connections including waiting connections

- **Number of connections where nginx is reading the request header**

    The current number of connections where nginx is reading the request header

- **Number of connections where nginx is writing the response back to the client**

    The current number of connections where nginx is writing the response back to the client

- **Number of idle client connections waiting for a request**

    The current number of idle client connections waiting for a request
- **Count of client requests**

    Client request count in nginx

- **Count of successful client connections**

    Successful client connection in nginx

- **Count of dropped connections**

    Dropped connections count








