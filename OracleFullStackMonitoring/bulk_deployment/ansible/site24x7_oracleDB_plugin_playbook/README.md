
# Site24x7 OracleDB Plugin Playbook


### Use this playbook to install the Site24x7 OracleDB plugins in multiple OracleDB instances.

---

### How does it work?

The playbook performs the following processes that are required for the Site24x7 OracleDB plugin to collect performance metrics.

- Installs `python3` if not found.
- Installs `pip3` if not found.
- Installs `oracledb` Python package if not found.
- Checks the presence of the `Site24x7` monitoring agent.


- Creates the below directories under the `/opt/site24x7/monagent/temp` directory.
    - /plugins/OracleCore
    - /plugins/OracleSGA
    - /plugins/OraclePDB
    - /plugins/OracleWaits
    - /plugins/OracleTablespaceDetails
    - /plugins/OracleTablespaceUsage
      
- Download the below files from the [plugins repository](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring) with read, write, and execute permission.
- Configures the files based on the values provided in the `vars` section of the playbook.
- Executes the oracle python files to check for a valid JSON output.
- Finally, it moves all the OracleDB plugin directories from the `/opt/site24x7/monagent/temp` into the `/opt/site24x7/monagent/plugins` directory for the data collection to start happening.



### Prerequisites 
To run the playbook, provide the OracleDB configuration details in the `vars` section of the playbook as shown below.

```yaml
   vars:
      Oracle_host: "localhost"
      Oracle_port: "2484"
      Oracle_username: "None"                           
      Oracle_password: "None"    
      Oracle_home: "/opt/oracle/product/19c/dbhome_1"                         
      Oracle_sid: "ORCL"
      Oracle_tablespace_names: '[\"SYSTEM\",\"USERS\"]'
      Oracle_tablespace_name: "SYSTEM"
      Oracle_tls: "True"
      Oracle_wallet_location: "/opt/oracle/product/19c/dbhome_1/wallet" 
```


**Oracle_host** : 

The host on which the OracleDB instance is running

**Oracle_port** : 

The port number of the running Oracle instance
	
**Oracle_username** : 

The Oracle username. If there is no username, set the value as `"None"`
	
**Oracle_password** : 

The Oracle password. If there is no password, set the value as `"None"`

**Oracle_home** : 

The Oracle Home directory path.
	
**Oracle_sid** : 

The Oracle SID

**Oracle_tablespace_names** : 

Names of the tablespaces, whose usage has to be monitored

**Oracle_tablespace_name** :

Name of the tablespace whose details have to be monitored

**Oracle_tls**: 

- True: If TLS is enabled for OracleDB connection
- False: If TLS is not enabled for OracleDB connection

**Oracle_wallet_location**

- Oracle Wallet Location path

---

### Run the playbook

Execute the command below to run the playbook:
```
ansible-playbook site24x7_oracleDB_plugin_playbook.yml --user <username> 

```

Once the playbook is executed, the OracleDB plugins will be deployed in the Ansible-managed nodes. 

Once the deployment is complete, you can view the performance data of the plugin monitors in the SIte24x7 web client.
