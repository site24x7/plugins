# Monitoring iDRAC Servers

This plugin in python monitors the hardwares of iDRAC servers

### It uses snmpwalk command to get the hadrware data from the iDRAC Servers
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server

### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu
### Tested for snmp version 2c

# PreRequisites : Install Site24x7 Server Agents
1. Download and Install Site24x7 Server Agent 
2. Download plugin from https://raw.githubusercontent.com/site24x7/plugins/master/iDRAC_Powersource/iDRAC_Powersource.py
3. Place the plugin in the created folder under agent plugins directory (/opt/site24x7/monagent/plugins/iDRAC_Powersource)
4. Plugin name and folder name must be same
5. The agent will execute the plugin and push the data to the Site24x7 server

# Prerequisites : Python Packages
Install netsnmp python package

# Update iDRAC Server configuration details

HOST = 'localhost'
VERSION = '2c' # supports snmp version 2c 
COMMUNITY = 'public'
MIB = 'MIB LOCATION' #Absolute path of the MIB Location

# Monitored Attributes

### Powersource
status, owatt(Watts), iwatt(Watts), ovolt(Volts), ivolt(Volts), current(Ampere)


### Changes in the plugin will be reflected in Site24x7 only when there is a change in plugin_version.

### HEARTBEAT - false : Site24x7 will alert as down only when plugin status is down
### HEARTBEAT - true  : Site24x7 will alert as down 1. When plugin status is down 2. When there is no data from plugin

Learn more about the plugin installation steps and the various performance metrics that you can monitor here
https://www.site24x7.com/plugins.html
