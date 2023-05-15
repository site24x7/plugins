Plugin for monitoring MongoDb Atlas Cluster
==============================================

This plugin monitors the availability and state of mongodb atlas cluster.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
		
- Create a cluster in https://www.mongodb.com and get your public_key and private_key to access API.

- Add your Current IP address on the API key settings everytime you start your mongodb atlas

### Plugin Installation  

- Create a directory "mongodb_atlas" :
      
- Download all the files in "mongodb_atlas" folder and place it under the "mongodb_atlas" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_atlas/mongodb_atlas.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_atlas/mongodb_atlas.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python mongodb_atlas.py --group_id=<your_group_id> --public_key=<your_public_key> --private_key=<your_private_key>
		
- Move the directroy "mongodb_atlas"  under Site24x7 Linux Agent plugin directory :

		Linux             ->   /opt/site24x7/monagent/plugins/mongodb_atlas


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Configurations

- Configure this set up in your cfg file 
                
		[mongodb_atlas]
		group_id = <group_id> 
		public_key = <public_key>
		private_key = <your_private_key>

### Metrics Monitored


---

	analytics_nodes          ->	Number of analytics nodes in the region.
	clustertype              ->	Type of the cluster
	disksize                 ->	Capacity, in gigabytes, of the host's root volume. 
	electable_nodes          ->	Number of electable nodes in the region.
	maxinstance_size         ->	Maximum instance size to which your cluster can automatically scale.
	mininstanc_size          ->	Minimum instance size to which your cluster can automatically scale.
	mongodb_majorversion     ->	Major version of MongoDB the cluster runs
	mongodb_version          ->	Version of MongoDB the cluster runs
	mongo_uri_updated        ->	Timestamp in date and time format in UTC when the connection string was last updated. 
	name                     ->	Name of the cluster to retrieve.
	numshards                ->	Positive integer that specifies the number of shards for a sharded cluster.
	pitenabled               ->	Flag that indicates if the cluster uses Continuous Cloud Backup backups.
	priority                 ->	Election priority of the region. 
	provider_backup_enabled  ->	Flag that indicates if the cluster uses Cloud Backups for backups.
	providername             ->	Cloud service provider on which Atlas provisioned the hosts.
	readonly_nodes           ->	Number of read-only nodes in the region.
	replication_factor       ->	Number of replica set members
	rootcert_type            ->	Certificate Authority that MongoDB Atlas clusters use.
	srvaddress               ->	Connection string for connecting to the Atlas cluster. 
	statename                ->	Current state of the cluster. 
	zonename                 ->	Name for the zone.
