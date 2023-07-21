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

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Create a directory with the name "mysql_db_size".

- Download the file "mysql_db_size.py" and place it under the "mysql_custom_query" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_db_size/mysql_db_size.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mysql_db_size.py script.
		
- Update the below configurations in mysql_db_size.py file in #Config Section:

		MYSQL_HOST = "localhost"
		MYSQL_PORT="3306"
		MYSQL_USERNAME="root"
		MYSQL_PASSWORD=""
		
- Execute the below command to check for valid json output.

		python mysql_db_size.py
		
#### Linux 

- Move the directory "mysql_db_size" under Site24x7 Linux Agent plugin directory :

		Linux             ->   /opt/site24x7/monagent/plugins/
		
#### Windows

- Move the directory "mysql_db_size" under Site24x7 Windows Agent plugin directory :

		Windows             ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
	

Metrics Captured:
================= 
	Each of the database size (in MB)
