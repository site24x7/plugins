# Plugin for Monitoring Port


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
