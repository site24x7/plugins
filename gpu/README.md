# Plugin for Monitoring GPU Device

### Plugin Installation
---

  
#### Linux

- Create a directory named `gpu`.

		mkdir gpu
  		cd gpu/

- Download the file [gpu.py](https://github.com/site24x7/plugins/blob/master/gpu/gpu.py) and [gpu.cfg](https://github.com/site24x7/plugins/blob/master/gpu/gpu.cfg) place it under the `gpu` directory.
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/gpu/gpu.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/gpu/gpu.cfg

- Execute the below command in terminal to check for valid json output.

		python gpu.py
  
- Move the directory `gpu` under the Site24x7 Linux Agent plugin directory: 

		mv gpu /opt/site24x7/monagent/plugins/


#### Windows
  
- Create a directory named `gpu`.

- Download the file [gpu.py](https://github.com/site24x7/plugins/blob/master/gpu/gpu.py) and place it under the `gpu` directory

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.
 
- Execute the below command in command prompt to check for valid json output.

		python gpu.py

- Move the folder `gpu` under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
	
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Metrics Captured

Name		        | Description
---         		|   ---
Average Memory   	| 	Average Percentage of memory utilization across multiple GPUs.
GPU Utilization   	| 	The percentage of the GPU's memory that is currently being used by processes or applications.
Temperature  		| 	The current operating temperature of the GPU, typically measured in degrees Celsius (°C).
Memory   		| 	The amount of memory currently being consumed by the GPU.
Total Memory   		| 	The total amount of memory available on the GPU.
GPU   			| 	The model name of the GPU.
Power Draw		|	The actual current power consumption of the GPU in watts.
Power Limit		|	The maximum allowed power consumption set for the GPU, typically in watts.
Driver Version		|	The version number of the installed NVIDIA graphics driver software.
CUDA Version		|	The version number of the CUDA toolkit installed on the system, which enables GPU-accelerated computing.
