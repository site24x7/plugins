# Plugin for Monitoring GPU Device

### PreRequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Make sure that python is present in the server where you have installed the plugin by following the steps in the below help article.

   https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers


- Plugin Uses "GPUtil" python module to get the gpu device performance metrics	
	
  Execute the following command in your server to install gputil 
  
		pip install gputil
      
### Plugin installation
---
##### Windows 

- Create a folder named "windows_gpu_monitoring" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\windows_gpu_monitoring
		
- Download the file "windows_gpu_monitoring.py" and place it under the "windows_gpu_monitoring" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/windows_gpu_monitoring/windows_gpu_monitoring.py
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.
  
### Metrics Captured

- memory_utilzation
- used_memory
- temperature

