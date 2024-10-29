# Plugin Bulk Installation Using Ansible

This Ansible playbook helps in deploying multiple plugins from a controller node to target hosts, ideal for installing the same plugin across multiple servers in bulk.

## Introduction to Ansible
Ansible is an open-source automation tool that simplifies the process of managing, configuring, and deploying applications across multiple hosts. It uses YAML-based playbooks to execute tasks and is particularly useful for system administrators and DevOps teams.

## Prerequisites

Before executing this playbook, ensure the following prerequisites are met:

1. **Site24x7 Agent**: The Site24x7 Linux monitoring agent must be installed and actively running on all target hosts.
2. **Ansible Configuration**: 
   - Ansible should be correctly installed and configured on the controller node.
   - All target hosts must be accessible via SSH from the controller node.
3. **Plugin Availability**:
   - Ensure the plugin folder is available on the controller node.

## Execution Steps

1. **Download the Ansible Playbook**:
   Use the following command to download the Ansible playbook:
   ```bash
   wget https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/pluginbulkinstallation/pluginbulkinstallation.yaml
   ```

2. **Define the Target Hosts**:
   Open the playbook file and ensure the `hosts` group matches the intended target group. By default, it is set to `all`.

3. **Run the Ansible Playbook**:
   Execute the playbook using the following command, specifying the path to the plugin folder:
   ```bash
   ansible-playbook pluginbulkinstallation.yaml
   ```

4. **Execute the Plugin**:
   Run the following command to execute the playbook, and specify the plugin folder path (e.g., `/root/user/custom_plugin`) where the plugin files are located:
   ```bash
   ansible-playbook pluginbulkinstallation.yaml -e "plugin_folder_path=/root/user/custom_plugin"
   ```

