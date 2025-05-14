# Plugin for Monitoring Windows Port


## Plugin Installation

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Plugin Installation 

#### Windows
  
- Create a folder named `WindowsPortCheck`.

- Download the files [WindowsPortCheck.cfg](https://github.com/site24x7/plugins/blob/master/WindowsPortCheck/WindowsPortCheck.cfg), [WindowsPortCheck.ps1](https://github.com/site24x7/plugins/blob/master/WindowsPortCheck/WindowsPortCheck.ps1) and place it under the `WindowsPortCheck` folder.


- Move the folder `WindowsPortCheck` under Site24x7 Windows Agent plugin folder:

```console
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
```
    
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics

| Metric Name           | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Total Processes       | The number of unique processes currently listening on the specified port.   |
| Total CPU Usage       | The total CPU usage percentage of all processes using the specified port.   |
| Total Memory Usage    | The total memory consumed (in MB) by all processes using the port.          |
| Port Status Text      | Indicates whether the specified port is currently open or closed.           |


## Sample Images

![image](https://github.com/user-attachments/assets/0a4e1ede-5afc-4a7c-b6f9-d32a5ad0bfa3)
