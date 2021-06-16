Plugin for monitoring MongoDb Cluster
==============================================

This plugin monitors the metrics of MongoDb Cluster.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
		
- Create a cluster in https://www.mongodb.com and get your public_key and private_key to access API.

### Plugin Installation

- Create a directory "mongodb_cluster" under Site24x7 Linux Agent plugin directory : 

      Linux             ->   /opt/site24x7/monagent/plugins/mongodb_cluster

---
      
- Download all the files in "mongodb_cluster" folder and place it under the "mongodb_cluster" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_cluster/mongodb_cluster.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_cluster/mongodb_cluster.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python mongodb_cluster.py --group_id=<your_group_id> --public_key=<your_public_key> --private_key=<your_private_key>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Configurations
---

group_id =<your_group_id>
public_key =<your_public_key>
private_key =<your_private_key>

#Metrics monitored

---

	analyticsNodes         ->	Number of analytics nodes in the region.
	clusterType            ->	Type of the cluster
	diskSizeGB             ->	Capacity, in gigabytes, of the host's root volume. 
	electableNodes         ->	Number of electable nodes in the region.
	maxInstanceSize        ->	Maximum instance size to which your cluster can automatically scale.
	minInstanceSize        ->	Minimum instance size to which your cluster can automatically scale.
	mongoDBMajorVersion    ->	Major version of MongoDB the cluster runs
	mongoDBVersion         ->	Version of MongoDB the cluster runs
	mongoURIUpdated        ->	Timestamp in date and time format in UTC when the connection string was last updated. 
	name                   ->	Name of the cluster to retrieve.
	numShards              ->	Positive integer that specifies the number of shards for a sharded cluster.
	pitEnabled             ->	Flag that indicates if the cluster uses Continuous Cloud Backup backups.
	priority               ->	Election priority of the region. 
	providerBackupEnabled  ->	Flag that indicates if the cluster uses Cloud Backups for backups.
	providerName           ->	Cloud service provider on which Atlas provisioned the hosts.
	readOnlyNodes          ->	Number of read-only nodes in the region.
	replicationFactor      ->	Number of replica set members
	rootCertType           ->	Certificate Authority that MongoDB Atlas clusters use.
	srvAddress             ->	Connection string for connecting to the Atlas cluster. 
	stateName              ->	Current state of the cluster. 
	zoneName               ->	Name for the zone.

