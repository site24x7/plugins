# JFROG ARTIFACTORY MONITORING

=================================================================

JFrog Artifactory is a universal repository manager used in software development to manage and store various types of binary artifacts. It provides a centralized location for storing and retrieving software components, making it easier to manage dependencies, version control, and deployment across different platforms and environments.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Ensure you have Python version 3 or higher installed in your server. 

### Plugin Installation 

- Create a directory named "jfrog_artifactory".
- Download the below files in and place it under the "jfrog_artifactory" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jfrog_artifactory/jfrog_artifactory.py

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jfrog_artifactory/jfrog_artifactory.cfg

- To check if the plugin is working, execute the command below with appropriate arguments and check for a valid JSON output with applicable metrics and their corresponding values.  

		python jfrog_artifactory.py --api_key=<api-key>  --artifactory_url=<artifactory-url>

- Add the applicable configurations in the jfrog_artifactory.cfg file:

		[JFrog Artifactory Monitoring]
		api_key = <api-key> 
		artifactory_url = <artifactory_url>
Note for the above parameters:

 - api_key - Generate the API key and add it if there is any authentication present. Otherwise set the parameter as 'None'
 - artifactory_url - Add the Artifactory's URL with port. 
eg: "http://127.0.1.1:8082/artifactory"
		
