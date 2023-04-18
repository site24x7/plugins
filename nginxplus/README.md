# NginxPlus Plugin
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

#### Enable nginx_status to get metrics -

1. Open terminal and run the following command to open NGINX server configuration file.
		 ``` 
		 $sudo vi /etc/nginx/nginx.conf
		 ```
2. Add the following code inside the server block which is present in the "/etc/nginx/nginx.conf" file.
```
location /api/ {
      api write=on;
}
```
3. Save and close the /etc/nginx/nginx.conf file.
4. Now restart the nginx to apply the changes :
```bash
sudo systemctl reload nginx
```


## Plugin Installation  

- Once installed the respective agent in the server, create a directory named "nginxplus".
      
- Download all the files in the "nginxplus" folder and place it under the "nginxplus" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginxplus/nginxplus.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/nginxplus/nginxplus.cfg

- Execute the below command with appropriate arguments to check for the valid json output:

 ```bash
 python3 nginxplus.py --nginx_status_url="http://localhost:80/api/3" --username=<nginxplus username> --password=<nginxplus password> 
 ```

- Once the above command execution given the valid json, further provide the command argument as configurations in nginxplus.cfg file.
```
[nginxplus]
nginx_status_url="http://localhost:80/api/3"
username=<username>
password=<password>
logs_enabled="False"
log_type_name =None
log_file_path=None

```	
- Once the configuration done, move the "nginx" directory under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/nginxplus 

		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

In case if user needs to run this nginx plugin in windows server, please follow the steps in below link.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers










