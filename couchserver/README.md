
Plugin for CouchBase Server Monitoring
==============================

Couchbase Server is both a key-value store and a document store, meaning that you can store binary or any other kind of data using Couchbase Server, as well as JSON documents

Our Couchbase Server Plugin is for monitoring the performance metrics of a CouchBase server. 

#Author: Sriram, Zoho Corp
#Language : Python  

PreRequisites
=============

Ensure CouchBase Server is installed in the server and it should be up and running.

Our plugin uses '/pools/default' url to fetch the performance metrics (http://127.0.0.1:8091/_stats).

By default it is configured in the installation of CouchBase Server itself otherwise configure it.

Installation
=============

Go to linux agent plugins directory - '/opt/site24x7/monagent/plugins'

Make a directory in the name 'couchbaseserver'

Download couchbase server plugin from https://github.com/site24x7/plugins/blob/master/couchbaseserver/couchbaseserver.py

Place the plugin file into the couchbaseserver directory

Now the structure should look like '/opt/site24x7/monagent/plugins/couchbaseserver/couchbaseserver.py'


Configurations:
==============

By default CouchBase Server plugin uses the status url 'http://127.0.0.1:8091/_stats' to fetch the performance metrics.

In order to change the configurations, go to plugins directory and edit the required plugin file.

couchbaseserver => /opt/site24x7/monagent/plugins/couchbaseserver/couchbaseserver.py

Make your changes in the config section (sample provided below)


Config Section:
==============

COUCHBASE_SERVER_HOST='127.0.0.1'

COUCHBASE_SERVER_PORT="8091"

COUCHBASE_SERVER_STATS_URI="/pools/default"

COUCHBASE_SERVER_USERNAME=None

COUCHBASE_SERVER_PASSWORD=None


CouchBase Server Plugin Attributes:
===================================

Some of the collected performance metrics are as follows:

`hdd.total` : Total hard disk space

`hdd.quotaTotal` : Hard disk quota

`hdd.usedByData` : Hard disk used for data

`hdd.used` : Used hard disk space

`ram.used` : RAM in use

`ram.quotaUsed` : RAM used for data

`ram.total` : Total RAM