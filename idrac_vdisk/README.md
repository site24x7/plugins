# IDRAC Vdisk Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
---

### Plugin Installation  

Supported versions: 1 and 2c

#### Linux

- Create a directory named "idrac_vdisk" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/idrac_vdisk
      
- Download all the files in the "idrac_vdisk" folder and place it under the "idrac_vdisk" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac_vdisk/idrac_vdisk.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac_vdisk/idrac_vdisk.cfg
		wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac_vdisk/SNMPUtil.py

- Execute the following command in your server to install snmpwalk: 

		sudo apt install snmp

- Execute the below command with appropriate arguments to check for the valid json output:

		python idrac_vdisk.py --hostname='hostname' --snmp_version='2c' --snmp_community_str='public'

##### Windows 

- Create a folder named "idrac_vdisk" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\idrac_vdisk
		
- Install the latest version of the Net-SNMP package for windows.
		
- Download the file in the "idrac_vdisk" and place it under the "idrac_vdisk" directory
  
		https://raw.githubusercontent.com/site24x7/plugins/master/idrac_vdisk/idrac_vdisk.py
		https://raw.githubusercontent.com/site24x7/plugins/master/idrac_vdisk/idrac_vdisk.cfg
		https://raw.githubusercontent.com/site24x7/plugins/master/idrac_vdisk/SNMPUtil.py
		
- Execute the below command with appropriate arguments to check for the valid json output:

		python idrac_vdisk.py --hostname='hostname' --snmp_version='2c' --snmp_community_str='public'
---

### Configurations

- Provide your idrac configurations in idrac_vdisk.cfg file.

		[idrac_main]
		hostname = 'hostname'
		snmp_version = '2c' 
		snmp_community_str = 'public'
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.





