
Plugin for Redis Monitoring
===========================

Redis Plugin is for monitoring the performance metrics of Redis database. 
  

PreRequisites
=============

Download redis plugin from https://github.com/site24x7/plugins/blob/master/redis/Redis.py
Place the plugin folder 'redis/redis.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Our plugin uses 'redis' module to interact with the Redis server. Have this installed to use this feature.
Installation of the redis module is as follows


How to install redis
===================

Execute the following command in your server to install redis:
pip install redis

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

For e.g. redis => /opt/site24x7agent/monagent/plugins/redis/Redis.py

#Config Section:
==================

REDIS_HOST = "localhost"

REDIS_PORT = "6379"

REDIS_PASSWORD = ""

REDIS_DBS = "0"

REDIS_QUEUES = ""

Redis Plugin Attributes:
=======================

Some of the collected redis attributes are as follows:

"used_memory" : Total no. of bytes allocated by Redis

"used_memory_peak" : Peak memory consumed by Redis

"used_cpu_sys" : System CPU consumed by Redis

"used_cpu_user" : User CPU consumed by Redis

"keyspace_hits" : No. of successful lookup of keys in the main dictionary

"keyspace_misses" : No. of failed lookup of keys in the main dictionary

"total_connections_received" : Total no. of connections accepted by the server

"rejected_connections" : Total no. of connections rejected by max clients limit
