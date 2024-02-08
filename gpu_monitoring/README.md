# Plugin for Monitoring GPU Device

### Prerequisites

- Plugin Uses "gpustat" python module to get the gpu device performance metrics. Execute the following command in your server to install gpustat
	```
	pip install gpustat
	```
- Plugin Uses "gpustat -cp" command to get the individual core utilization

### Plugin Installation
---

- Create a directory named "gpu_monitoring".

- Download the file "[gpu_monitoring.py](https://github.com/site24x7/plugins/blob/master/gpu_monitoring/gpu_monitoring.py)" and place it under the "gpu_monitoring" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/gpu_monitoring/gpu_monitoring.py

  
- Execute the below command to check for valid json output

		python gpu_monitoring.py
  
  #### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the postgres.py script.
- Move the directory "gpu_monitoring" under the Site24x7 Linux Agent plugin directory: 

		/opt/site24x7/monagent/plugins/
  #### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.


- Move the folder "gpu_monitoring" under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
	
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Metrics Captured

- Memory Utilization
- CPU Utilization
- Temperature
- Individual Core Utilization
- Device Name
