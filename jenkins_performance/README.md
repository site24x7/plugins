                                         
 #### JENKINS PLUGIN
                                                                                               
==========================================================================================================================

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

- Create a directory "jenkins_performance" under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/jenkins_performance
      
- Download all the files in "jenkins_performance" folder and place it under the "jenkins_performance" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_performance/jenkins_performance.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_performance/jenkins_performance.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python jenkins_performance.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --apikey=<apikey>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---

### Configurations

		[jenkins_performance]
		host = <host_name>
		port = <port_number>
		username = <username>
		password = <password>
		apikey = <apikey>
	
---
#### Jenkins performance monitoring:


		METRICS                                             DESCRIPTION


		NodeCount                                           Number of node
		Health-check Count                                  The number of health checks associated
		Health-check Duration                               The rate at which the health checks are running (sec)
		Nodes Offline                                       Number of offline nodes
		Nodes Online                                        Number of online nodes
		Projects Count                                      Project count
		Projects Disabled                                   Number of disabled projects
		Projects Enabled                                    Number of enabled projects
		Queue Size                                          Number of jobs in queue
		Executor Count                                      Number of executors available for Jenkins
		Executors Free Count                                Number of executors available for Jenkins that are not currently in use
		Executors Inuse Count                               Number of executors in use
		Queues Pending                                      Number of pending jobs in the queue
		Queues Stuck                                        Number of stucked jobs in the queue
		Queues Blocked                                      Number of jobs that are blocked in the queue
		Jobs in Queue                                       Number of buildable items in queue
		Plugins Active                                      Number of active plugins
		Plugins Failed                                      Number of plugins failed
		Plugins Inactive                                    Number of inactive plugins
		Plugins Withupdate                                  Number of plugins with update
		Builds Blocked duration                             Time taken by the jobs in blocked state (sec)
		Build Creation Time                                 Time taken by the build to complete (sec)
		Builds Execution Duration                           Build execution time (sec)
		Builds Queuing Duration                             Build queuing time (sec)
		Builds Waiting Duration                             Time taken by the build by waiting in a queue (sec)


