# Site24x7 MySQL Plugin Playbook


### Use this playbook to install the Site24x7 MySQL plugin to monitor MySQL nodes in remote servers.

---

### How does it work?

There are two playbooks you need to use to install the plugin:
1. site24x7_mysql_grant_privileges.yml playbook that creates a Site24x7 user
2. The site24x7_remote_mysql_node_playbook.yml playbook performs the following processes that are required for the Site24x7 MySQL plugin to collect performance metrics.

- Installs `python3` if not found.
- Installs `pip3` and `pymysql` Python packages if not found.
- Checks the presence of the `Site24x7` monitoring agent.
- If the `pymysql` module does not get installed with pip, it will be installed using the pymysql binary file.
- Creates directories `plugins/mysql` under the `/opt/site24x7/monagent/temp` directory.
- Downloads the files [mysql.py](https://raw.githubusercontent.com/site24x7/plugins/master/mysql/mysql.py) and [mysql.cfg](https://raw.githubusercontent.com/site24x7/plugins/master/mysql/mysql.cfg) from the [Plugins repository](https://github.com/site24x7/plugins/tree/master/mysql) with read, write, and execute permission.
- Configures the `mysql.cfg` file based on the values provided in the `vars` section of the playbook.
- Executes the `mysql.py` file to check for a valid JSON output.
- Finally, it moves the `mysql` directory along with the `mysql.py` and `mysql.cfg` files into the `/opt/site24x7/monagent/plugins` directory.

### Create a Site24x7 MySQL user using the site24x7_mysql_grant_privileges.yml playbook:

To create 'site24x7' user to monitor MySQL, follow below steps

- Change the bind-address = 0.0.0.0 in the MySQL configuration file (/etc/mysql/mysql.conf.d.mysqld.cnf), to connect using remote server.
- The MySQL user should have CREATE, GRANT, UPDATE and RELOAD permission to create a user, grant permission, to update superprivilege, to flush.

		GRANT CREATE USER ON *.* TO 'user'@'hostname';
		GRANT UPDATE, GRANT OPTION ON mysql.* TO 'user'@'hostname';
		GRANT GRANT OPTION ON *.* TO 'username'@'hostname';
		GRANT RELOAD ON *.* TO 'user'@'hostname';

- In the site24x7_mysql_grant_privileges playbook, provide the MySQL user and password in configuration details in the `vars` section of the site24x7_mysql_grant_privileges.yml playbook as shown below.

```yaml
   vars:
     mysql_user: "user"
     mysql_password: "password"
```

### Edit the site24x7_remote_mysql_node_playbook.yml playbook to install the plugin

In the site24x7_remote_mysql_node_playbook.yml playbook, provide the MySQL configuration with respective mysql_node , username and password details in the `vars` section of the playbook as shown below.

```yaml
   vars:
      credential:
        - mysql_node: "node1"
          username: "user"
          password: "password"
        - mysql_node: "node2"
          username: "user"
          password: "password"
```

The below details are required to set the values in the [mysql.cfg](https://github.com/site24x7/plugins/blob/master/mysql/mysql.cfg) file for the plugin.


**mysql_node** : 

The host on which the MySQL instance is running

**port** : 

The port number of the running MySQL instance
	
**username** : 

The MySQL username. If there is no username, set the value as `'"None"'`
	
**password** : 

The MySQL password. If there is no password, set the value as `'"None"'`

**logs_enabled** : 

To enable AppLogs for this plugin, configure logs_enabled=true
	
**log_type_name** : 

To enable AppLogs, configure log_type_name
		
**log_file_path** : 

To enable applog,configure log_file_path

---

### Run the playbooks

Execute the command below to run the playbook that creates the 'site24x7' user to monitor MySQL:
```
ansible-playbook site24x7_mysql_grant_privileges.yml --user <username> -b

```

Execute the command below to run the playbook to install the MySQL plugin in the server where ansible is running:
```
ansible-playbook site24x7_remote_mysql_node_playbook.yml --user <username> -b

```

Once the playbooks are executed, the MySQL plugins will be deployed in the Ansible controller nodes. 

Once the deployment is complete, you can view performance data of the plugin monitors in the SIte24x7 web client.

