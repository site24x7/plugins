
Plugin for MemCache Monitoring
==============================

MemCache Plugin is for monitoring the performance metrics of MemCached server. 
  

PreRequisites
=============

Download memcache plugin from https://github.com/site24x7/plugins/blob/master/memcached/memcached.py
Place the plugin folder 'memcached/memcached.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)
Our plugin uses 'memcache' module to interact with the Memcached server. Have this installed to use this feature.
Installation of the memcache module is as follows


How to install memcache
=======================

Execute the following command in your server to install memcache:
Download the python-memcache(python-memcached-1.57.tar.gz) from its source https://pypi.python.org/pypi/python-memcached.
Build the same by executing the following commands:

python setup.py build
python setup.py install

Try importing memcache module in your python interperter should not throw any error on successful installation.


Configurations:
==============
In order to change the monitoring configurations, go to plugins directory and edit the required plugin file.

For e.g. memcache => /opt/site24x7agent/monagent/plugins/memcached/memcached.py

#Config Section:
MEMCACHE_HOST='127.0.0.1'

MEMCACHE_PORT=11211

Memcache Plugin Attributes:
=======================

Some of the collected memcache attributes are as follows:

"bytes" : Current number of bytes used by this server to store items.

"curr_connections" : Current number of open connections.

"total_connections" : Total number of connections opened since the server started running.

"bytes_read" : Total number of bytes read by this server from network

"bytes_written" : Total number of bytes sent by this server to network

"limit_maxbytes" : Number of bytes this server is permitted to use for storage.

"threads" : Number of worker threads requested.

"evictions" : Number of valid items removed from cache to free memory for new items. 