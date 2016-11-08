
Plugin for Mysql Table Monitoring
=================================

MySQL table status Plugin is for monitoring the metrics of MySQL tables in a database. 
  

### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu

PreRequisites
=============
	Site24x7 MySQL plugin uses "pymysql" module to get the performance metrics of MySQL servers

Download mysql plugin from https://github.com/site24x7/plugins/blob/master/mysql_table_status/mysql_table_status.py
Place the plugin folder 'mysql/mysql.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Our plugin uses 'pymysql' module to interact with the MySQL server. Have this installed to use this feature.

How to install pymysql
======================

Execute the following command in your server to install pymsql:
	pip install pymysql


How to install pip
===================

For CentOS, Fedora, RHEL:
	yum install python-devel
	yum install python-pip (or)
	easy_install pip	

For Debian, Ubuntu :
	apt-get update
	apt-get -y install python-pip (or)
	easy_install pip

Note:
	pip is a package management system that is used to install and manage software packages written in Python.
	
MySQL Table status plugin installation:
=======================================

Create a directory with the name "mysql\_table\_status", under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/mysql\_table\_status

Download the file ["mysql_table_status.py" from our GitHub repository](https://github.com/site24x7/plugins/tree/master/mysql_table_status "")  and place it under the "mysql\_table\_status" directory

Commands to perform the above step:
	
	cd /opt/site24x7/monagent/plugins/
	mkdir mysql_table_status
	cd mysql_table_status
	wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_table_status/mysql_table_status.py
	

Configurations:
==============
In order to change the monitoring configurations, go to plugins directory and edit the required plugin file.

For e.g. mysql => /opt/site24x7agent/monagent/plugins/mysql_table_status/mysql_table_status.py

#Config Section:
	MYSQL_HOST = "localhost"
	MYSQL_PORT="3306"
	MYSQL_USERNAME="root"
	MYSQL_PASSWORD=""
	DATABASE = "<database over which the table stats has to be retrived>"
	TABLE = "<Table name for which the metrics has to retrived>"

MySQL Table stats Plugin Attributes:
====================================

	 {
    "data_length": 16384,
    "heartbeat_required": "true",
    "index_length": 16384,
    "max_data_length": 0,
    "plugin_version": "1",
    "row_length": 3276,
    "rows_count": 5,
    "units": {
        "data_length": "bytes",
        "index_length": "bytes",
        "max_data_length": "bytes",
        "row_count": "units",
        "row_lenth": "bytes"
    },
    "version": "5.6.33-0ubuntu0.14.04.1-log"
	}

Monitoring additional metrics:
==============================
To monitor additional metrics, edit the "mysql_table_status.py" file and add the new metrics that need monitoring
 
Increment the plugin version value in the file "mysql_table_status.py" to view the newly added metrics ( For e.g. Change the default plugin version from PLUGIN_VERSION = "1" to "PLUGIN_VERSION = "2") 
