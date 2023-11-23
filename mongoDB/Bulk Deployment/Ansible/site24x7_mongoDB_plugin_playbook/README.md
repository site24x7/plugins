
# Site24x7 MongoDB Plugin Playbook


### This playbook is used to install the Site24x7 MongoDB plugin to given MongoDB nodes.

---
### Prerequisites 
To run the playbook, the user has to provide the mongoDB config details in the vars section of the playbook as mentioned below.

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

These details are needed to set the values in the [mongoDB.cfg](https://github.com/site24x7/plugins/blob/master/mongoDB/mongoDB.cfg) file for the plugin.


**mongoDB_host** : 

Host on which the mongoDB is running.

**mongoDB_port** : 

Port number of the running mongoDB instance.
	
**mongoDB_username** : 

MongoDB username, in case of no username, this has to be set as `'"None"'`
	
**mongoDB_password** : 

MongoDB password, in case of no password, this has to be set as `'"None"'`

**mongoDB_dbname** : 

MongoDB database name
	
**mongoDB_authdb** : 

MongoDB authentication database name
		
**mongoDB_tls** : (True/False)
  - `True`: If TLS is enabled for mongoDB connection.
  -  `False`: If TLS is not enabled for mongoDB connection.
		
**mongoDB_tlscertificatekeyfile** : 

Path of the mongoDB certificate key file, in case of no TLS this has to be set as `'"None"'`
	
**mongoDB_tlscertificatekeyfilepassword** : 

Password of the mongoDB certificate key file, in case of no TLS this has to be set as `'"None"'`
	
**mongoDB_tlsallowinvalidcertificates** : 
  - `True` for allowing invalid certificates
  - `False` for not allowing invalid certificates

---

### Running the playbook.

Execute the below command to run the playbook :
```
ansible-playbook site24x7_mongoDB_plugin_playbook.yml --user <username> -b

```


The playbook will perform the following installations, required for the Site24x7 MongoDB plugin to collect the metrics.

- Installing `python3` if not found.
- Installing `pip3` if not found.
- Installing `pymongo` python package if not found.
- Checking the presence of `Site24x7` Agent.
- Creates directories `plugins/mongoDB` under the `/opt/site24x7/monagent/temp` directory.
- Downloads the files `mongoDB.py` and `mongoDB.cfg` from the [plugins repository](https://github.com/site24x7/plugins/tree/master/mongoDB)
   with read, write and execute permission.
- Configures the `mongoDB.cfg` file based on the values given in the `vars` section.
- Executes the `mongoDB.py` file and check for valid `JSON` output.
- Finally moves the `mongoDB` directory along with `mongoDB.py` and `mongoDB.cfg` files into the `/opt/site24x7/monagent/plguins` directory.
