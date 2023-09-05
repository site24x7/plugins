# ILO Logical Drive Monitoring
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

- Test SNMP walk for ilologicaldrive:

			snmpwalk -v <version> -c <community-name> <OID>
	Example:

			snmpwalk  -v  2c  -c  public  10.19.1.0  1.3.6.1.4.1.232.6.2.6.1
		
#### Windows

- Follow the steps in [k-base](https://support.site24x7.com/portal/en/kb/articles/ilologicaldrive-monitoring-for-windows) for ilologicaldrive plugins installation

---

### Plugin Installation  

Supported versions: 1 and 2c

- Create a directory named "ilologicaldrive"
- Download all the files in the "ilologicaldrive" folder and place it under the "ilologicaldrive" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/hpilo/ilologicaldrive/ilologicaldrive.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/hpilo/ilologicaldrive/cpqida.mib
		wget https://raw.githubusercontent.com/site24x7/plugins/master/hpilo/ilologicaldrive/SNMPUtil.py
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the ilologicaldrive.py script.
- Add the configurations such as hostname, snmp version, mib file path, etc,. in ilologicaldrive.py.
- Execute the below command with appropriate arguments to check for the valid json output:

		python ilologicaldrive.py 
		
#### Linux

- Move the directory named "ilologicaldrive" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/
		
##### Windows 

- Move the folder named "ilologicaldrive" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.







