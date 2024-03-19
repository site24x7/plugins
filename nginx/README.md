# Nginx Plugin
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python version 3 or higher.

#### Enable nginx_status to get metrics -

1. Open terminal and run the following command to open NGINX server configuration file.

		 sudo vi /etc/nginx/nginx.conf

2. Add the following code inside the server block which is present in the "/etc/nginx/nginx.conf" file.
	```
	location /nginx_status {
	    stub_status;
    	
	}
	```
3. Save and close the /etc/nginx/nginx.conf file.
4. Now reload the nginx to apply the changes :
	```bash
	sudo systemctl reload nginx
	```

5. Test the nginx status URL; it should return a response without error.

	For Example
	```
	curl http://localhost/nginx_status
	```
 	Response of the command should be similar to the below output.
	
	```
	Active connections: 2
	server accepts handled requests
	344014 344014 661581
	Reading: 0 Writing: 1 Waiting: 1
	```
 **Note :**
	The nginx status URL used was the default one. If you have assigned a domain, please use that in the URL accordingly.

## Plugin Installation  

- Once the agent is installed on the server, create a directory named "nginx".

		mkdir nginx
  		cd nginx/
      
- Download all the files in the "nginx" folder and place it under the "nginx" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.py && sed -i "1s|^.*|#! $(which python3)|" nginx.py
  		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.cfg



- Execute the below command with the appropriate arguments to check for valid JSON output.

		python3 nginx.py --nginx_status_url "http://localhost/nginx_status" --username "nginx username" --password "nginx password"

- After executing the above command and receiving valid JSON, provide the command argument as configurations in the `nginx.cfg` file.

		[nginx]
		plugin_version=1
		heartbeat=true
		nginx_status_url="http://localhost/nginx_status"
		username="None"
		password="None"
		timeout=60
		logs_enabled = "true"
		log_type_name = "Nginx Logs"
		log_file_path = "/var/log/nginx/access*"
	
- Once the configuration done, move the "nginx" directory under the Site24x7 Linux Agent plugin directory: 

		mv nginx /opt/site24x7/monagent/plugins/

		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


If you need to run this nginx plugin on a Windows server, please follow the steps provided in the link below.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers


## Supported Metrics

Name		            	| Description
---         		   	|   ---
Currently active client connections	|	Current active client connections including waiting connections.
Number of connections where nginx is reading the request header	|	The current number of connections where nginx is reading the request header.
Number of connections where nginx is writing the response back to the client	|	The current number of connections where nginx is writing the response back to the client.
Number of idle client connections waiting for a request	|	The current number of idle client connections waiting for a request.
Count of client requests	|	Client request count in nginx.
Count of successful client connections	|	Successful client connection in nginx.
Count of dropped connections	|	Dropped connections count.






