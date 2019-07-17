
Plugin for Mysql Replication Monitoring
=================================

MySQL Replication Plugin is for monitoring the replication metrics of MySQL in a database. 
  
### Language : Python
### Tested in Ubuntu

PreRequisites
=============
	Site24x7 MySQL plugin uses "pymysql" module to get the performance metrics of MySQL servers

Download mysql plugin from https://raw.githubusercontent.com/site24x7/plugins/master/mysql-replication/mysql-replication.py

Place the plugin folder 'mysql-replication/mysql-replication.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Our plugin uses 'pymysql' module to interact with the MySQL server. Have this installed to use this feature.

How to install pymysql
======================

Execute the following command in your server to install pymsql:
	pip install pymysql

To install python to a specific python : 
	python3 -m pip install pymysql	

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
	
Mysql replication plugin installation:
=======================================

Create a directory with the name "mysql-replication", under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/mysql-replication

Download the file ["mysql-replication.py" from our GitHub repository](https://raw.githubusercontent.com/site24x7/plugins/master/mysql-replication/mysql-replication.py)  and place it under the "mysql-replication.py" directory

Commands to perform the above step:
	
	cd /opt/site24x7/monagent/plugins/
	mkdir mysql-replication.py
	cd mysql-replication.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql-replication.py/mysql-replication.py
	

Configurations:
==============
In order to change the monitoring configurations, go to plugins directory and edit the required plugin file.

For e.g. mysql => /opt/site24x7agent/monagent/plugins/mysql-replication.py/mysql-replication.py

#Config Section:
	MYSQL_HOST = "localhost"
	MYSQL_PORT="3306"
	MYSQL_USERNAME="root"
	MYSQL_PASSWORD=""
	

MySQL Replication Plugin Attributes:
==================================== 
	Seconds_Behind_Master
	Slave_IO_State
	Last_Errno
	Last_IO_Errno
	Last_SQL_Errno
	Relay_Log_Space
	Skip_Counter
	Slave_IO_Running
	Slave_SQL_Running
	Slave_heartbeat_period
	Slave_open_temp_tables
	Slave_received_heartbeats
	Slave_retried_transactions
	Slave_running
	
