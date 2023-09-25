# ILO CPU Monitoring
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.

#### Linux 

- Execute the following command in your server to install snmpwalk: 

		On Centos/RedHat machines you can install snmpwalk using Yum:
			yum install net–snmp–utils

		On Ubuntu install snmpwalk using apt-get:
			sudo apt–get install snmp
- After installation, export the net-snmp path in the $PATH variable.

  Example:

			export PATH=$PATH:/var/lib/net-snmp/bin

- Test SNMP walk for ilocpu:
  
			snmpwalk  -v  <version>  -c  <community-name>  <ip-address>  <OID>
	Example:

			snmpwalk  -v  2c  -c  public  10.19.1.0  1.3.6.1.4.1.232.6.2.6.1
		
#### Windows

- Install the latest version of the Net-SNMP package. [Follow these steps](https://support.site24x7.com/portal/en/kb/articles/install-net-snmp-package-in-windows-for-plugins) to install and configure it.
- And also add Net-SNMP path to system variables. Then open command prompt or cmd.
- Test SNMP walk for ilobattery:
  
			snmpwalk  -v  <version>  -c  <community-name>  <ip-address>  <OID>
	Example:

			snmpwalk  -v  2c  -c  public  10.19.1.0  1.3.6.1.4.1.232.6.2.6.1 

---

### Plugin Installation  

Supported versions: 1 and 2c

- Create a directory named "ilocpu"
- Download all the files in the "ilocpu" folder and place it under the "ilocpu" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/hpilo/ilocpu/ilocpu.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/hpilo/ilocpu/cpqstdeq.mib
		wget https://raw.githubusercontent.com/site24x7/plugins/master/hpilo/ilocpu/SNMPUtil.py
  
- Add the configurations such as Host(IP Address), snmp version, mib file path, etc,. in ilocpu.py.
- Execute the below command with appropriate arguments to check for the valid json output:

		python ilocpu.py 
		
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the ilocpu.py script.
- Move the directory named "ilocpu" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/
		
##### Windows 

- Follow the [Instructions](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers) to set the python path in environment and system variables.
- Move the folder named "ilocpu" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.







