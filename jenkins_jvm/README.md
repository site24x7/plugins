                                
# JENKINS PLUGIN
                                                                                               

### What is Jenkins?
	
 Jenkins is an open source automation server written in Java. It helps to execute a series of actions to achieve a continuous integration process. 



### How it's used for Developers?

 Jenkins enables developers around the world to reliably build, test, package, stage and deploy their software.

 With Jenkins, multiple developers from different modules can integrate the code change in a single project. 

### How does it accelerate the development and test process 

 With Jenkins, DevOps can accelerate the software development and testing process thru automation. Once the code is committed by the developer, next the code will be built and tested.

 If the test is passed, then the build will be tested for deployment. After deployment is successful, it's pushed to production.



### Importance of monitoring Jenkins JVM:

To run the Jenkins effectively, DevOps team is required to monitor the significant metrics of Jenkins. The continuous monitoring Jenkins will allow DevOps team to view below features.

- Total number of bytes used by heap memory, non-heap memory , total memory.
- Total threads.
- Running thread , terminated threads.

---

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Follow below steps to generate API key 
	- Install the "Metrics plugin" from Jenkins. (Jenkins -> Manage Jenkins -> Manage plugins ->Available)
	- (Jenkins -> Manage Jenkins -> Configure system) Generate your API key under the metrics section.
 - Python version 3 or higher.

---

## Plugin Installation  

- Create a directory "jenkins_jvm".
  
  		mkdir jenkins_jvm
  		cd jenkins_jvm/
  
- Download all the files in "jenkins_jvm" folder and place it under the "jenkins_jvm" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_jvm/jenkins_jvm.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_jvm/jenkins_jvm.cfg


- Execute the below command with appropriate arguments to check for the valid json output.  

		python jenkins_jvm.py --host "host" --port "port" --username "username" --password "password" --apikey "apikey"
		
- Change the below configurations in "jenkins_jvm.cfg" file

		[jenkins_jvm]
		host = "host"
		port = "port"
		username = "username"
		password = "password"
		apikey = "apikey"

##### Linux 

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the jenkins_jvm.py script.

- Move the directory "jenkins_jvm" under Site24x7 Linux Agent plugin directory : 

		mv jenkins_jvm /opt/site24x7/monagent/plugins/
  
##### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.


- Move the folder "jenkins_jvm" under Site24x7 Windows Agent plugin directory : 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---

#### Metrics Captured


Name		            	| Description
---         		   	|   ---
blocked_count                   |                   Number of threads that are currently blocked.
total_count                     |                   Total thread count.
deadlock_count                  |                   The number of threads that have a currently detected deadlock.
file_descriptor_ratio           |                   The ratio of used to total file descriptors. 
heap_memory_commited            |                   The amount of memory, in the heap (bytes).
heap_memory_initiated           |                   The amount of memory, in the heap that has been newly initiated (bytes).
maximum_heap_memory             |                   The maximum amount of memory, in the heap, that is used (bytes).
heap_memory_used                |                   The amount of memory, in the heap that is currently in use (bytes).
non-heap_memory_commited        |                   The amount of memory, outside the heap (bytes).
non-heap_memory_initiated       |                   The amount of memory, outside the heap that has been newly initiated (bytes).
maximum_non-heap_memory         |                   The maximum amount of memory, outside the heap, that is used (bytes).
non-heap_memory_used            |                   The amount of memory, outside the heap that is currently in use (bytes).
total_memory_commited           |                   The total amount of memory (bytes).
total_memory_initiated          |                   The total amount of memory, that has been newly initiated (bytes).
total_maximum_memory            |                   The maximum amount of memory (bytes).
total_memory_used               |                   The total amount of memory used (bytes).
new_threads                     |                   The number of threads that have not currently started execution.
running_threads                 |                   The total number of threads that are currently in execution.
terminated_threads              |                   The total number of threads that have completed execution.
suspended_threads               |                   The total number of threads that have suspended execution.
waiting_threads                 |                   The total number of threads that are waiting for execution.
