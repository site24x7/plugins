
Plugin for Nagios
==================

A plugin to all your existing Nagios integrations and harness the power of the open source community by our extensive integrations to get the details you want.
  

PreRequisites
=============

Download 'nagios_plugins.json' plugin from https://github.com/site24x7/plugins/nagios/nagios_plugins.json
Place the plugin 'nagios_plugins.json' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Nagios scripts which obey the performance data format as mentioned in 'http://docs.pnp4nagios.org/pnp-0.6/perfdata_format' are only supported.


Configurations:
==============

For e.g.

The file nagios_plugins.json will look like the initial structure below

{
	"nagios": [
	]	
}

Edit the 'nagios_plugins.json' file to include the paths of the nagios script you want the agent to execute.

Sample Configuration:

{
	"nagios": [
		"/usr/local/nagios/libexec/check_ping -H localhost -w 1,1% -c 1,1% -p 5 -t 10 -4",
		"/usr/local/nagios/libexec/check_load -r"
	]
}

'check_load' is a nagios plugin which will be executed by the Site24x7 Linux monitoring agent which will report back to the Site24x7 server.


