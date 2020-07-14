Plugin for Mysql DB-Size Monitoring
===================================

Plugin is for monitoring the individual size of databases present in MYSQL. 
  
### Language : Python

PreRequisites
=============
    Our Linux server monitoring agent should be installed in the network or on the specific host where the MySQL instance is running.

    Site24x7 MySQL plugin uses "pymysql" module to get the performance metrics of MySQL servers

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
	
Plugin Installation:
===================
Download and install the latest version of the Site24x7 Linux agent in the server where you plan to run the plugin. If it is installed successfully, you will see a Linux server monitor in the Site24x7 Control Panel. This confirms that the agent is able to communicate with our data center.

Create a directory with the name "mysql_db_size", under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/mysql_db_size

Download the file ["mysql_db_size.py" from our GitHub repository](https://raw.githubusercontent.com/site24x7/plugins/master/mysql_db_size/mysql_db_size.py)  and place it under the "mysql_db_size.py" directory

Commands to perform the above step:
	
	cd /opt/site24x7/monagent/plugins/
	mkdir mysql_db_size.py
	cd mysql_db_size.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_db_size.py/mysql_db_size.py
	

Configurations:
==============
In order to change the monitoring configurations, go to plugins directory and edit the required plugin file.

For e.g. mysql => /opt/site24x7agent/monagent/plugins/mysql_db_size.py/mysql_db_size.py

#Config Section:
	MYSQL_HOST = "localhost"
	MYSQL_PORT="3306"
	MYSQL_USERNAME="root"
	MYSQL_PASSWORD=""
	

Metrics Captured:
================= 
	Each of the database size (in MB)