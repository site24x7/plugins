                                         
#### JENKINS PLUGIN
                                                                                               
=================================================================

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


---

### Plugin Installation  

- Create a directory "jenkins_specific_job" under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/jenkins_specific_job
      
- Download all the files in "jenkins_specific_job" folder and place it under the "jenkins_specific_job" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_specific_job/jenkins_specific_job.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_specific_job/jenkins_specific_job.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python jenkins_specific_job.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --jobname=<job_name>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---

### Configurations


		[jenkins_specific_job]
		host=<host_name> 
		port=<port_number> 
		username=<username>
		password=<password> 
		jobname=<job_name>


### Jenkins specific job monitoring


		METRICS                                       DESCRIPTION


		build_count                                   Number of Builds in the job
		job_lastbuild_queueid                         Queue Id of the last build 
		job_lastbuild_duration                        Time taken for last build(in ms)
		job_lastbuild_estimated_duration               Estimated time for last build(in ms)
		job_lastbuildid                               Id of the last build
		job_lastbuild_number                           Last build's Number in the job
		build_failed                                  Number of builds failed
		build_success                                 Number of successful builds
		build_aborted                                 Number of builds aborted

