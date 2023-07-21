# IDRAC Battery Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

#### Linux 

- Execute the following command in your server to install snmpwalk: 

		On Centos/RedHat machines you can install snmpwalk using Yum:
  			yum install net–snmp–utils

  		On Ubuntu install snmpwalk using apt-get:
  			sudo apt–get install snmp
  
- After installation, export the net-snmp path in the $PATH variable.

    		Example:
  			export PATH=$PATH:/var/lib/net-snmp/bin

- Test SNMP walk for iDrac:
  
  		command:
  			snmpwalk -v <version> -c <community-name> <OID>
        	Example:
  			snmpwalk -v 2c -c public 10.19.1.0 1.3.6.1.4.1.674.10892.5.4.600.50.1.5
		
#### Windows

- Follow the steps in [k-base](https://support.site24x7.com/portal/en/kb/articles/idrac-monitoring-for-windows) for iDrac plugins installation

---

### Plugin Installation  

Supported versions: 1 and 2c

- Create a directory named "idrac_battery"
      
- Download all the files in the "idrac_battery" folder and place it under the "idrac_battery" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac_battery/idrac_battery.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac_battery/idrac_battery.cfg
		wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac_battery/SNMPUtil.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the idrac_battery.py script.
  
- Execute the below command with appropriate arguments to check for the valid json output:

		python idrac_battery.py --hostname='hostname' --snmp_version='2c' --snmp_community_str='public'

- Provide your idrac configurations in idrac_battery.cfg file.

		[idrac_main]
		hostname = 'hostname'
		snmp_version = '2c' 
		snmp_community_str = 'public'
		
#### Linux

- Move the directory named "idrac_battery" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/
		
##### Windows 

- Move the folder named "idrac_battery" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.





