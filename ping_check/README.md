# Plugin for Monitoring Host Ping

### Plugin installation
---
##### Linux 

- Create a directory "ping_check".

- Download the files "ping_check.py" and place it under the "ping_check" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/ping_check/ping_check.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/ping_check/ping_check.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the ping_check.py script.
		
- Configure the Host to be monitored in the file ping_check.cfg

		[host_1]
		host="8.8.8.8"

- Configure INTERFACE_IP if the ping has to be happen via a specific source else leave it to None.

- Execute the below command to check for valid json output

		python ping_check.py --host="host"
		
##### Linux 

- Move the directory "ping_check" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/

##### Windows

- Move the directory "ping_check" under Site24x7 Windows Agent plugin directory - C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Captured
---

- Ping status
- Packet Loss
