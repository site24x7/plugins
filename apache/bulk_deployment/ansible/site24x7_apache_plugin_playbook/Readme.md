
# Site24x7 Apache Plugin Playbook


### Use this playbook to install the Site24x7 Apache plugin in multiple Apache nodes.

---

### How does it work?
There are two playbooks you need to use to install the plugin:
1. site24x7_enable_mod_status.yml playbook as an example to update the configurations to enable the mod_status.
2. The site24x7_apache_plugin_playbook.yml playbook performs the some processes like downloading the plugin file, creating new directories, etc. that are required for the Site24x7 Apache plugin to collect performance metrics.

#### 1. Playbook: site24x7_enable_mod_status.yml

This playbook is an `Example` on how to enable mod_status using ansible playbooks. If required, please modify the playbook according to your server's configurations. The playbook works for RedHat and Debian distro.

- Checks if the given conf file `exists` in the given directory.
- Takes `backup` of the conf with time stamp.
- Adds the configuration given by the user after the regex or statement or EOF specified by the user.
- `Restarts` the Apache server. 

#### 2. Playbook: site24x7_apache_plugin_playbook.yml

The playbook performs the following processes that are required for the Site24x7 Apache plugin to collect performance metrics.

- Installs `python3` if not found.
- Installs `pip3` if not found.
- Checks the presence of the `Site24x7` monitoring agent.
- Creates directories `plugins/apache` under the `/opt/site24x7/monagent/temp` directory.
- Downloads the files [apache.py](https://raw.githubusercontent.com/site24x7/plugins/master/apache/apache.py) and [apache.cfg](https://raw.githubusercontent.com/site24x7/plugins/master/apache/apache.cfg) from the [plugins repository](https://github.com/site24x7/plugins/tree/master/apache)
   with read, write, and execute permission.
- Configures the `apache.cfg` file based on the values provided in the `vars` section of the playbook.
- Executes the `apache.py` file to check for a valid JSON output.
- Finally, it moves the `apache` directory along with the `apache.py` and `apache.cfg` files into the `/opt/site24x7/monagent/plugins` directory.

### Prerequisites 
To run the playbook, provide the Apache Server configuration details in the `vars` section of the playbook as shown below.

```yaml
   vars:
      apache_url: "http://localhost:80/server-status?auto"
      apache_username: "None"                           
      apache_password: "None"    
      apache_access_logs_enabled: "true"
      apache_access_logs_file_path: "/var/log/apache*/access.log*"
```

The details below are required to set the values in the [apache.cfg](https://github.com/site24x7/plugins/blob/master/apache/apache.cfg) file for the plugin.


**apache_url** : 

The URL with host IP and port number or domain name, and followed by the mod-status endpoint.
	
**apache_username** : 

The Apache Server username. If there is no username, set the value as `'"None"'`
	
**apache_password** : 

The Apache Server password. If there is no password, set the value as `'"None"'`

**apache_access_logs_enabled** : (True/False)

- `True` for enabling logs collection of the static "Apache Access Logs" log type
- `False` for disabling logs collection
	
**apache_access_logs_file_path** : 
This specifies the comma separated path(s) to the Apache access log files that the monitoring system will read and analyze. The * indicates it applies to all access logs in the specified directory.

---

### Run the playbook

Execute the command below to run the playbook:
```
ansible-playbook site24x7_apache_plugin_playbook.yml --user <username> -b

```

Once the playbook is executed, the Apache plugins will be deployed in the Ansible managed nodes. 

Once the deployment is complete, you can view performance data of the plugin monitors in the Site24x7 web client.
