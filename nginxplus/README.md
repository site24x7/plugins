# NginxPlus Plugin
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python version 3 or higher.

#### Enabling nginx_status for Metrics Collection 

1. Open terminal and run the following command to open NGINX server configuration file.


		 sudo vi /etc/nginx/nginx.conf

2. Add the following code inside the server block which is present in the "/etc/nginx/nginx.conf" file.
	```
	location /api/ {
	      api write=on;
	}
	```
3. Save and close the /etc/nginx/nginx.conf file.
4. Now reload the nginx to apply the changes :
	```bash
	sudo systemctl reload nginx
	```
5. Test the nginx status URL; it should return a response without error.

	For example:		
	```
	curl http://localhost:80/api/3
	```
	Response of the command should be similar to the below output.
	```
	["nginx","processes","connections","slabs","http","ssl"]
	```
	
	**Note :**
	
	The nginx status URL used was the default one. If you have assigned a domain, please use that in the URL accordingly.
	
## Plugin Installation  

- Once the agent is installed on the server, create a directory named "nginxplus".

		mkdir nginxplus
  		cd nginxplus/
  
- Download all the files in the "nginxplus" folder and place it under the "nginxplus" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginxplus/nginxplus.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginxplus/nginxplus.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the nginxplus.py script.

- Execute the below command with the appropriate arguments to check for valid JSON output.

		python3 nginxplus.py --nginx_status_url "http://localhost:80/api/3" --username "nginxplus username" --password "nginxplus password" 

- After executing the above command and receiving valid JSON, provide the command argument as configurations in the `nginxplus.cfg` file:

		[nginxplus]
		nginx_status_url="http://localhost:80/api/3"
		username="username"
		password="password"
		logs_enabled="False"
		log_type_name =None
		log_file_path=None
	
- Once the configuration is complete, move the "nginxplus" directory to the Site24x7 Linux Agent plugin directory.

		mv nginxplus /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes, and the user can view the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

If you need to run this nginx plugin on a Windows server, please follow the steps provided in the link below.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
