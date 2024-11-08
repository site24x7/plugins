# Linux disk Mount Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `linux_disk_mount`.
  
```bash
mkdir linux_disk_mount
cd linux_disk_mount/
```
      
- Download below files and place it under the "linux_disk_mount" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/linux_disk_mount/linux_disk_mount.py && sed -i "1s|^.*|#! $(which python3)|" linux_disk_mount.py
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 linux_disk_mount.py
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "linux_disk_mount" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv linux_disk_mount /opt/site24x7/monagent/plugins/
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Linux Disk Mount Server Monitoring Plugin Metrics

| Metric Name                        | Description                                                  |
|-------------------------------------|--------------------------------------------------------------|
| `File_System`                       | List of file systems with detailed metrics.                  |
| `File_System.name`                  | The name of the file system (e.g., `/dev/nvme0n1p3_crypt-/`).|
| `File_System.Free_Size`             | The free disk space in GB for the file system.               |
| `File_System.Used_Size`             | The used disk space in GB for the file system.               |
| `File_System.Total_Size`            | The total disk space in GB for the file system.              |
| `File_System.Used_Utilization`      | The percentage of used disk space in the file system.        |
| `File_System.Free_Utilization`      | The percentage of free disk space in the file system.        |
| `File_System.status`                | The status of the file system (1 if the file system is valid, 0 if not). |
| `Total_No_Of_Disk_Partitions`       | The total number of disk partitions tracked.                 |
| `Total_Disk_Capacity`               | The total disk capacity in GB across all tracked file systems. |
| `Total_Used_Disk`                   | The total used disk space in GB across all tracked file systems. |
| `Total_Free_Disk`                   | The total free disk space in GB across all tracked file systems. |
