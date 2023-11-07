# MongoDB Atlas Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
---

### Plugin Installation  

- Create a directory named "mongodb_atlas" in your server.		
      
- Download the below files and place them under the "mongodb_atlas" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_atlas/mongodb_atlas.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_atlas/mongodb_atlas.cfg
		
### Prerequisites

 - Execute the following command in your server to install Pymongo: 

		pip install pymongo
		
		
 Note: Please install the compatibility version of Pymongo for your existing Python version
| Python Version | Reference link contains a list of compatible Pymongo versions                  |
| -------------- | ---------------------------------------------------------------------------- |
| Python 3       | https://www.mongodb.com/docs/drivers/pymongo/#python-3-compatibility         |
| Python 2       | https://www.mongodb.com/docs/drivers/pymongo/#python-2-compatibility         |

### Configurations

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mongodb_atlas.py script.

- Provide your mongodb_atlas configurations in mongodb_atlas.cfg file.

        [mongo_db_atlas]
        mongo_connect_string =<mongodb connection string>
        dbname=<mongodb database name>


- Execute the below command with appropriate arguments which were given in the configuration to check for the valid output with JSON format.
	```
	python3 mongodb_atlas.py  --mongo_connect_string <mongodb connection string> --dbname <monogdb database name>
	```
		
- Once the above execution was given valid output, then copy the mongodb_atlas directory to the Site24x7 Linux Agent plugin directory:
  
 		Linux             ->   /opt/site24x7/monagent/plugins/mongodb_atlas
		
**Note:** 

`While entering the connection string make sure to encode the password if it has special characters.`

**Example Password:**

`Actual Password: test@123`

`Encoded Password: test%40123`

**Example Connection String:**

`mongodb+srv://test:test%40123@atlascluster.xyltq3c.mongodb.net/?retryWrites=true&w=majority`

### Performace Metrics

- Asserts Msg per sec
- Asserts Regular per sec
- Asserts User per sec
- Asserts Warning per sec
- Bytes Currently in the Cache
- Concurrent Transactions Read Available
- Concurrent Transactions Read Out
- Concurrent Transactions Read Total Tickets
- Concurrent Transactions Write Available
- Concurrent Transactions Write Out
- Concurrent Transactions Write Total Tickets
- Connections Available
- Current Connections
- Document Deleted per sec
- Document Inserted per sec
- Document Returned per sec
- Document Updated per sec
- Extra Info Page Faults per sec
- Memory Bits
- Memory Mapped
- Memory Resident
- Memory Virtual
- Metrics cursor Open NoTimeout
- Metrics cursor Open Pinned
- Metrics cursor Open Total
- Metrics cursor Timed Out
- Network Bytes In per sec
- Network Bytes Out per sec
- Network Num Requests per sec
- OpLatencies Commands Latency
- OpLatencies Reads Latency
- OpLatencies Writes Latency
- Opcounters Command per sec
- Opcounters Delete per sec
- Opcounters Getmore per sec
- Opcounters Insert per sec
- Opcounters Query per sec
- Opcounters Update per sec
- Stats Collections
- Stats Data Size
- Stats Index Size
- Stats Indexes
- Stats Objects
- Stats Storage Size
- Total Connections Created
- Total no of dbs
- Uptime
- version


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7. 

To see the mongodb_atlas monitor in the Site24x7's web client, login Site24x7 with your account, navigate to Server tab -> Plugin Integration -> list of plugin monitors -> user can check the mongodb_atlas monitor.


