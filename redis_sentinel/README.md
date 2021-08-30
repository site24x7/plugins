Plugin for Monitoring Redis Sentinel
==============================================

Redis Sentinel is the high availability solution for open-source Redis server.  In case of a failure in your Redis cluster, Sentinel will automatically detect the point of failure and bring the cluster back to stable mode without any human intervention.

Follow the below steps to configure the Redis Sentinel plugin and to monitor metrics for providing in-depth visibility into the performance, availability, and usage stats of Redis Sentinel.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
		

### Plugin installation
---
##### Linux 

- Create a folder "redis_sentinel" under Site24x7 Linux Agent plugin directory : 

      Linux            ->   /opt/site24x7/monagent/plugins/redis_sentinel

---

- Download the file in "redis_sentinel" folder and place it under the "redis_sentinel" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/redis_sentinel/redis_sentinel.py

- Execute the below command with appropriate arguments to check for the valid json output. 

		python redis_sentinel.py --port=<PORT_FOR_REDIS_SENTINEL> --master=<MASTER_NAME_TO_MONITOR>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured
---
	sentinel_masters                  ->  Number of master in redis sentinel
	sentinel_running_scripts          ->  Number of running scripts in sentinel
	last_ok_ping_reply                ->  Number of seconds since last OK ping
	link_pending_commands             ->  Number of pending sentinel commands
	num_slaves                        ->  Number of slaves detected
	num_other_sentinels               ->  Number of other sentinels detected
	role_reported_time                ->  Time in which the role is reported
	sentinel_scripts_queue_length     ->  Queue length of sentinel scripts
	last_ping_reply                   ->  Number of seconds since last ping reply
	sentinel_simulate_failure_flags   ->  Checks whether master is down
	last_ping_sent                    ->  Last ping sent in master
	quorum                            ->  Number of quorums in sentinel to detect the failure
