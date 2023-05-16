Plugin for monitoring the KVM host
==================================

Kernel-based Virtual Machine (KVM) is an open source technology that lets you to act your linux as a hypervisor. This plugin is used to monitor the kvm host server to get the details like CPU, memory and other details.  

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "libvirt" python library. This module is used for managing virtualization platforms

- How to install libvirt :

		apt-get install libvirt-bin libvirt-doc
		
For more details on the libvirt library , refer https://libvirt.org/index.html. 


### Plugin installation
---
##### Linux 

- Create a directory "kvm_host".

- Download all the files in "kvm_host" folder and place it under the "kvm_host" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/kvm_host/kvm_host.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/kvm_host/kvm_host.cfg
			  	
- Configure the keys to be monitored, as mentioned in the below configuration, in "kvm_host.cfg"

		[localhost]
		host="qemu:///system"
		plugin_version="1"
		heartbeat="True"
		
host - KVM host to be monitored.Incase of remote host ssh login details has to be provides.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python kvm_host.py --host "qemu:///system" --plugin-version "1" --heartbeat "True"
		
- Move the directory "kvm_host" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---
		active_cpus - Active cpus available 
		buffers_memory - Buffer memory size 
		cached_memory -  Cached memory size
		conn_encrypted -  Is this connection encrypted 
		conn_secure -  Is this connection secure
		cores_per_socket -  Number of cores per socket
		cpu_freq_in_hz -  Frequency of cpu in Hz
		cpu_model -  Cpu model 
		free_memory -  Size of free memory
		host -  name of the KVM host
		idle_time -  CPU Idle time 
		iowait_time -  IO Wait time
		kernel -  Kernel time
		libvirt_version -  libvirt library version number 
		mem_in_mb -  Size of memory in MB
		networks_count -  Number of network devices 
		numa_node_count -  Number of NUMA nodes
		sockets_per_node -  Number of sockets per Node 
		storage_pool_count - Number of storage pools in the host
		threads_per_core -  Number of threads allocated per core
		total_memory -  Size of total memory
		uri -  Current login uri 
		user_time -  User Time 
		version -  KVM version
		virtualization_type - Type of virtualization 
		vms_count - Number of vms in the host
			
