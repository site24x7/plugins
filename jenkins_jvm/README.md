                                
#### JENKINS PLUGIN
                                                                                               
===============================================================

## What is Jenkins?
	
 Jenkins is an open source automation server written in Java. It helps to execute a series of actions to achieve a continuous integration process. 



## How it's used for Developers?

 Jenkins enables developers around the world to reliably build, test, package, stage and deploy their software.

 With Jenkins, multiple developers from different modules can integrate the code change in a single project. 

## How does it accelerate the development and test process 

 With Jenkins, DevOps can accelerate the software development and testing process thru automation. Once the code is committed by the developer, next the code will be built and tested.

 If the test is passed, then the build will be tested for deployment. After deployment is successful, it's pushed to production.




## Importance of monitoring Jenkins:

To run the Jenkins effectively, DevOps team is required to monitor the significant metrics of Jenkins. The continuous monitoring Jenkins will allow DevOps team to view below features.

- Analyse trends - Successful build has gone out today, Failure builds which was in the queue.
- Comparison of feature releases between weeks.
- Jenkins latency shot up.
- Instant alert when any entity has broken.


---

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Follow below steps to generate API key 
- Install the "Metrics plugin" from Jenkins. (Jenkins -> Manage Jenkins -> Manage plugins ->Available)
- (Jenkins -> Manage Jenkins -> Configure system) Generate your API key under the metrics section.

---

### Plugin Installation  

- Create a directory "jenkins_jvm" under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/jenkins_jvm
      
- Download all the files in "jenkins_jvm" folder and place it under the "jenkins_jvm" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_jvm/jenkins_jvm.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_jvm/jenkins_jvm.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python jenkins_jvm.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --apikey=<apikey>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---

### Configurations

		[jenkins_jvm]
		host=<host_name> 
		port=<port_number> 
		username=<username> 
		password=<password> 
		apikey=<apikey>

---

#### Jenkins jvm Monitoring:


		METRICs                                            DESCRIPTION
	
		Blocked Count                                      Number of threads that are currently blocked
		Total Count                                        Total thread count
		Deadlock Count                                     The number of threads that have a currently detected deadlock 
		File descriptor Ratio                              The ratio of used to total file descriptors. 
		Heap Memory Commited                               The amount of memory, in the heap (bytes)
		Heap Memory Initiated                              The amount of memory, in the heap that has been newly initiated (bytes)
		Maximum Heap Memory                                The maximum amount of memory, in the heap, that is used (bytes)
		Heap Memory Used                                   The amount of memory, in the heap that is currently in use (bytes)
		Non-Heap Memory Commited                           The amount of memory, outside the heap (bytes)
		Non-Heap Memory Initiated                          The amount of memory, outside the heap that has been newly initiated (bytes)
		Maximum Non-Heap Memory                            The maximum amount of memory, outside the heap, that is used (bytes)
		Non-Heap Memory Used                               The amount of memory, outside the heap that is currently in use (bytes)
		Total Memory Commited                              The total amount of memory (bytes)
		Total Memory Initiated                             The total amount of memory, that has been newly initiated (bytes)
		Total Maximum Memory                               The maximum amount of memory (bytes)
		Total Memory Used                                  The total amount of memory used (bytes)
		New Threads                                        The number of threads that have not currently started execution
		Running Threads                                    The total number of threads that are currently in execution
		Terminated Threads                                 The total number of threads that have completed execution
		Suspended Threads                                  The total number of threads that have suspended execution
		Waiting Threads                                    The total number of threads that are waiting for execution
