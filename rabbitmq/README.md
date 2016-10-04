
Plugin for RabbitMQ Monitoring
==============================

RabbitMQ is open source message broker software (sometimes called message-oriented middleware) that implements the Advanced Message Queuing Protocol (AMQP). The RabbitMQ server is written in the Erlang programming language and is built on the Open Telecom Platform framework for clustering and failover.

Our RabbitMQ Plugin is for monitoring the performance metrics of a RIAK server. 
  

PreRequisites
=============

Our plugin uses Management Plugin to fetch the performance metrics (http://127.0.0.1:15672/api/overview).

By default it is configured in the installation of RabbitMQ itself otherwise configure it.

Installation
=============

Go to linux agent plugins directory - '/opt/site24x7/monagent/plugins'

Make a directory in the name 'rabbitmq'

Download riak plugin from https://github.com/site24x7/plugins/blob/master/rabbitmq/rabbitmq.py

Place the plugin file into the rabbitmq directory

Now the structure should look like '/opt/site24x7/monagent/plugins/rabbitmq/rabbitmq.py'


Configurations:
==============

By default rabbitmq plugin uses the status url 'http://127.0.0.1:15672/api/overview' to fetch the performance metrics.

In order to change the configurations, go to plugins directory and edit the required plugin file.

rabbitmq => /opt/site24x7/monagent/plugins/rabbitmq/rabbitmq.py

Make your changes in the config section (sample provided below)


Config Section:
==============

RABBITMQ_HOST='localhost'

RABBITMQ_PORT="15672"

RABBITMQ_API_URI="/api/overview"

RABBITMQ_NODES_URI="/api/nodes"

RABBITMQ_USERNAME='guest'

RABBITMQ_PASSWORD='guest'



RabbitMQ Plugin Attributes:
=======================

Some of the collected performance metrics are as follows:

`fd_used` : Used file descriptors

`mem_used` : Memory used in bytes

`run_queue` : Average number of Erlang processes waiting to run shown as process

`sockets_used` : Number of file descriptors used as sockets

`partitions` : Number of network partitions this node is seeing

`consumers` : Number of Consumers

`messages_ready` : Number of messages ready to be delivered to clients

`messages_unack` : Number of messages delivered to clients but not yet acknowledged

`messages_rate`: Count of the total messages in the queue