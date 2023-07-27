# Nginx Plugin
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

#### Enable nginx_status to get metrics -

1. Open the nginx `server configuration file`.

		 
		 sudo vi /etc/nginx/conf.d/default.conf
		 
2. Add the following code inside the server block which is present in the `server configuration file`.

		location /nginx_status {
		    stub_status;
		    	
		}
3. Save and close the `nginx server configuration` file.
4. Execute the below command to check the validate the syntax of the nginx server configuration file.
   	
    	nginx -t
    	
6. Now reload the nginx to apply the changes :

		sudo systemctl reload nginx

5. Please test the Nginx status URL that returns a response without error.  

	For Example
	```
	curl http://localhost/nginx_status
	```
 	The response of the command should be similar to the below output.
	
	```
	Active connections: 2
	server accepts handled requests
	344014 344014 661581
	Reading: 0 Writing: 1 Waiting: 1
	```
 **Note:**
	The nginx status URL is used as the default one. In case you have assigned a domain please use that in the URL accordingly.

## Plugin Installation  

- Once installed the respective agent in the server, create a directory named "nginx".
      
- Download all the files in the "nginx" folder and place them under the "nginx" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the nginx.py script.

- Execute the below command with appropriate arguments to check for the valid JSON output:

		python3 nginx.py --url=<nginx stats url> --username=<nginx username> --password=<nginx password> --cafile=<cafile>

- Once the above command execution gives the valid JSON, further provide the command argument as configurations in nginx.cfg file.

		[nginx]
		url="http://localhost/nginx_status"
		username=None
		password=None
  		cafile=None
		logs_enabled = "true"
		log_type_name = "Nginx Logs"
		log_file_path = "/var/log/nginx/access*"
	
- Once the configuration is done, move the "nginx" directory under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/

		
The agent will automatically execute the plugin within five minutes and the user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


In case the user needs to run this nginx plugin in a Windows server, please follow the steps below link.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers


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








