
Plugin for Riak Monitoring
==============================

Riak is a distributed NoSQL key-value data store that offers high availability, fault tolerance, operational simplicity, and scalability.

Our Riak Plugin is for monitoring the performance metrics of a RIAK server. 
  

PreRequisites
=============

Ensure Riak is installed in the server and it should be up and running.

Our plugin uses '/stats' url to fetch the performance metrics (http://127.0.0.1:8098/stats).

By default it is configured in the installation of Riak itself otherwise configure it.

Installation
=============

Go to linux agent plugins directory - '/opt/site24x7/monagent/plugins'

Make a directory in the name 'riak'

Download riak plugin from https://github.com/site24x7/plugins/blob/master/riak/riak.py

Place the plugin file into the riak directory

Now the structure should look like '/opt/site24x7/monagent/plugins/riak/riak.py'


Configurations:
==============

By default Riak plugin uses the status url 'http://127.0.0.1:8098/stats' to fetch the performance metrics.

In order to change the configurations, go to plugins directory and edit the required plugin file.

riak => /opt/site24x7/monagent/plugins/riak/riak.py

Make your changes in the config section (sample provided below)


Config Section:
==============

RIAK_HOST='127.0.0.1'

RIAK_PORT="8098"

RIAK_STATS_URI="/stats/"

RIAK_USERNAME=None

RIAK_PASSWORD=None


Riak Plugin Attributes:
=======================

Some of the collected performance metrics are as follows:

`pbc_active` : Number of active protocol buffers connections

`pbc_connects` : Number of protocol buffers connections

`read_repairs` : Number of read repair operations this this node has coordinated in the last minute

`memory_atom` : Total amount of memory currently allocated for atom storage

`memory_atom_used` : Total amount of memory currently used for atom storage

`memory_binary` : Total amount of memory used for binaries

`memory_code` : Total amount of memory allocated for Erlang code

`memory_ets` : Total memory allocated for Erlang Term Storage

`memory_processes` : Total amount of memory allocated for Erlang processes

`memory_processes_used` : Total amount of memory used by Erlang processes

`memory_total` : Total allocated memory

`node_get_fsm_active_60s` : Number of active GET FSMs

`node_get_fsm_in_rate` : Average number of GET FSMs enqueued by Sidejob

`node_get_fsm_out_rate` : Average number of GET FSMs dequeued by Sidejob

`node_get_fsm_rejected_60s` : Number of GET FSMs actively being rejected by Sidejob's overload protection

`node_gets` : Number of GETs coordinated by this node

`node_put_fsm_active_60s` :  Number of active PUT FSMs

`node_put_fsm_in_rate` : Average number of PUT FSMs enqueued by Sidejob

`node_put_fsm_out_rate` : Average number of PUT FSMs dequeued by Sidejob

`node_put_fsm_rejected_60s` : Number of PUT FSMs actively being rejected by Sidejob's overload protection

`node_puts` : Number of PUTs coordinated by this node

`vnode_gets` : Number of GET operations coordinated by vnodes on this node

`vnode_index_deletes` : Number of vnode index delete operations

`vnode_index_reads` : Number of vnode index read operations

`vnode_index_writes` : Number of vnode index write operations

`vnode_puts` : Number of PUT operations coordinated by vnodes on this node shown as operation