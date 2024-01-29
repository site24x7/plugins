
# Oracle Full Stack Monitoring
___

## The Oracle Full Stack Monitoring includes the following plugins

- [Oracle Core Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OracleCore)
- [Oracle PDB Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OraclePDB)
- [Oracle Tablespace Details Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OracleTablespaceDetails)
- [Oracle Tablespace Usage Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OracleTablespaceUsage)
- [Oracle Waits Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OracleWaits)

All the plugins listed are made from the perspective of **Oracle Database Tuning**. By viewing these various plugins and their metrics one can get various insights on how to tune and use their oracle instance efficiently.


## Prerequisites for the Plugins

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.7 or higher version should be installed.
- Install **oracledb** module for python
	```
	pip3 install oracledb
	```

- Roles need to be granted

	```
	grant select_catalog_role to {username}
	```
	```
	grant create session to {username}
	```


## Setting plugin prerequisites 
The Oracle plugin prerequisites can be set using the **SetenvPrerequisites.py** file. To run the **SetenvPrerequisites.py** script, the below command should be executed. Executing the below command will install the **oracledb** python module. And also creates a new user and grants the below privileges to the user.

- grant select_catalog_role to {username}
- grant create session to {username}

```
./SetenvPrerequisites.py --sysusername "sysusername" --syspassword "syspassword" --username "username" --password "password" --sid "sid"  --hostname "hostname" --port "port" --tls "tls" --wallet_location "wallet_location" --oracle_home "oracle_home"
```
- **sysusername :**
  
  This user should be a DBA user with user creation previleges.

- **syspassword :**
  
  This is the password for the sysusername

- **username :**
  
  This username is the user to be created

- **password :**
  
  This is the password to be created for the new user in the username

- **sid :**
  
  sid of the oracle instance

- **hostname :**
  
  hostname of the oracle instance

- **port :**
  
  port of the oracle instance

- **tls :**

  tls option for the oracle instance (true/ false)

- **wallet_location :**
  
  wallet_location of the oracle_instance

- **oracle_home :**
  
  oracle home path for the oracle instance


  
  


