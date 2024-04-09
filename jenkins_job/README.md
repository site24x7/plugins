                                         
# JENKINS PLUGIN
                                                                                               
### What is Jenkins?
	
 Jenkins is an open source automation server written in Java. It helps to execute a series of actions to achieve a continuous integration process.

### How it's used for Developers?

 Jenkins enables developers around the world to reliably build, test, package, stage and deploy their software.

 With Jenkins, multiple developers from different modules can integrate the code change in a single project. 

### How does it accelerate the development and test process 

 With Jenkins, DevOps can accelerate the software development and testing process thru automation. Once the code is committed by the developer, next the code will be built and tested.

 If the test is passed, then the build will be tested for deployment. After deployment is successful, it's pushed to production.


### Importance of monitoring Jenkins Job:

To run the Jenkins effectively, DevOps team is required to monitor the significant metrics of Jenkins. The continuous monitoring Jenkins will allow DevOps team to view below features.

- Total number of jobs.
- Sucsessful jobs and failed jobs.
- Time taken to execute the jobs.
- Number of jobs waiting in queue.


---

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Follow below steps to generate API key 
	- Install the "Metrics plugin" from Jenkins. (Jenkins -> Manage Jenkins -> Manage plugins ->Available)
	- (Jenkins -> Manage Jenkins -> Configure system) Generate your API key under the metrics section.
- Python version 3 or higher.

---

## Plugin Installation  

- Create a directory "jenkins_job".
  
		mkdir jenkins_job
  		cd jenkins_job/
  
- Download all the files and place it under the "jenkins_job" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_job/jenkins_job.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_job/jenkins_job.cfg



- Execute the below command with appropriate arguments to check for the valid json output.  

		python jenkins_job.py --host "host" --port "port" --username "username" --password "password" --apikey "apikey"

- Change the below configurations in "jenkins_job.cfg" file

		[jenkins_job]
		host = "host"
		port = "port"
		username = "username"
		password = "password"
		apikey = "apikey"

##### Linux 

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the jenkins_job.py script.
  
- Move the directory "jenkins_job" under Site24x7 Linux Agent plugin directory : 

		mv jenkins_job /opt/site24x7/monagent/plugins/

##### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Move the folder "jenkins_job" under Site24x7 Windows Agent plugin directory : 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 -> Plugins -> Plugin Integrations.
		
---
### Metrics Captured

Name		            	| Description
---         		   	|   ---
job_count                       |                    Number of jobs.
jobs_scheduled_rate             |                    The rate at which the jobs are scheduled (events/minute).
jobs_blocked_duration           |                    The time taken by the jobs in the build queue in the blocked state (sec).
jobs_buildable_duration         |                    The time taken by the jobs in the build queue in the buildable state (sec).
jobs_execution_time             |                    Time taken for job execution (sec).
jobs_queuing_duration           |                    Time taken by the job in the build queue (sec).
jobs_total_duration             |                    Time taken by the job from entering the build queue to completing building (sec).
jobs_waiting_duration           |                    Time taken by the jobs to spend in their quiet period (sec).



