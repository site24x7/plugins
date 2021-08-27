Plugin for monitoring MongoDb Atlas performance
==============================================

This plugin monitors the metrics of MongoDb Atlas performance.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
		
- Create a cluster in https://www.mongodb.com and get your public_key and private_key to access API.

- Add your Current IP address on the API key settings everytime you start your mongodb atlas


### Plugin Installation

- Create a directory "mongodb_measurement_of_process" under Site24x7 Linux Agent plugin directory : 

      Linux             ->   /opt/site24x7/monagent/plugins/mongodb_atlas_perf_metrics

---
      
- Download all the files in "mongodb_atlas_perf_metrics" folder and place it under the "mongodb_atlas_perf_metrics" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_atlas_perf_metrics/mongodb_atlas_perf_metrics.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_atlas_perf_metrics/mongodb_atlas_perf_metrics.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python mongodb_atlas_perf_metrics.py --group_id=<your_group_id> --host=<your_host_name> --port=27017 --public_key=<your_public_key> --private_key=<your_private_key>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Configurations
---
- Configure this set up in your cfg file.  

                [mongodb_atlas_perf_metrics]
		group_id=<your_group_id> 
		host=<your_host_name> 
		port=<port_number> 
		public_key=<your_public_key> 
		private_key=<your_private_key>

### Metrics Monitored
---

	groupid                 ->	Unique 24-hexadecimal digit string that identifies the project that owns this Atlas MongoDB process.
	host                    ->	Hostname
	start                   ->	Timestamp in date and time format in UTC when to start retrieving measurements.
	end                     ->	Timestamp in date and time format in UTC when to stop retrieving measurements.
	connections             ->	Number of connections to a MongoDB process found 
	network.in              ->	The total number of bytes that the server has received over network connections initiated by clients or other mongod instances.
	network.out             ->	The total number of bytes that the server has sent over network connections initiated by clients or other mongod instances.
	network.request         ->	The total number of distinct requests that the server has received.
	opcounter.cmd           ->	The total number of commands issued to the database since the mongod instance last started.
	opcounter.query         ->	The total number of queries received since the mongod instance last started.
	opcounter.update        ->	The total number of update operations received since the mongod instance last started.
	opcounter.delete        ->	The total number of delete operations since the mongod instance last started.
	opcounter.getmore       ->	The total number of getMore operations since the mongod instance last started.
	opcounter.insert        ->	The total number of insert operations received since the mongod instance last started
	logicalsize             ->	Size in GB
