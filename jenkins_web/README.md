                                         
# JENKINS PLUGIN
                                                                                               

## What is Jenkins?
	
 Jenkins is an open source automation server written in Java. It helps to execute a series of actions to achieve a continuous integration process. 



## How it's used for Developers?

 Jenkins enables developers around the world to reliably build, test, package, stage and deploy their software.

 With Jenkins, multiple developers from different modules can integrate the code change in a single project. 

## How does it accelerate the development and test process 

 With Jenkins, DevOps can accelerate the software development and testing process thru automation. Once the code is committed by the developer, next the code will be built and tested.

 If the test is passed, then the build will be tested for deployment. After deployment is successful, it's pushed to production.




## Importance of monitoring Jenkins Web:

To run the Jenkins effectively, DevOps team is required to monitor the significant metrics of Jenkins. The continuous monitoring Jenkins will allow DevOps team to view below features.

- Total active requests.
- Time taken to generate response for the request.
- Response status


---

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Follow below steps to generate API key 
- Install the "Metrics plugin" from Jenkins. (Jenkins -> Manage Jenkins -> Manage plugins ->Available)
- (Jenkins -> Manage Jenkins -> Configure system) Generate your API key under the metrics section.

---

### Plugin Installation  

- Create a directory "jenkins_web".

		mkdir jenkins_web
  		cd jenkins_web/
      
- Download all the files in "jenkins_web" folder and place it under the "jenkins_web" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_web/jenkins_web.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_web/jenkins_web.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the jenkins_web.py script.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python jenkins_web.py --host "host" --port "port" --username "username" --password "password" --apikey "apikey"
		
- Change the below configurations in "jenkins_performance.cfg" file

		[jenkins_web]
		host="host"
		port="port"
		username="username"
		password="password" 
		apikey="apikey"
			
- Move the directory "jenkins_web" under Site24x7 Linux Agent plugin directory : 

		mv jenkins_web /opt/site24x7/monagent/plugins/


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---

#### Metrics Captured

Name		            	| Description
---         		   	|   ---
total_activerequests                |               The total number of requests that are currently active
total_badrequest                    |               The total number of request with HTTP/400 status code
total_responsecode_created          |               The total number of request with HTTP/201 status code
total_forbidden_responsecode        |               The total number of request with HTTP/403 status code
noContent_responsecode              |               The total number of request with HTTP/204 status code
notFound_responsecode               |               The total number of request with HTTP/404 status code
unmodified_responsecode             |               The total number of request with HTTP/304 status code
success_responsecpde                |               The total number of request with HTTP/200 status code
non_informational_responsecode      |               The total number of request with a non information status code
servererror_responsecode            |               The total number of request with HTTP/500 status code
service_unavailable                 |               The total number of request with HTTP/503 status code
request_duration                    |               Time taken to generate the corresponding code
