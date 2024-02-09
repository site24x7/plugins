# Plugin for Monitoring GPU Device

### Prerequisites

- Python version 3 or higher.

- Plugin Uses "gpustat" python module to get the gpu device performance metrics. Execute the following command in your server to install gpustat
	```
	pip install gpustat
	```

### Plugin Installation
---

  
#### Linux

- Create a directory named "gpu_monitoring".

		mkdir gpu_monitoring
  		cd gpu_monitoring/

- Download the file "[gpu_monitoring.py](https://github.com/site24x7/plugins/blob/master/gpu_monitoring/gpu_monitoring.py)" and place it under the "gpu_monitoring" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/gpu_monitoring/gpu_monitoring.py


- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the gpu_monitoring.py script.

- Execute the below command to check for valid json output

		python gpu_monitoring.py
  
- Move the directory "gpu_monitoring" under the Site24x7 Linux Agent plugin directory: 

		mv gpu_monitoring /opt/site24x7/monagent/plugins/


#### Windows
  
- Create a directory named "gpu_monitoring".

- Download the file "[gpu_monitoring.py](https://github.com/site24x7/plugins/blob/master/gpu_monitoring/gpu_monitoring.py)" and place it under the "gpu_monitoring" directory

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Execute the below command to check for valid json output

		python gpu_monitoring.py

- Move the folder "gpu_monitoring" under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
	
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Metrics Captured
Name		            	| Description
---         		   	|   ---
GPU Utilization   | The percentage of the GPU's memory that is currently being used by processes or applications.
Temperature  | The current operating temperature of the GPU, typically measured in degrees Celsius (°C).
Memory   | The amount of memory currently being consumed by the GPU.
Total Memory   | The total amount of memory available on the GPU.
GPU   | The model name of the GPU
