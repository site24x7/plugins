# Nginx Plugin

## Nginx plugin installer

### On Windows Servers
Open a PowerShell terminal as Administrator and execute the commands below to set up your directory layout, download the script files, and configure prerequisites.
```powershell
New-Item -ItemType Directory -Force -Path "C:\nginx-1.30.4\plugins\nginx"
cd "C:\nginx-1.30.4\plugins\nginx"
```

### On Linux Servers
Execute the command below in the terminal to run an installer that checks the prerequisites and installs the plugin.
```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/nginx/installer/Site24x7NginxPluginInstaller.sh && sudo bash Site24x7NginxPluginInstaller.sh
```
	       
## Prerequisites

- Download and install the latest version of the [Site24x7 Windows Agent](https://site24x7.com) or [Site24x7 Linux Agent](https://site24x7.com) on the server where you plan to run the plugin.
- Python version 3 or higher.

#### Enable nginx_status and Advanced Logging to get metrics -

1. Open your terminal and run your text editor to modify the NGINX configuration file.

    **Windows:**
 	```powershell
	notepad C:\nginx-1.30.4\conf\nginx.conf
	```
    **Linux:**
 	```bash
	sudo vi /etc/nginx/nginx.conf
	```
  
2. Define the custom tracking tokens in the text layout format and ensure `stub_status` is active with an `allow all` rule inside the HTTPS server block.

 	```nginxconf
	log_format advanced_text '\(remote_addr -\)remote_user [\(time_local] "\)request" '
	                         '\(status\)body_bytes_sent "\(http_referer" "\)http_user_agent" '
	                         'rt=\$request_time urt=\(upstream_response_time cs=\)upstream_cache_status';

	access_log  logs/access.log  advanced_text;

	location /nginx_status {
	    stub_status;
	    allow all;
	}
	```
  
3. Save and close the /etc/nginx/nginx.conf file.
4. Now reload NGINX to apply your tracking changes:

    **Windows:**
 	```powershell
	cd C:\nginx-1.30.4
	.\nginx.exe -s reload
	```
    **Linux:**
 	```bash
	sudo systemctl reload nginx
	```

5. Test the secure nginx status URL; it should return a raw response without error.

	For Example
	```bash
	curl https://localhost/nginx_status -Insecure
	```
 	Response of the command should be similar to the below output.
	
	```
	Active connections: 2
	server accepts handled requests
	344014 344014 661581
	Reading: 0 Writing: 1 Waiting: 1
	```
 **Note :**
	The nginx status URL uses HTTPS and ignores self-signed certificate constraints. If you have assigned a domain, please update the URL parameters accordingly.

## Plugin Installation  

- Once the agent is installed on the server, create a directory named `nginx`.

    **Windows:**
  	```powershell
	mkdir nginx
  	cd nginx/
 	```
    **Linux:**
  	```bash
	mkdir nginx
  	cd nginx/
 	```
   
- Place your updated monitoring script files (`nginx_monitoring.py` and `nginx.cfg`) inside this `nginx` directory. On Linux servers, execute the following command to configure the Python path:
 	```bash
	sed -i "1s|^.*|#! \$(which python3)|" nginx_monitoring.py
	```

- Execute the below command with the appropriate arguments to verify a clean metric JSON output string.

 	```bash
	python3 nginx.py --nginx_status_url "http://localhost/nginx_status" --username "nginx username" --password "nginx password"
 	```

- After executing the above command and receiving valid JSON, provide the configuration arguments inside the `nginx.cfg` file.

 	```ini
	[nginx]
	plugin_version=1
	heartbeat=true
	nginx_status_url="https://localhost/nginx_status"
	username="None"
	password="None"
	timeout=60
	logs_enabled = "false"
	log_type_name = "Nginx Logs"
	log_file_path = "C:\nginx-1.30.4\logs\access.log" # Use /var/log/nginx/access.log for Linux
	```

- Once the configuration is done, move the `nginx` directory under the Site24x7 Agent plugin directory: 

    **Windows:**
	```powershell
	mv nginx "C:\Program Files\Site24x7\WinAgent\plugins\"
	```
    **Linux:**
	```bash
	sudo mv nginx /opt/site24x7/monagent/plugins/
	```

		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


If you need to run this nginx plugin on a Linux server, please follow the steps provided in the link below.
https://site24x7.com


## Supported Metrics

### Core Connection Metrics

Name		            							| Description
---         		   							|   ---
Currently active client connections						|	Current active client connections including waiting connections.
Number of connections where nginx is reading the request header			|	The current number of connections where nginx is reading the request header.
Number of connections where nginx is writing the response back to the client	|	The current number of connections where nginx is writing the response back to the client.
Number of idle client connections waiting for a request				|	The current number of idle client connections waiting for a request.
Count of client requests							|	Client request count in nginx.
Count of successful client connections						|	Successful client connection in nginx.
Count of dropped connections							|	Dropped connections count.

### Advanced Metrics (Log-Parsed)

Name		            							| Description
---         		   							|   ---
HTTP Status 2xx Count                             |   Total count of successful status 200-299 responses processed.
HTTP Status 3xx Count                             |   Total count of redirect status 300-399 responses processed.
HTTP Status 4xx Count                             |   Total count of client error status 400-499 responses processed.
HTTP Status 5xx Count                             |   Total count of server error status 500-599 responses processed.
Traffic Throughput Bytes                          |   Total volume of data bandwidth sent back to clients in bytes.
Cache Hit Count                                   |   Total number of requests served directly from local disk cache.
Cache Miss Count                                  |   Total number of requests that missed cache and hit backend.
Cache Bypass Count                                |   Total number of requests explicitly configured to bypass cache.
Cache Expired Count                               |   Total number of requests where cached content was expired.
Avg Request Time ms                               |   Average end-to-end client request round-trip time in milliseconds.
Avg Upstream Response Time ms                     |   Average response execution latency of backend applications in milliseconds.