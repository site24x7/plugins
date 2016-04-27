
Plugin for MongoDB Monitoring
=============================

MongoDB Plugin is for monitoring the performance metrics of MongoDB database. 
  

PreRequisites
=============

Download mongodb plugin from https://github.com/site24x7/plugins/blob/master/mongod/mongod.py
Place the plugin folder 'mongod/mongod.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Our plugin uses 'pymongo' module to interact with the MongoDB server. Have this installed to use this feature.
Installation of the pymongo module is as follows


How to install pymongo
===================

Execute the following command in your server to install pymongo:
pip install pymongo

How to install pip
==================

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

For e.g. mongodb => /opt/site24x7agent/monagent/plugins/mongod/mongod.py

#Config Section:
MONGODB_HOST='127.0.0.1'

MONGODB_PORT=27017

MONGODB_DBSTATS="yes"

MONGODB_REPLSET="no"

MongoDB Plugin Attributes:
=======================

Some of the collected mongodb attributes are as follows:

"connections_available" : Total number of connections available

"connections_current" : Total number of current connections

"cursors_total_open" : Total number of open cursors

"heap_usage" : Total heap usage
