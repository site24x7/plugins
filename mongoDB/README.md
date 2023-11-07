# MongoDB Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
---

### Plugin Installation  

- Create a directory named "mongoDB" in your server.		
      
- Download the below files and place it under the "mongoDB" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongoDB/mongoDB.py  && sed -i "1s|^.*|#! $(which python3)|" mongoDB.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongoDB/mongoDB.cfg
		
### Prerequisites

 - Execute the following command in your server to install pymongo: 

		pip install pymongo
		
		
 Note: Please install the compatibility version of pymongo for your existing Python version
| Python Version | Reference link contains list of compatible pymongo versions                  |
| -------------- | ---------------------------------------------------------------------------- |
| Python 3       | https://www.mongodb.com/docs/drivers/pymongo/#python-3-compatibility         |
| Python 2       | https://www.mongodb.com/docs/drivers/pymongo/#python-2-compatibility         |

### Configurations

- Provide your MongoDb configurations in mongoDB.cfg file.

		[mongo_db]
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


- Execute the below command with appropriate arguments which were given in the configuration to check for the valid output with JSON format.

		python mongoDB.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --dbname=<dbname> --authdb=<authdb> --tls=False 
		
		
- Once above execution was given valid output, then copy the mongoDB directory to Site24x7 Linux Agent plugin directory:
  
 		Linux             ->   /opt/site24x7/monagent/plugins/mongoDB

  
### Performace Metrics


- **Asserts Msg per sec**: The rate at which message assertion failures occur per second.

- **Asserts Regular per sec**: The rate at which regular assertion failures occur per second.

- **Asserts User per sec**: The rate at which user-related assertion failures occur per second.

- **Asserts Warning per sec**: The rate at which assertion warning failures occur per second.

- **Bytes Currently in the Cache**: The number of bytes currently stored in the cache.

- **Concurrent Transactions Read Available**: The number of available concurrent transactions for reading operations.

- **Concurrent Transactions Read Out**: The number of concurrent transactions for reading operations that are currently active.

- **Concurrent Transactions Read Total Tickets**: The total number of tickets available for concurrent read transactions.

- **Concurrent Transactions Write Available**: The number of available concurrent transactions for write operations.

- **Concurrent Transactions Write Out**: The number of concurrent transactions for write operations that are currently active.

- **Concurrent Transactions Write Total Tickets**: The total number of tickets available for concurrent write transactions.

- **Connections Available**: The number of available database connections.

- **Current Connections**: The current number of active database connections.

- **Document Deleted per sec**: The rate at which documents are being deleted from the database per second.

- **Document Inserted per sec**: The rate at which documents are being inserted into the database per second.

- **Document Returned per sec**: The rate at which documents are being retrieved from the database per second.

- **Document Updated per sec**: The rate at which documents are being updated in the database per second.

- **Extra Info Page Faults per sec**: The rate at which page faults involving extra information occur per second.

- **Memory Bits**: The number of memory bits.

- **Memory Mapped**: Memory mapped value.

- **Memory Resident**: The amount of memory marked as "resident" in the system.

- **Memory Virtual**: The total virtual memory size.

- **Metrics cursor Open NoTimeout**: The number of open cursor metrics without timeouts.

- **Metrics cursor Open Pinned**: The number of open cursor metrics that are pinned.

- **Metrics cursor Open Total**: The total number of open cursor metrics.

- **Metrics cursor Timed Out**: The number of cursor metrics that have timed out.

- **Network Bytes In per sec**: The rate at which bytes are being received over the network per second.

- **Network Bytes Out per sec**: The rate at which bytes are being sent out over the network per second.

- **Network Num Requests per sec**: The rate at which network requests are being made per second.

- **OpLatencies Commands Latency**: Latency for processing commands, possibly in microseconds.

- **OpLatencies Reads Latency**: Latency for read operations, possibly in microseconds.

- **OpLatencies Writes Latency**: Latency for write operations, possibly in microseconds.

- **Opcounters Command per sec**: The rate at which command operations are counted per second.

- **Opcounters Delete per sec**: The rate at which delete operations are counted per second.

- **Opcounters Getmore per sec**: The rate at which "get more" operations are counted per second.

- **Opcounters Insert per sec**: The rate at which insert operations are counted per second.

- **Opcounters Query per sec**: The rate at which query operations are counted per second.

- **Opcounters Update per sec**: The rate at which update operations are counted per second.

- **Stats Collections**: The number of collections.

- **Stats Data Size**: The size of data.

- **Stats Index Size**: The size of indexes.

- **Stats Indexes**: The number of indexes.

- **Stats Objects**: The number of objects.

- **Stats Storage Size**: The size of storage.

- **Total Connections Created**: The total number of connections created since the database/server started.

- **Total no of dbs**: The total number of databases on the system.

- **Uptime**: The total uptime of the database or system.

- **version**: The version of the MongoDB database.



The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7. 

To see the mongoDb monitor in the Site24x7's web client, login Site24x7 with your account, navigate to Server tab -> Plugin Integration -> list of plugin monitors -> user can check the mongoDB monitor.


