Plugin for monitoring MongoDb process measurements
==============================================

This plugin monitors the metrics of MongoDb processes.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
		
- Create a cluster in https://www.mongodb.com and get your public_key and private_key to access API.

### Plugin Installation

- Create a directory "mongodb_measurement_of_process" under Site24x7 Linux Agent plugin directory : 

      Linux             ->   /opt/site24x7/monagent/plugins/mongodb_measurement_of_process

---
      
- Download all the files in "mongodb_measurement_of_process" folder and place it under the "mongodb_measurement_of_process" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_measurement_of_process/mongodb_measurement_of_process.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_measurement_of_process/mongodb_measurement_of_process.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python mongodb_cluster.py --group_id=<your_group_id> --host=<your_host_name> --port=27017 --public_key=<your_public_key> --private_key=<your_private_key>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Configurations
---

group_id=<your_group_id>
host=<your_host_name>
port=27017
public_key=<your_public_key>
private_key=<your_private_key>

#Metrics monitored

---

	groupid                 ->	Unique 24-hexadecimal digit string that identifies the project that owns this Atlas MongoDB process.
	host                    ->	Hostname
	start                   ->	Timestamp in date and time format in UTC when to start retrieving measurements.
	end                     ->	Timestamp in date and time format in UTC when to stop retrieving measurements.
	connections             ->	Number of connections to a MongoDB process found 
	NETWORK_BYTES_IN        ->	The total number of bytes that the server has received over network connections initiated by clients or other mongod instances.
	NETWORK_BYTES_OUT       ->	The total number of bytes that the server has sent over network connections initiated by clients or other mongod instances.
	NETWORK_NUM_REQUESTS    ->	The total number of distinct requests that the server has received.
	OPCOUNTER_CMD           ->	The total number of commands issued to the database since the mongod instance last started.
	OPCOUNTER_QUERY         ->	The total number of queries received since the mongod instance last started.
	OPCOUNTER_UPDATE        ->	The total number of update operations received since the mongod instance last started.
	OPCOUNTER_DELETE        ->	The total number of delete operations since the mongod instance last started.
	OPCOUNTER_GETMORE       ->	The total number of getMore operations since the mongod instance last started.
	OPCOUNTER_INSERT        ->	The total number of insert operations received since the mongod instance last started
	LOGICAL_SIZE            ->	Size in GB


