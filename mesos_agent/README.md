
Plugin for Apache Mesos Monitoring
==================================

Apache Mesos is an open source cluster manager that handles workloads in a distributed environment through dynamic resource sharing and isolation. Mesos is suited for the deployment and management of applications in large-scale clustered environments.

Configure the host, port, username and password in the python plugin to get the metrics monitored in the Site24x7 Servers

Metrics monitored 
=================

- master_slave_registrations - #Number of agents that were able to cleanly re-join the cluster and connect back to the master after the master is disconnected.
- master_master_slave_reregistrations - #Number of agent re-registrations
- master_slave_removals - #Number of agent removed for various reasons, including maintenance
- master_slave_shutdowns_scheduled - #Number of agents which have failed their health check and are scheduled to be removed. 
- master_slave_shutdowns_canceled - #Number of cancelled agent shutdowns. 
- master_slave_shutdowns_completed - #Number of agents that failed their health check.
- master_slaves_active - #Number of active agents
- master_slaves_connected - #Number of connected agents	
- master_slaves_disconnected - #Number of disconnected agents
- master_slaves_inactive - #Number of inactive agents
