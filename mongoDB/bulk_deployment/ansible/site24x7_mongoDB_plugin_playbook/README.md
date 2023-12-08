
# Site24x7 MongoDB Plugin Playbook


### Use this playbook to install the Site24x7 MongoDB plugin in multiple MongoDB nodes.

---

### How does it work?

The playbook performs the following processes that are required for the Site24x7 MongoDB plugin to collect performance metrics.

- Installs `python3` if not found.
- Installs `pip3` if not found.
- Installs `pymongo` Python package if not found.
- Checks the presence of the `Site24x7` monitoring agent.
- Creates directories `plugins/mongoDB` under the `/opt/site24x7/monagent/temp` directory.
- Downloads the files [mongoDB.py](https://raw.githubusercontent.com/site24x7/plugins/master/mongoDB/mongoDB.py) and [mongoDB.cfg](https://raw.githubusercontent.com/site24x7/plugins/master/mongoDB/mongoDB.cfg) from the [plugins repository](https://github.com/site24x7/plugins/tree/master/mongoDB)
   with read, write, and execute permission.
- Configures the `mongoDB.cfg` file based on the values provided in the `vars` section of the playbook.
- Executes the `mongoDB.py` file to check for a valid JSON output.
- Finally, it moves the `mongoDB` directory along with the `mongoDB.py` and `mongoDB.cfg` files into the `/opt/site24x7/monagent/plugins` directory.

### Prerequisites 
To run the playbook, provide the MongoDB configuration details in the `vars` section of the playbook as shown below.

```yaml
   vars:
      mongoDB_host: "mongoDB_host"
      mongoDB_port: "27017"
      mongoDB_username: '"None"'
      mongoDB_password: '"None"'
      mongoDB_dbname: "mydatabase"
      mongoDB_authdb: "admin"
      mongoDB_tls: False
      mongoDB_tlscertificatekeyfile: '"None"'
      mongoDB_tlscertificatekeyfilepassword: '"None"'
      mongoDB_tlsallowinvalidcertificates: False
```

The details below are required to set the values in the [mongoDB.cfg](https://github.com/site24x7/plugins/blob/master/mongoDB/mongoDB.cfg) file for the plugin.


**mongoDB_host** : 

The host on which the MongoDB instance is running

**mongoDB_port** : 

The port number of the running MongoDB instance
	
**mongoDB_username** : 

The MongoDB username. If there is no username, set the value as `'"None"'`
	
**mongoDB_password** : 

The MongoDB password. If there is no password, set the value as `'"None"'`

**mongoDB_dbname** : 

The name of the MongoDB database
	
**mongoDB_authdb** : 

The MongoDB authentication database name
		
**mongoDB_tls** : (True/False)
  - `True`: If TLS is enabled for MongoDB connection
  -  `False`: If TLS is not enabled for MongoDB connection
		
**mongoDB_tlscertificatekeyfile** : 

The path of the MongoDB certificate key file. If there is no TLS, set the value as `'"None"'`
	
**mongoDB_tlscertificatekeyfilepassword** : 

The password of the MongoDB certificate key file. If there is no TLS, set the value as `'"None"'`
	
**mongoDB_tlsallowinvalidcertificates** : 
  - `True` for allowing invalid certificates
  - `False` for not allowing invalid certificates

---

### Run the playbook

Execute the command below to run the playbook:
```
ansible-playbook site24x7_mongoDB_plugin_playbook.yml --user <username> -b

```

Once the playbook is executed, the MongoDB plugins will be deployed in the Ansible managed nodes. 

Once the deployment is complete, you can view performance data of the plugin monitors in the SIte24x7 web client.
