# Plugin for Monitoring VPN Host and INTRANET URL



## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin installation
---
#### Linux 

- Create a directory "vpn_check" 

- Download the files "vpn_check.py" , "isp.sh" and place it under the "vpn_check" directory
  
	wget https://raw.githubusercontent.com/site24x7/plugins/master/vpn_check/vpn_check.py

	wget https://raw.githubusercontent.com/site24x7/plugins/master/vpn_check/isp.sh

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the vpn_check.py script.


- Place the "vpn_check" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/vpn_check
#### Windows

- Create a directory "vpn_check" under Site24x7 Windows Agent plugin directory.

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\vpn_check

- Download the  "vpn_check.py" file and place it under the "vpn_check" directory
	
### Plugin configurations
---

- Configure the VPN host and port to be monitored in the file vpn_check.py

- Configure the url to be monitored in the field 'URL_BEHIND_VPN' in the file vpn_check.py


The agent will automatically execute the plugin within five minutes and the user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Captured
---

- VPN status
- URL status
- Response Time of the URL
- ISP Vendor
