# MongoDB Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
---

### Plugin Installation  

- Create a directory named "mongod" under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/mongoDB
      
- Download all the files in the "mongoDB" folder and place it under the "mongoDB" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongoDB/mongoDB.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/mongoDB/mongoDB.cfg

 - Execute the following command in your server to install pymongo: 

		pip install pymongo
		
 Note: Please install the compatibility version of pymongo for your existing Python version
| Python Version | Reference link contains list of compatible pymongo versions                  |
| -------------- | ---------------------------------------------------------------------------- |
| Python 3       | https://www.mongodb.com/docs/drivers/pymongo/#python-3-compatibility         |
| Python 2       | https://www.mongodb.com/docs/drivers/pymongo/#python-2-compatibility         |
		
		

- Execute the below command with appropriate arguments to check for the valid json output:

		python mongoDB.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --dbstats=<dbstats> --replset=<replset> --dbname=<dbname> --authdb=<authdb>


---

### Configurations

- Provide your MongoDb configurations in mongod.cfg file.

		["mongodb"]
		host=<host_name>
		port=<port_number>
		username=<your_username>
		password=<your_password>
		dbstats=<dbstats>
		replset=<replset>
		dbname=<dbname>
		authdb=<authdb>
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

