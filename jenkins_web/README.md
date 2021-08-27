                                         
                                                                                               JENKINS PLUGIN
                                                                                               
========================================================================================================================================================================================== 

##What is Jenkins?
	
	Jenkins is an open source automation server written in Java. It helps to execute a series of actions to achieve a continuous integration process. 



##How it's used for Developers?

	Jenkins enables developers around the world to reliably build, test, package, stage and deploy their software.

	With Jenkins, multiple developers from different modules can integrate the code change in a single project. 

##How does it accelerate the development and test process 

	With Jenkins, DevOps can accelerate the software development and testing process thru automation. Once the code is committed by the developer, next the code will be built and tested.

       If the test is passed, then the build will be tested for deployment. After deployment is successful, it's pushed to production.




##Importance of monitoring Jenkins:

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

- Create a directory "jenkins_web" under Site24x7 Linux Agent plugin directory : 

	Linux             ->   /opt/site24x7/monagent/plugins/jenkins_web
---
      
- Download all the files in "jenkins_web" folder and place it under the "jenkins_web" directory

	wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_web/jenkins_web.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/jenkins_web/jenkins_web.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

	python jenkins_web.py --host=<host_name> --port=<port_number> --username=<username> --password=<password> --apikey=<apikey>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Configurations
---

host=<host_name>
-
port=<port_number>
-
username=<your_username>
-
password=<your_password>
-
apikey=<your_api_key>
---
####Jenkins web Monitoring:


METRICs                                            DESCRIPTION


Total ActiveRequests                               The total number of requests that are currently active
Total BadRequest                                   The total number of request with HTTP/400 status code
Total Responsecode Created                         The total number of request with HTTP/201 status code
Total Forbidden Responsecode                       The total number of request with HTTP/403 status code
NoContent Responsecode                             The total number of request with HTTP/204 status code
NotFound Responsecode                              The total number of request with HTTP/404 status code
Unmodified Responsecode                            The total number of request with HTTP/304 status code
Success Responsecpde                               The total number of request with HTTP/200 status code
Non Informational Responsecode                     The total number of request with a non information status code
ServerError Responsecode                           The total number of request with HTTP/500 status code
Service Unavailable                                The total number of request with HTTP/503 status code
Request Duration                                   Time taken to generate the corresponding code
