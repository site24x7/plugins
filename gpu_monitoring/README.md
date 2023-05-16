# Plugin for Monitoring GPU Device

### PreRequisites

- Plugin Uses "gpustat" python module to get the gpu device performance metrics	
	
      Execute the following command in your server to install gpustat - pip install gpustat

- Plugin Uses "gpustat -cp" command to get the individual core utilization

### Plugin installation
---
##### Linux 

- Create a directory "gpu_monitoring".

- Download the file "gpu_monitoring.py" and place it under the "gpu_monitoring" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/gpu_monitoring/gpu_monitoring.py
		
- Execute the below command to check for valid json output

		pyhton gpu_monitoring.py
  
- Move the directory "gpu_monitoring" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/gpu_monitoring
	
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Metrics Captured

- Memory Utilization
- CPU Utilization
- Temperature
- Individual Core Utilization
- Device Name
