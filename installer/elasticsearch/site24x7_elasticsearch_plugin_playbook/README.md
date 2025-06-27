
# Site24x7 Elasticsearch Plugin Playbook


### Use this playbook to install the Site24x7 Elasticsearch plugin in multiple Elasticsearch nodes.

---

### How does it work?

The playbook performs the following processes that are required for the Site24x7 Elasticsearch plugin to collect performance metrics.

- Installs `python3` if not found.
- Installs `pip3` if not found.
- Installs `requests` Python package if not found.
- Checks the presence of the `Site24x7` monitoring agent.
- Creates directories `plugins/elasticsearch` under the `/opt/site24x7/monagent/temp` directory.
- Downloads the files [elasticsearch.py](https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/elasticsearch.py) and [elasticsearch.cfg](https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/elasticsearch.cfg) from the [plugins repository](https://github.com/site24x7/plugins/tree/master/elasticsearch)
   with read, write, and execute permission.
- Configures the `elasticsearch.cfg` file based on the values provided in the `vars` section of the playbook.
- Executes the `elasticsearch.py` file to check for a valid JSON output.
- Finally, it moves the `elasticsearch` directory along with the `elasticsearch.py` and `elasticsearch.cfg` files into the `/opt/site24x7/monagent/plugins` directory.

### Prerequisites 
To run the playbook, provide the Elasticsearch configuration details in the `vars` section of the playbook as shown below.

```yaml
   vars:
      elasticsearch_host: <elasticsearch_host>
      elasticsearch_port: <elasticsearch_port>
      elasticsearch_node_name: <elasticsearch_node_name>
      elasticsearch_username: <elasticsearch_username>
      elasticsearch_password: <elasticsearch_password>
      elasticsearch_ssl_option: <elasticsearch_ssl_option>
      elasticsearch_cafile: <elasticsearch_cafile>
```

The details below are required to set the values in the [elasticsearch.cfg](https://github.com/site24x7/plugins/blob/master/elasticsearch/elasticsearch.cfg) file for the plugin.

- **elasticsearch_host**

    Name of the Elasticsearch host

- **elasticsearch_port**

    The Elasticsearch port number

- **elasticsearch_node_name**

    The name of the Elasticsearch node

- **elasticsearch_username**

    The username set for the Elasticsearch instance

- **elasticsearch_password**

    The password set for the Elasticsearch user.

- **elasticsearch_ssl_option**

    Elasticsearch SSL option (True/False)

- **elasticsearch_cafile**

    Elasticsearch cafile path


---

### Run the playbook

Execute the command below to run the playbook:
```
ansible-playbook site24x7_elasticsearch_plugin_playbook.yml --user <username> -b

```

Once the playbook is executed, the elasticsearch plugins will be deployed in the Ansible managed nodes. 

Once the deployment is complete, you can view performance data of the plugin monitors in the SIte24x7 web client.
