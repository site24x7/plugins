Plugin for CouchDB Monitoring
==============================

CouchDB, is an open source database that completely embraces the web. It is a NoSQL database that uses JSON to store data, uses JavaScript as its query language using MapReduce, and uses HTTP for an API.

Our CouchDB Plugin is for monitoring the performance metrics of a CouchDB server. 

#Author: Sriram, Zoho Corp
#Language : Python

PreRequisites
=============

1.Ensure CouchDB is installed in the server and it should be up and running.

2.This plugin uses '/_stats' url to fetch the performance metrics (http://127.0.0.1:5894/_stats).

3.By default it is configured in the installation of CouchDB itself otherwise configure it.

Installation
=============

Go to linux agent plugins directory - '/opt/site24x7/monagent/plugins'

Make a directory in the name 'couchdb'

Download couchdb plugin from https://github.com/site24x7/plugins/blob/master/couchdb/couchdb.py

Place the plugin file into the couchdb directory

Now the structure should look like '/opt/site24x7/monagent/plugins/couchdb/couchdb.py'


Configurations:
==============

By default CouchDB plugin uses the status url 'http://127.0.0.1:5894/_stats' to fetch the performance metrics.

To change the configurations, go to plugins directory and edit the required plugin file.

couchdb => /opt/site24x7/monagent/plugins/couchdb/couchdb.py

Make your changes in the config section (sample provided below)


Config Section:
==============

COUCHDB_HOST='127.0.0.1'

COUCHDB_PORT="5984"

COUCHDB_STATS_URI="/_stats/"

COUCHDB_USERNAME=None

COUCHDB_PASSWORD=None


CouchDB Plugin Attributes:
=======================

Some of the collected performance metrics are as follows:

`auth_cache_hits` : Number of authentication cache hits.

`auth_cache_misses` : Number of authentication cache misses.

`database_reads` : Number of times a document was read from a database.

`database_writes` : Number of times a database was changed

`open_databases` : Number of open databases

`open_os_files` : Number of file descriptors CouchDB has open

`request_time` : Length of a request inside CouchDB without MochiWeb

`clients_requesting_changes` : Number of clients for continuous _changes

`bulk_requests` : Number of bulk requests

`requests` : Number of HTTP requests

`temporary_view_reads` : Number of temporary view reads

`view_reads` : Number of view reads

`no_of_http_post_requests` : Number of HTTP POST requests

`no_of_http_copy_requests` : Number of HTTP COPY requests

`no_of_http_get_requests` : Number of HTTP GET requests

`no_of_http_head_requests` : Number of HTTP HEAD requests

`no_of_http_move_requests` : Number of HTTP MOVE requests

`no_of_http_put_requests` :  Number of HTTP PUT requests

`no_of_http_200_responses` : Number of HTTP 200 OK responses

`no_of_http_201_responses` : Number of HTTP 201 Created responses

`no_of_http_202_responses` : Number of HTTP 202 Accepted responses

`no_of_http_301_responses` : Number of HTTP 301 Moved Permanently responses

`no_of_http_304_responses` : Number of HTTP 304 Not Modified responses

`no_of_http_400_responses` : Number of HTTP 400 Bad Request responses

`no_of_http_401_responses` : Number of HTTP 401 Unauthorized responses

`no_of_http_403_responses` : Number of HTTP 403 Forbidden responses

`no_of_http_404_responses` : Number of HTTP 404 Not Found responses

`no_of_http_405_responses` : Number of HTTP 405 Method Not Allowed responses

`no_of_http_409_responses` : Number of HTTP 409 Conflict responses

`no_of_http_412_responses` : Number of HTTP 412 Precondition Failed responses

`no_of_http_500_responses` : Number of HTTP 500 Internal Server Error responses
