                                         
# JENKINS PLUGIN
                                                                                               

### What is Jenkins?
	
 Jenkins is an open source automation server written in Java. It helps to execute a series of actions to achieve a continuous integration process. 


### How it's used for Developers?

 Jenkins enables developers around the world to reliably build, test, package, stage and deploy their software.

 With Jenkins, multiple developers from different modules can integrate the code change in a single project. 

### How does it accelerate the development and test process 

 With Jenkins, DevOps can accelerate the software development and testing process thru automation. Once the code is committed by the developer, next the code will be built and tested.

 If the test is passed, then the build will be tested for deployment. After deployment is successful, it's pushed to production.


### Importance of monitoring Jenkins specific job:

To run the Jenkins effectively, DevOps team is required to monitor the significant metrics of Jenkins. The continuous monitoring Jenkins will allow DevOps team to view below features.

- Total number of builds in the job.
- Number of successfull builds and failed builds in the job.
- Time taken for last build.
- Queue Id for the last build.


---

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python version 3 or higher.


---

## Plugin Installation  

- Create a directory "jenkins_specific_job".
  
		mkdir jenkins_specific_job
  		cd jenkins_specific_job/
  
- Download all the files and place it under the "jenkins_specific_job" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_specific_job/jenkins_specific_job.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_specific_job/jenkins_specific_job.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the jenkins_specific_job.py script.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python jenkins_specific_job.py --host "host" --port "port" --username "username" --password "password" --jobname "job_name"

- Change the below configurations in "jenkins_specific_job.cfg" file

		[jenkins_specific_job]
		host="host"
		port="port"
		username="username"
		password="password" 
		jobname="job_name"

##### Linux 

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the jenkins_specific_job.py script.

- Move the directory "jenkins_specific_job" under Site24x7 Linux Agent plugin directory : 

		mv jenkins_specific_job /opt/site24x7/monagent/plugins/



##### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.


- Move the folder "jenkins_specific_job" under Site24x7 Windows Agent plugin directory : 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---
### Metrics Captured

Name		            	| Description
---         		   	|   ---
build_count                        |           Number of Builds in the job.
job_lastbuild_queueid              |           Queue Id of the last build .
job_lastbuild_duration             |           Time taken for last build(in ms).
job_lastbuild_estimated_duration   |            Estimated time for last build(in ms).
job_lastbuildid                    |           Id of the last build.
job_lastbuild_number               |            Last build's Number in the job.
build_failed                       |           Number of builds failed.
build_success                      |           Number of successful builds.
build_aborted                      |           Number of builds aborted.

