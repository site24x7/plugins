
Plugin for Mysql Monitoring
===========

MySQL Plugin is for monitoring the performance metrics of MySQL database. 
  

PreRequisites
======================

Download mysql plugin from https://github.com/site24x7/plugins/blob/master/mysql/mysql.py
Place the plugin folder 'mysql/mysql.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Our plugin uses 'pymysql' module to interact with the MySQL server. Have this installed to use this feature.
Installation of the pymysql module to interact with MySQL


How to install pymysql
======================

Execute the following command in your server to install pymsql:
pip install pymysql

How to install pip
======================

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

Configurations:
==============
In order to change the monitoring configurations, go to plugins directory and edit the required plugin file.

For e.g. mysql => /opt/site24x7agent/monagent/plugins/mysql/mysql.py

```
#Config Section:
MYSQL_HOST = "localhost"
MYSQL_PORT="3306"
MYSQL_USERNAME="root"
MYSQL_PASSWORD=""
```

MySQL Plugin Attributes:
=======================

Some of the collected  mysql attributes are as follows:

* `slow_queries` : No. of slow queries running on the MySQL server

* `max_used_connections` : Total no. of used connections

* `aborted_clients` : Total connections that were aborted

* `aborted_connects` : No. of failed attempts to connect to the MySQL server

* `open_files` : No. of files that are open by the MySQL server

* `threads_running` : No. of threads that are currently running

* `threads_connected` : No. of currently open connections
