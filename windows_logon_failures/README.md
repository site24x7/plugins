# Windows Login Failure Monitoring

                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


---


### Plugin Installation  

- Create a directory named "windows_logon_failure" under the Site24x7 Windows Agent plugin directory: 

		Windows             ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
      
- Download all the files in the "windows_logon_failure" folder and place it under the "windows_logon_failure" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/windows_logon_failure/windows_logon_failure.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/windows_logon_failure/windows_logon_failure.cfg



- Execute the below command with appropriate arguments to check for the valid json output:

 ```
.\windows_logon_failure.ps1 -threshold "count"
 ```
Since it's a windows plugin, to run in windows server please follow the steps in below link, remaining configuration steps are exactly the same. 

  https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers



---

### Configurations

- Provide your threshold configurations in windows_logon_failure.cfg file.
```
    [login_filures]
    threshold=<Threshold Count>
```	
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics

The metrics that are captured by the plugin are as follows:
 
 - #### failed_login_count
   The number of failed logins in the windows server
 

