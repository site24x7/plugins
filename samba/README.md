
Plugin for Samba Monitoring
==============================

Samba Plugin is for monitoring the performance metrics of Samba server. 
  

PreRequisites
=============

Download samba plugin from https://github.com/site24x7/plugins/blob/master/samba/samba.py
Place the plugin folder 'samba/samba.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configurations:
==============
In order to change the monitoring configurations, go to plugins directory and edit the required plugin file.

For e.g. samba => /opt/site24x7agent/monagent/plugins/samba/samba.py


Samba Plugin Attributes:
=======================

The collected Samba attributes are as follows:

"samba_version" : Current Samba server installation version number. 

"folders_accessed" : Number of unique folder shares being accessed by users.

"users" : Total number of users that have open connection to Samba server.
