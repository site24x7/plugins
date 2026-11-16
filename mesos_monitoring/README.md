# Mesos Monitoring

Install and configure the Mesos plugin to monitor the performance, availability, and health of your Apache Mesos cluster. Track master status, agent connectivity, task states, resource utilization, message flow, and operations to ensure optimal performance of your Mesos environment.

---

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python version 3 or higher.
- Apache Mesos master running with the HTTP API accessible (default port `5050`).

> **Note:** If HTTP authentication is enabled on the Mesos master (using `--authenticate_http_readonly` flag), you will need valid credentials. If authentication is not enabled (default), set `username` and `password` to `"None"`.

---

## Installation

### Plugin Installation

- Create a directory named `mesos_monitoring`:

```bash
mkdir mesos_monitoring
cd mesos_monitoring/
```

- Download all the files [mesos_monitoring.cfg](https://github.com/site24x7/plugins/blob/master/mesos_monitoring/mesos_monitoring.cfg), [mesos_monitoring.py](https://github.com/site24x7/plugins/blob/master/mesos_monitoring/mesos_monitoring.py) and place them under the `mesos_monitoring` directory:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/mesos_monitoring/mesos_monitoring.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/mesos_monitoring/mesos_monitoring.cfg
```

- Execute the below command with appropriate arguments to check for valid JSON output:

```bash
python3 mesos_monitoring.py --hostname "localhost" --port "5050" --protocol "http" --username "None" --password "None"
```

For HTTPS-enabled connections:

```bash
python3 mesos_monitoring.py --hostname "localhost" --port "5050" --protocol "https" --verify_ssl "true" --username "admin" --password "password"
```

### Configurations

Provide your Mesos master configurations in the `mesos_monitoring.cfg` file.

#### For Linux

```bash
[global_configurations]
use_agent_python=1

[mesos_monitoring]
hostname = "localhost"
port = "5050"
protocol = "http"
username = "None"
password = "None"
verify_ssl = "true"
```

#### For Windows

```bash
[mesos_monitoring]
hostname = "localhost"
port = "5050"
protocol = "http"
username = "None"
password = "None"
verify_ssl = "true"
```

> **Note:** Set `username` and `password` to `"None"` if authentication is not enabled on the Mesos master. Set `verify_ssl` to `"false"` to skip SSL certificate verification for self-signed certificates.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the mesos_monitoring.py script.

- Move the `mesos_monitoring` directory under the Site24x7 Linux Agent plugin directory:

```bash
mv mesos_monitoring /opt/site24x7/monagent/plugins/
```

#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Move the folder `mesos_monitoring` under Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---

## Metrics Captured

### Summary

| Metric Name                       | Description                                                                                              |
|-----------------------------------|----------------------------------------------------------------------------------------------------------|
| Master Elected                    | Whether this Mesos master node is the elected cluster leader (1 = elected, 0 = standby).                 |
| Dropped Messages                  | Number of messages dropped by the Mesos master due to processing failures or queue overflow.             |
| Active Frameworks                 | Number of Mesos frameworks (e.g., Marathon, Chronos) actively registered with the Mesos master.          |
| Active Agents                     | Number of Mesos agent nodes currently active and available to run tasks in the cluster.                   |
| Connected Agents                  | Number of Mesos agent nodes currently connected to the Mesos master.                                     |
| Running Tasks                     | Number of Mesos tasks currently in running state across all Mesos agents.                                |
| CPU Usage                         | Percentage of total CPUs allocated by the Mesos master that are currently in use by running tasks.       |
| Memory Usage                      | Percentage of total memory allocated by the Mesos master that is currently in use by running tasks.      |
| Disk Usage                        | Percentage of total disk allocated by the Mesos master that is currently in use by running tasks.        |
| Uptime                            | Time in seconds since the Mesos master process started.                                                  |

### Agents

| Metric Name                       | Description                                                                                              |
|-----------------------------------|----------------------------------------------------------------------------------------------------------|
| Agent Registrations               | Number of times Mesos agent nodes have registered with the Mesos master.                                 |
| Agent Re-registrations            | Number of times Mesos agent nodes have re-registered with the Mesos master after a connection loss.      |
| Agent Removals                    | Number of Mesos agent nodes that have been removed from the cluster by the Mesos master.                 |
| Agent Shutdowns Scheduled         | Number of Mesos agent node shutdowns that have been scheduled by the Mesos master.                       |
| Agent Shutdowns Canceled          | Number of scheduled Mesos agent node shutdowns that were canceled before execution.                      |
| Agent Shutdowns Completed         | Number of Mesos agent node shutdowns that have been successfully completed.                              |
| Disconnected Agents               | Number of Mesos agent nodes currently disconnected from the Mesos master.                                |
| Inactive Agents                   | Number of Mesos agent nodes marked as inactive by the Mesos master.                                      |

### Tasks

| Metric Name                       | Description                                                                                              |
|-----------------------------------|----------------------------------------------------------------------------------------------------------|
| Tasks Dropped                     | Number of Mesos tasks dropped by the Mesos master before being launched on a Mesos agent.                |
| Tasks Error                       | Number of Mesos tasks that terminated with an error on Mesos agents.                                     |
| Tasks Failed                      | Number of Mesos tasks that have failed during execution on Mesos agents.                                 |
| Tasks Finished                    | Number of Mesos tasks that have completed successfully on Mesos agents.                                  |
| Tasks Gone                        | Number of Mesos tasks reported as gone when a Mesos agent is removed from the cluster.                   |
| Tasks Gone By Operator            | Number of Mesos tasks manually marked as gone by the cluster operator.                                   |
| Tasks Killed                      | Number of Mesos tasks that were explicitly killed by a framework or the Mesos master.                    |
| Tasks Killing                     | Number of Mesos tasks currently in the process of being killed on Mesos agents.                          |
| Tasks Lost                        | Number of Mesos tasks lost due to Mesos agent failures or network partitions.                            |
| Tasks Staging                     | Number of Mesos tasks currently in staging state, waiting to be launched on a Mesos agent.               |
| Tasks Starting                    | Number of Mesos tasks currently starting up on Mesos agents.                                             |
| Tasks Unreachable                 | Number of Mesos tasks on Mesos agents that are unreachable from the Mesos master.                        |

### Resources

| Metric Name                       | Description                                                                                              |
|-----------------------------------|----------------------------------------------------------------------------------------------------------|
| CPUs Used                         | Number of CPUs currently allocated to running Mesos tasks across all Mesos agents.                       |
| Disk Total                        | Total disk space (MB) available across all Mesos agent nodes in the cluster.                             |
| Disk Used                         | Disk space (MB) currently allocated to running Mesos tasks across all Mesos agents.                      |
| GPU Usage                         | Percentage of total GPUs allocated by the Mesos master that are currently in use by running tasks.       |
| GPUs Total                        | Total number of GPUs available across all Mesos agent nodes in the cluster.                              |
| GPUs Used                         | Number of GPUs currently allocated to running Mesos tasks across all Mesos agents.                       |
| Memory Total                      | Total memory (MB) available across all Mesos agent nodes in the cluster.                                 |
| Memory Used                       | Memory (MB) currently allocated to running Mesos tasks across all Mesos agents.                          |

### System

| Metric Name                       | Description                                                                                              |
|-----------------------------------|----------------------------------------------------------------------------------------------------------|
| Valid Status Updates              | Number of valid task status updates received by the Mesos master from Mesos agents.                      |
| Invalid Status Updates            | Number of invalid task status updates received by the Mesos master from Mesos agents.                    |
| Registrar Queued Operations       | Number of operations queued in the Mesos master registrar waiting to be persisted.                       |
| Registry Size                     | Size of the Mesos master registrar registry in bytes, which stores cluster state information.            |
| State Fetch Time                  | Time taken to fetch the Mesos master registrar state in milliseconds.                                    |
| State Store Time                  | Time taken to store the Mesos master registrar state in milliseconds.                                    |

### Messages

| Metric Name                            | Description                                                                                         |
|----------------------------------------|-----------------------------------------------------------------------------------------------------|
| Messages Authenticate                  | Number of authentication messages received by the Mesos master from frameworks and agents.          |
| Messages Deactivate Framework          | Number of messages to deactivate a Mesos framework received by the Mesos master.                    |
| Messages Decline Offers               | Number of resource offer decline messages sent by Mesos frameworks to the Mesos master.             |
| Messages Executor To Framework         | Number of messages forwarded by the Mesos master from Mesos executors to Mesos frameworks.          |
| Messages Exited Executor               | Number of Mesos executor exit notifications received by the Mesos master from Mesos agents.         |
| Messages Framework To Executor         | Number of messages forwarded by the Mesos master from Mesos frameworks to Mesos executors.          |
| Messages Kill Task                     | Number of task kill request messages sent by Mesos frameworks to the Mesos master.                  |
| Messages Launch Tasks                  | Number of task launch messages sent by Mesos frameworks to the Mesos master.                        |
| Messages Reconcile Operations          | Number of operation reconciliation messages sent by Mesos frameworks to the Mesos master.           |
| Messages Reconcile Tasks               | Number of task reconciliation messages sent by Mesos frameworks to the Mesos master.                |
| Messages Register Framework            | Number of Mesos framework registration messages received by the Mesos master.                       |
| Messages Register Agent                | Number of Mesos agent registration messages received by the Mesos master.                           |
| Messages Re-register Framework         | Number of Mesos framework re-registration messages received by the Mesos master after reconnection. |
| Messages Re-register Agent             | Number of Mesos agent re-registration messages received by the Mesos master after reconnection.     |
| Messages Resource Request              | Number of resource request messages sent by Mesos frameworks to the Mesos master.                   |
| Messages Revive Offers                 | Number of offer revival messages sent by Mesos frameworks to resume receiving resource offers.       |
| Messages Status Update                 | Number of task status update messages received by the Mesos master from Mesos agents.               |
| Messages Suppress Offers              | Number of offer suppression messages sent by Mesos frameworks to stop receiving resource offers.     |
| Messages Unregister Framework          | Number of Mesos framework unregistration messages received by the Mesos master.                     |
| Messages Unregister Agent              | Number of Mesos agent unregistration messages received by the Mesos master.                         |
| Messages Update Agent                  | Number of Mesos agent attribute or resource update messages received by the Mesos master.           |
| Messages Status Update Ack            | Number of task status update acknowledgement messages sent by Mesos frameworks to the Mesos master. |
| Messages Operation Status Update Ack  | Number of operation status update acknowledgements sent by Mesos frameworks to the Mesos master.    |
