
# Site24x7 Check Updates Plugin Playbook


### A playbook to install Site24x7 CheckUpdates plugins on all your Linux Servers and monitor the number of pending security updates. 

---

### How does it work?

The playbook performs the following processes that are required for the Site24x7 check_updates plugin to collect performance metrics.

- Installs `python3` if not found.
- Installs `pip3` if not found.
- Installs `distro` Python package if not found.
- Checks the presence of the `Site24x7` monitoring agent.
- Creates directories `plugins/check_updates` under the `/opt/site24x7/monagent/temp` directory.
- Downloads the files [check_updates.py](https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/check_updates.py) from the [plugins repository](https://github.com/site24x7/plugins/tree/master/check_updates)
   with read, write, and execute permission.
- Executes the `check_updates.py` file to check for a valid JSON output.
- Finally, it moves the `check_updates` directory along with the `check_updates.py` files into the `/opt/site24x7/monagent/plugins` directory.


---

### Run the playbook

Execute the command below to run the playbook:
```
ansible-playbook site24x7_check_updates_plugin_playbook.yml --user <username> -b

```

Once the playbook is executed, the check_updates plugins will be deployed in the Ansible-managed nodes. 

Once the deployment is complete, you can view the performance data of the plugin monitors in the Site24x7 web client.
