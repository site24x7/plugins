
# Site24x7 Redis Plugin Playbook


### Use this playbook to install the Site24x7 Redis plugin in multiple Redis nodes.

---

### How does it work?

The playbook performs the following processes that are required for the Site24x7 Redis plugin to collect performance metrics.

- Installs `python3` if not found.
- Installs `pip3` if not found.
- Installs `Redis` Python package if not found.
- Checks the presence of the `Site24x7` monitoring agent.
- Creates directories `plugins/Redis` under the `/opt/site24x7/monagent/temp` directory.
- Downloads the files [Redis.py](https://raw.githubusercontent.com/site24x7/plugins/master/redis/Redis.py) and [Redis.cfg](https://raw.githubusercontent.com/site24x7/plugins/master/redis/Redis.cfg) from the [plugins repository](https://github.com/site24x7/plugins/tree/master/Redis)
   with read, write, and execute permission.
- Configures the `Redis.cfg` file based on the values provided in the `vars` section of the playbook.
- Executes the `Redis.py` file to check for a valid JSON output.
- Finally, it moves the `Redis` directory along with the `Redis.py` and `Redis.cfg` files into the `/opt/site24x7/monagent/plugins` directory.

### Prerequisites 
To run the playbook, provide the Redis configuration details in the `vars` section of the playbook as shown below.

```yaml
   vars:
      Redis_host: <Redis_host>
      Redis_port: <Redis_port>
      Redis_password: <Redis_password>
      Redis_dbs: <Redis_dbs>
```

The details below are required to set the values in the [Redis.cfg](https://github.com/site24x7/plugins/blob/master/redis/Redis.cfg) file for the plugin.

- **Redis_host:** 

    The host on which the Redis server is running

- **Redis_port:** 

    The port on which the Redis server is running

- **Redis_password:** 

    Password of Redis Server

- **Redis_dbs:** 
    
    Name of Redis Database


---

### Run the playbook

Execute the command below to run the playbook:
```
ansible-playbook site24x7_Redis_plugin_playbook.yml --user <username> -b

```

Once the playbook is executed, the Redis plugins will be deployed in the Ansible managed nodes. 

Once the deployment is complete, you can view performance data of the plugin monitors in the SIte24x7 web client.
