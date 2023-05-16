# IDRAC PDiskMonitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

#### LInux 

- Execute the following command in your server to install snmpwalk: 

		sudo apt install snmp
		
#### Windows

- Install the latest version of the Net-SNMP package for windows.

---

### Plugin Installation  

Supported versions: 1 and 2c

- Create a directory named "idrac_pdisk"
      
- Download all the files in the "idrac_pdisk" folder and place it under the "idrac_pdisk" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac_pdisk/idrac_pdisk.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac_pdisk/idrac_pdisk.cfg
		wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac_pdisk/SNMPUtil.py

- Execute the below command with appropriate arguments to check for the valid json output:

		python idrac_pdisk.py --hostname='hostname' --snmp_version='2c' --snmp_community_str='public'

- Provide your idrac configurations in idrac_pdisk.cfg file.

		[idrac_main]
		hostname = 'hostname'
		snmp_version = '2c' 
		snmp_community_str = 'public'
		
#### Linux

- Move the directory named "idrac_pdisk" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/
		
##### Windows 

- Move the folder named "idrac_pdisk" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.





