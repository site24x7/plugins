# NTFS Monitoring

                    
## Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


---

### Plugin Installation  

- Create a directory named "ntfs_monitoring".
      
- Download all the files and place it under the "ntfs_monitoring" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/ntfs_monitoring/ntfs_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/ntfs_monitoring/ntfs_monitoring.cfg



- Execute the below command with appropriate arguments to check for the valid json output:

	 ```
	.\ntfs_monitoring.ps1 -mountpointpath "C:\,D:\,E:\"
	 ```
 
- After above command with parameters gives expected output, please configure the relevant  parameters in the ntfs_monitoring.cfg file..
```
    [NTFS]
    mountpointpath=<mount point paths>
```
- Move the folder into the  Site24x7 Windows Agent plugin directory: 

		Windows             ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
		
    
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

--- 

## Supported Metrics

The metrics that are captured by the NTFS plugin are as follows:
 
 - #### Usage
   Used percentage  of  memory of the specified mountpoint.
   
 - #### Free
   Free percentage of memory of the specified mountpoint.
   
   
   
   
