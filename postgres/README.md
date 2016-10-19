
Plugin for PostgreSQL Monitoring
=================================

For monitoring the performance metrics of your PostgreSQL database using Site24x7 Server Monitoring Plugins. 
  
### Author: Tarun, Zoho Corp
### Language : Python
### Tested in Ubuntu


Before you start 
=================

1. Install Site24x7 Server Agent 
2. Download postgres plugin from https://raw.githubusercontent.com/site24x7/plugins/master/postgres/postgres.py
3. Place the plugin folder 'postgres/postgres.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)
4. This plugin requires Python module "psycopg2" to fetch the statistics from postgres database.
5. For installing "psycopg2" please refer http://initd.org/psycopg/docs/install.html#installation .

Configure postgres to support statistics
=======================================

1. Create a username with password based authentication and grant superuser rights to this user.
		CREATE USER username WITH PASSWORD 'yourpassword' SUPERUSER;

2. Make sure the postgres database server is configured to allow password and md5 authenticated connections.


Configure the agent plugin
==========================
 
Make the following changes in the pgsql plugin file ( copied to agent's plugin directory earlier ).
 
- Replace the shebang character "#!" in line 1 to the appropriate path for python's version where you have installed psycopg2 in your system. Eg : 
		#!/usr/bin/python2
- Change the value of global variables 'userName' , 'passWord' to the value configured in above steps. Eg : 
		userName = "username"
		passWord = "yourPassword"
- Also set the appropriate values for variables "db" , "hostName" and "port"
	 
- Save the changes and restart the agent.
 
		/etc/init.d/site24x7monagent restart

Site24x7 agent will now report pgsql statistics in the plugins tab under the site24x7.com portal.


PostgreSQL Plugin Attributes:
=============================

Some of the collected pgsql attributes are as follows:

- General information:

		"table_count" :  Total number of tables in the current database.
		"locks_count" : Total number of locks in database.
		"VERSION" : Numerical representation of the PostgreSQL Database version.
		"Error occured" : Is set to 1 if plugin execution encountered some error.
		"Error reason" : Contains the text of the exception invoked during plugin execution (if any).

- Connection Usage statistics:

		"users_idle_count" : Number of currently idle users/backends connected to the database.
		"users_active_count" : Number of currently actine users/backends connected to the database

- Database statistics:

		"db_conflicts": Sum of number of queries canceled due to conflicts with recovery across all databases.
		"db_cache_usage_ratio": Usage rate of the cache, calculated using SUM(blks_hit) / SUM(blks_read).
		"db_rollbacks": Sum of number of transactions that have been rolled back across all databases.
		"db_commits": Sum of number of transactions that have been commited across all databases.

- Background writer process's statistics:

		"buffers_backend": Number of buffers written directly by a backend.
		"buffers_alloc": Number of buffers allocated.
		"buffers_checkpoint": Number of buffers written during checkpoints.
		"checkpoints_timed": Number of scheduled checkpoints that have been performed.
		"checkpoints_req": Number of requested checkpoints that have been performed.
		"maxwritten_clean": Number of times the background writer stopped a cleaning scan because it had written too many buffers.

