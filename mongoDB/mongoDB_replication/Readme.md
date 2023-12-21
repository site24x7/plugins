# MongoDB Replication Monitoring

                                                                     
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
 - Execute the following command in your server to install pymongo: 

		pip install pymongo
		
		
 Note: Please install the compatibility version of pymongo for your existing Python version
| Python Version | Reference link contains list of compatible pymongo versions                  |
| -------------- | ---------------------------------------------------------------------------- |
| Python 3       | https://www.mongodb.com/docs/drivers/pymongo/#python-3-compatibility          |
| Python 2       | https://www.mongodb.com/docs/drivers/pymongo/#python-2-compatibility         |
---

## Plugin Installation  

- Create a directory named "mongoDB_replication" in your server.		
      
- Download the below files and place it under the "mongoDB_replication" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongoDB/mongoDB_replication/mongoDB_replication.py  && sed -i "1s|^.*|#! $(which python3)|" mongoDB_replication.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongoDB/mongoDB_replication/mongoDB_replication.cfg
  
- Execute the below command with appropriate arguments to check for the valid JSON output:

		python3 mongoDB_replication.py --host "ip_address" --port "port_number" --username "username" --password "password" --dbname "dbname" --authdb "authdb" --tls "False" 



- After the above command with parameters gives the expected output, please configure the relevant parameters in the mongoDB_replication.cfg file.

		[mongoDB-Replication]
		host ="localhost"
		port ="27017"
		username ="None"
		password ="None"
		dbname ="mydatabase"
		authdb="admin"
		tls="False"
		tlscertificatekeyfile="None"
		tlscertificatekeyfilepassword="None"
		tlsallowinvalidcertificates="True"



		
		
- Once above execution was given valid output, then copy the mongoDB_replication directory to Site24x7 Linux Agent plugin directory:
  
 		Linux             ->   /opt/site24x7/monagent/plugins/mongoDB_replication

  
### Performace Metrics


- **Health**:  Indicates the health status of the MongoDB server (1 for healthy).

- **ID**: The identifier for the MongoDB server.

- **Opcounters Repl Command per sec**: Operations count for replicated commands per second.

- **Opcounters Repl Delete per sec**: Operations count for replicated delete commands per second.

- **Opcounters Repl Getmore per sec**: Operations count for replicated getmore commands per second.

- **Opcounters Repl Insert per sec**: Operations count for replicated insert commands per second.

- **Opcounters Repl Query per sec**: Queries count for replicated query per second.

- **Opcounters Repl Update per sec**: Operations count for replicated update commands per second.

- **Oplog First Entry Date**: Date of the first entry in the Oplog.

- **Oplog First Entry Time**: Time of the first entry in the Oplog.

- **Oplog Last Entry Date**: Date of the last entry in the Oplog.

- **Oplog Last Entry Time**: Time of the last entry in the Oplog.

- **Oplog timeDiff**: Time difference between first and last entry in oplog shown in seconds

- **Oplog Log Size MB**: Size of the Oplog in megabytes.

- **Oplog used MB**: Amount of Oplog space used in megabytes.

- **Repl Apply ops per sec**: No of Oplog Operations applied per second during replication.

- **Repl Apply Batches Total millis per sec**: Fraction of Time taken to apply batches during replication.

- **Repl Buffer Count per sec**: Operations count for buffer per second.

- **Repl Buffer Max Size Bytes:**: Maximum size of the buffer in bytes.

- **Repl Buffer Size Bytes**: Current size of the buffer in bytes.

- **Repl Network Bytes per sect**: Network bytes transmitted per second during replication.

- **Repl Network Getmores Num per sec**: Number of getmore operations per second during replication.

- **Repl Network Getmores Total millis per sec**: Fraction of time taken for getmore operations during replication.

- **Repl Network Readers Created per sec**:  Number of network readers created per second during replication.

- **Repl Network ops per sec**: Operations Read count for network per second during replication.

- **Replication Lag**: Lag replicating operations in seconds between the primary and secondary nodes.

- **State**: Numeric representation of the server state(1 for PRIMARY, 2 for SECONDARY).

- **State Str**: String representation of the server state.

- **TTL Deleted Documents per sec**: Number of documents deleted due to TTL Index per second.

- **TTL Passes per sec**: Number of background process removing documents from collections with a ttl index per second.

- **Voting Members Count**: Count of voting members in the replica set.


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7. 

To see the mongoDB_replication monitor in the Site24x7's web client, login Site24x7 with your account, navigate to Server tab -> Plugin Integration -> list of plugin monitors -> user can check the mongoDB_replication monitor.

