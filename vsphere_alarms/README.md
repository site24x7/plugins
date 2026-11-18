# Plugin for Monitoring vSphere Alarms

### Plugin Installation
---


#### Windows

- Create a folder named `vsphere_alarms`.

- Download the files [vsphere_alarms.ps1](https://github.com/site24x7/plugins/blob/master/vsphere_alarms/vsphere_alarms.ps1) and [vsphere_alarms.cfg](https://github.com/site24x7/plugins/blob/master/vsphere_alarms/vsphere_alarms.cfg) and place them under the `vsphere_alarms` folder.

- In the `vsphere_alarms.cfg` file, provide the vSphere server IP address or domain name, along with the required credentials.

- Install the VMware PowerCLI module in PowerShell as an administrator:

		Install-Module -Name VMware.PowerCLI -Scope AllUsers

> [!NOTE]
> The plugin only works if the VMware PowerCLI module is installed for all users or for the user account under which the Site24x7 agent service runs.
- Execute the below command in PowerShell to check for valid output:

		powershell .\vsphere_alarms.ps1 -v -Server 10.10.10.10 -username test@example.local -password example

- Move the folder `vsphere_alarms` under the Site24x7 Windows Agent plugin folder:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configure AppLogs in the Site24x7 web client
---

1. After a successful plugin execution, an `alarms*.txt` file should be created in the plugins folder.
2. If alarms are present, the file will contain the alarm logs. Copy the first line from the log file and open Site24x7.
3. Go to **AppLogs** and create a new log type. Paste the sample log line and use the following log pattern:

		$Datetime:date:yyyy-MM-dd-HH-mm-ss$, Entity: $Entity$, State: $State$, Alarm: $Alarm$, vCenter: $vCenter$, EntityType: $EntityType$

4. Create a log profile and select the server where the plugin is installed.
5. In the log profile, provide the log file path. Example:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\plugins\vsphere_alarms\alarms*

### Log Fields Captured

Name		| Description
---		|   ---
Datetime	|	The timestamp when the alarm was captured.
Entity		|	The name of the vSphere entity (e.g., VM, host, datastore) that triggered the alarm.
State		|	The current state of the alarm (e.g., red, yellow, green).
Alarm		|	The name or description of the triggered alarm.
vCenter		|	The vCenter server from which the alarm was reported.
EntityType	|	The type of the vSphere entity that triggered the alarm (e.g., VirtualMachine, HostSystem).
