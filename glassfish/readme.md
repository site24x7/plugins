# Plugin for GlassFish Monitoring


GlassFish is an open source application server project sponsored by Oracle corporation. Configure Site24x7 plugin to monitor the performance of your GlassFish servers.

Get to know how to configure the Oracle GlassFish plugins and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of GlassFish servers.

Learn more: https://www.site24x7.com/plugins/glassfish-plugin-monitoring.html
## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.

### Plugin Installation  

- Create a directory named `glassfish`.

  ```bash
  mkdir glassfish
  cd glassfish/
  ```
      
- Download all the files and place it under the `glassfish` directory.

  ```bash
  wget https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/glassfish.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/glassfish.cfg
  ```

 
- Execute the below command with appropriate arguments to check for the valid json output:
  ```bash
  python3 glassfish.py --host "hostname" --port "port no" --username "username" --password "password" --ssl "false"  --insecure "false"
  ```


#### Configurations

- Provide your IBM MQ configurations in glassfish.cfg file.
	```ini
  [localhost]
  host="localhost"
  port="4848"
  ssl="false"  
  insecure="false"
  username="None"
  password="None"
	```
 - Where,
   - host: The IP address or domain name of the server you're trying to connect to.
   - port: Admin port of the glassfish server.
   - ssl: Connect with https if "true" and http if "false".
   - insecure: If this parameter is set to "true", it allows you to connect even if the certificate is invalid. This should only be used in testing environments.
   - username and password: These credentials are required if any form of authentication is set up for the server.

#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the glassfish.py script.

- Move the folder `glassfish` into the Site24x7 Linux Agent plugin directory: 

		mv glassfish /opt/site24x7/monagent/plugins/
  
#### Windows
		
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Move the folder `glassfish` under Site24x7 Windows Agent plugin folder: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
	
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---	

## Supported Metrics

Name		            	| Description
---         		   	  |   ---

