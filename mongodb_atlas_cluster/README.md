# MongoDB Atlas Cluster Monitoring


                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Install **python3.6** or higher version on the server.

---

### Plugin Installation  

- Create a directory named "mongodb_atlas_cluster".
	
- Download the below files in the "mongodb_atlas_cluster".

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_atlas_cluster/mongodb_atlas_cluster.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_atlas_cluster/mongodb_atlas_cluster.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mongodb_atlas_cluster.py script.

- Execute the below command with appropriate arguments to check for the valid json output:
	```
    python3 monogdb_atlas_cluster.py --public_key=<public_key> --private_key=<private_key>--group_project_id=<group or project id> --cluster_name=<atlas cluster name>	 
    ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the mongodb_atlas_cluster.cfg file.

	```
    [mongodb_atlas]
    group_id= <your_group_id>
    public_key = <your_public_key>
    private_key = <your_private_key>
    cluster_name=<cluster_name>

	```	
- Move the "mongodb_atlas_cluster" folder into the Site24x7 Linux Agent plugin directory: 
	```
	Linux             ->   /opt/site24x7/monagent/plugins/mongodb_atlas_cluster
	```
	```
	Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\mongodb_atlas_cluster
	```

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.





## Supported Metrics
The following metrics are captured in the mongodb_atlas_cluster plugin:

- **analytics_nodes**

    Number of analytics nodes in the region.
- **clustertype**  

    Type of the cluster

- **disksize**                 
    
    Capacity, in gigabytes, of the host's root volume. 

- **electable_nodes**          

    Number of electable nodes in the region.

- **maxinstance_size**         

    Maximum instance size to which your cluster can automatically scale.

- **mininstanc_size**          

    Minimum instance size to which your cluster can automatically scale.
- **mongodb_majorversion**     

    Major version of MongoDB the cluster runs

- **mongodb_version**          

    Version of MongoDB the cluster runs

- **mongo_uri_updated**        

    Timestamp in date and time format in UTC when the connection string was last updated. 

- **name**                     
    
    Name of the cluster to retrieve.

- **numshards**                

    Positive integer that specifies the number of shards for a sharded cluster.


- **pitenabled**           

    Flag that indicates if the cluster uses Continuous Cloud Backup backups.

- **priority**                 
    
    Election priority of the region. 
- **provider_backup_enabled**  

    Flag that indicates if the cluster uses Cloud Backups for backups.

- **providername**             

    Cloud service provider on which Atlas provisioned the hosts.

- **readonly_nodes**           
    
    Number of read-only nodes in the region.
- **replication_factor**       

    Number of replica set members
- **rootcert_type**            

    Certificate Authority that MongoDB Atlas clusters use.
- **srvaddress**               
    
    Connection string for connecting to the Atlas cluster. 
- **statename**                
    
    Current state of the cluster. 
- **zonename**                 

    Name for the zone.
