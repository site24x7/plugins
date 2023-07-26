# IBM DB2 Monitoring

                                                                                       
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install ibm_db module for python
	```
	  pip install ibm_db
	```
---



### Plugin Installation  

- Create a directory named "ibm_db2_core".
      
- Download all the files in the "ibm_db2_core" folder and place it under the "ibm_db2_core" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_db2/ibm_db2_core/ibm_db2_core.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_db2/ibm_db2_core/ibm_db2_core.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the ibm_db2_core.py script.
 
- Execute the below command with appropriate arguments to check for the valid json output:
	```
	 python3 ibm_db2_core.py --host <hostname> --port <port no> --username <username> --password <password> --sample_db <db name>
	 ```
- Move the folder "ibm_db2_core" into the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/ibm_db2_core 
		
Since it's a python plugin, to run in windows server please follow the steps in below link, remaining configuration steps are exactly the same. 

  https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers



---

### Configurations

- Provide your IBM MQ configurations in ibm_db2_core.cfg file.
	```
	  [ibm_db_2]
	  host 	= "<hostname>"
	  port 	= "<port>"
	  username	= "<username>"
	  password 	= "<password>"
	  sample_db	= "<sample_db>"
	```	
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics
The following metrics are captured :

- **no_of_bufferpools**
    
    Total number of bufferpools

- **total_logical_reads**

    Total number of logical reads

- **total_physical_reads**

    Total number of physical reads

- **total_hit_ratio_percent**

    Percentage of total hit ratio

- **data_logical_reads**

    Number of pages read from data cache

- **data_physical_reads**

    Number of pages read from disk

- **data_hit_ratio_percent**

    Data hit ratio, that is, the percentage of time that the database manager did not need to load a page from disk to service a data page request.


- **index_logical_reads**

    Indicates the number of index pages which have been requested from the buffer pool (logical) for regular and large table spaces.


- **index_hit_ratio_percent**

     The percentage of the index reads that did not require physical disk access


- **xda_logical_reads**

    Number of data pages for XML storage objects (XDAs) which have been requested from the buffer pool (logical) for regular and large table spaces

- **xda_hit_ratio_percent**

    Auxiliary storage objects hit ratio.


- **log_utilization_percent**

    Percent utilization of total log space.


- **total_log_used_kb**

    Utilization of total log space in KB


- **total_log_available_kb**

    Total log avilable in KB


- **appls_cur_cons**

    Indicates the number of applications that are currently connected to the database.

- **appls_in_db2**

    Number of applications that are currently connected to the database, and for which the database manager is currently processing a request

- **connections_top**

    The highest number of simultaneous connections to the database since the database was activated.

- **db_status**

    The current status of the database.

- **deadlocks**

    Total number of deadlocks

- **lock_list_in_use**

    Number of pages currently in use by the lock list

- **lock_timeouts**

    The number of times that a request to lock an object timed out instead of being granted. 

- **lock_wait_time**

    The total elapsed time spent waiting for locks. 

- **lock_waits**

    Total number of lock waits

- **num_locks_held**

    Total number of locks held

- **num_locks_waiting** 

    Number of agents waiting on a lock

- **rows_modified**

    Total number of rows modified


- **rows_read**

    Total number of rows read


- **rows_returned**

    Total number of rows returned

- **total_cons**

    Total number of connections attempted from the DB2 Connect
