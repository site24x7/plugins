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
		

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7. 

To see the mongoDb monitor in the Site24x7's web client, login Site24x7 with your account, navigate to Server tab -> Plugin Integration -> list of plugin monitors -> user can check the mongoDB monitor.


