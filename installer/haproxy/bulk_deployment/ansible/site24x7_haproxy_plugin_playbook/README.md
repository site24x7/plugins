
# Site24x7 HAProxy Plugin Playbook


### Use this playbook to install the Site24x7 HAProxy plugin in multiple HAProxy nodes.

---

### How does it work?

The playbook performs the following processes that are required for the Site24x7 HAProxy plugin to collect performance metrics.

- Installs `python3` if not found.
- Installs `pip3` if not found.
- Installs `requests` Python package if not found.
- Installs `pandas` Python package if not found.
- Checks the presence of the `Site24x7` monitoring agent.
- Creates directories `plugins/haproxy` under the `/opt/site24x7/monagent/temp` directory.
- Downloads the files [haproxy.py](https://raw.githubusercontent.com/site24x7/plugins/master/haproxy/haproxy.py) and [haproxy.cfg](https://raw.githubusercontent.com/site24x7/plugins/master/haproxy/haproxy.cfg) from the [plugins repository](https://github.com/site24x7/plugins/tree/master/haproxy)
   with read, write, and execute permission.
- Configures the `haproxy.cfg` file based on the values provided in the `vars` section of the playbook.
- Executes the `haproxy.py` file to check for a valid JSON output.
- Finally, it moves the `haproxy` directory along with the `haproxy.py` and `haproxy.cfg` files into the `/opt/site24x7/monagent/plugins` directory.

### Prerequisites 

- The plugin requires the stats page to be enabled in the HAProxy to fetch the metrics, to enable the stats module in bulk, the `site24x7_haproxy_config_enable_stats.yaml` can be optionally used to enable the stats module in the haproxy config file located at `/etc/haproxy/haproxy.cfg`. In order to run the playbook execute the below command.
```
ansible-playbook haproxy_config.yml -b
```

by running the playbook the below code block will be pasted in the `/etc/haproxy/haproxy.cfg` file.

```cfg
Site24x7 - Enable HAProxy stats
frontend stats
  mode http
  timeout client 10s
  bind *:8404
  stats enable
  stats uri /stats
  stats refresh 10s
Site24x7 - Enable HAProxy stats

```




- To run the playbook, provide the HAProxy configuration details in the `vars` section of the playbook as shown below.

```yaml
   vars:
      HAProxy_hostname: "localhost"
      HAProxy_port: "8404"
      HAProxy_username: "test_user"                             # HAProxy username    [Enter '"None"' in case of no username]
      HAProxy_password: "test_password"                         # HAProxy password    [Enter '"None"' in case of no password]
      HAProxy_logs_enabled: "False"
      HAProxy_log_type_name: "None"
      HAProxy_log_file_path: "None"
```
The details below are required to set the values in the [haproxy.cfg](https://github.com/site24x7/plugins/blob/master/haproxy/haproxy.cfg) file for the plugin.

- **HAProxy_hostname** :

    The host on which the HAProxy instance is running.

- **HAProxy_port**

    The port on which the HAProxy instance is running.

- **HAProxy_username**

    The HAProxy username. If there is no username, set the value as `'"None"'`

- **HAProxy_password** :

    The HAProxy password. If there is no password, set the value as `'"None"'`

- **HAProxy_logs_enabled** :

    HAProxy logs enabled (True/False)

- **HAProxy_log_type_name** :

    Name of HAProxy log type

- **HAProxy_log_file_path**:

    Path of HAProxy log file



---

### Run the playbook

Execute the command below to run the playbook:
```
ansible-playbook site24x7_haproxy_plugin_playbook.yml --user <username> -b

```

Once the playbook is executed, the HAProxy plugins will be deployed in the Ansible-managed nodes. 

Once the deployment is complete, you can view the performance data of the plugin monitors in the SIte24x7 web client.
