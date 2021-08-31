                                         
 #### JENKINS PLUGIN
                                                                                               
================================================================================

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


		node_count                                          Number of node
		health-check_count                                  The number of health checks associated
		health-check_duration                               The rate at which the health checks are running (sec)
		nodes_offline                                       Number of offline nodes
		nodes_online                                        Number of online nodes
		projects_count                                      Project count
		projects_disabled                                   Number of disabled projects
		projects_enabled                                    Number of enabled projects
		queue_size                                          Number of jobs in queue
		executor_count                                      Number of executors available for Jenkins
		executors_free_count                                Number of executors available for Jenkins that are not currently in use
		executors_inuse_count                               Number of executors in use
		queues_pending                                      Number of pending jobs in the queue
		queues_stuck                                        Number of stucked jobs in the queue
		queues_blocked                                      Number of jobs that are blocked in the queue
		jobs_in_queue                                       Number of buildable items in queue
		plugins_active                                      Number of active plugins
		plugins_failed                                      Number of plugins failed
		plugins_inactive                                    Number of inactive plugins
		plugins_withupdate                                  Number of plugins with update
		builds_blocked_duration                             Time taken by the jobs in blocked state (sec)
		build_creation_time                                 Time taken by the build to complete (sec)
		builds_execution_duration                           Build execution time (sec)
		builds_queuing_duration                             Build queuing time (sec)
		builds_waiting_duration                             Time taken by the build by waiting in a queue (sec)


