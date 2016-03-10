
Plugin for Zookeeper Monitoring
===========================

Zookeeper Plugin is for monitoring the performance metrics of Zookeeper.
  

PreRequisites
=============

Ensure that the Zookeeper service is installated and up and running
Download Zookeeper from https://github.com/site24x7/plugins/blob/master/zookeeper/zookeeper.py 
Place it in the plugin folder 'zookeeper/zookeeper.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)


Configurations:
==============
In order to change the monitoring configurations, go to plugins directory and edit the required plugin file.

For e.g. zookeeper => /opt/site24x7agent/monagent/plugins/zookeeper/zookeeper.py

#Config Section:
ZOOKEEPER_HOST='127.0.0.1'

ZOOKEEPER_PORT=2181


Zookeeper Plugin Attributes:
=======================

Some of the collected zookeper server attributes are as follows:

"imok" : Denotes zookeeper status .

"zk_outstanding_requests" : Total number of outstanding requests.

"latency avg" : Average latency

"connections" : Total number of connections. 

"maxclientcnxns" : Total number of maximum client connections

"maxsessiontimeout" : Maximum session time out value

"minsessiontimeout" : Minimum session time out value

"zk_packets_sent" : Total number of packets sent

"zk_packets_received" : Total number of packets received.
