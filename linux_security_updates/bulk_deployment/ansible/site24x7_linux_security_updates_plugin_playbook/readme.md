
# Site24x7 Linux Security Updates Plugin Playbook


### An Ansible playbook to install the Site24x7 Linux Security Updates plugin on all your Linux servers to monitor the number of pending security updates.

---

### How does it work?

The playbook performs the following processes that are required for the Site24x7 linux_security_updates plugin to collect performance metrics.

- Installs `python3` if not found.
- Installs `pip3` if not found.
- Installs `distro` Python package if not found.
- Checks the presence of the `Site24x7` monitoring agent.
- Creates directories `plugins/linux_security_updates` under the `/opt/site24x7/monagent/temp` directory.
- Downloads the files [linux_security_updates.py](https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_updates/linux_security_updates.py) from the [plugins repository](https://github.com/site24x7/plugins/tree/master/linux_security_updates)
   with read, write, and execute permission.
- Executes the `linux_security_updates.py` file to check for a valid JSON output.
- Finally, it moves the `linux_security_updates` directory along with the `linux_security_updates.py` files into the `/opt/site24x7/monagent/plugins` directory.


---

### Run the playbook

Execute the command below to run the playbook:
```
ansible-playbook site24x7_linux_security_updates_plugin_playbook.yml --user <username> -b

```

Once the playbook is executed, the linux_security_updates plugins will be deployed in the Ansible-managed nodes. 

Once the deployment is complete, you can view the performance data of the plugin monitors in the Site24x7 web client.
