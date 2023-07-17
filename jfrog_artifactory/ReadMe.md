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
		
### Metrics collected :

	1.  Artifacts Size : The total size of all artifacts stored in JFrog Artifactory.

	2.  Binaries Count : The number of binary files stored in JFrog Artifactory.

	3.  Binaries Size : The total size of all binary files stored in JFrog Artifactory.

	4.  <Repo-Type> Repository Count : The number of a mentioned type of repository in JFrog Artifactory.

	5.  Committed Virtual Memory Size : The amount of virtual memory committed by the JFrog Artifactory process.

	6.  Days Till Licence Expiry : The number of days remaining until the JFrog Artifactory license expires.

	7.  Free Physical Memory Size : The amount of free physical memory available on the system hosting JFrog Artifactory, measured in megabytes (MB).

	8.  Free Space : The amount of free disk space available for storing artifacts in JFrog Artifactory.
	
	9.  Free Space in % : The percentage of free disk space available for storing artifacts in JFrog Artifactory.

	10.  Free Swap Space Size : The amount of free swap space available on the system hosting JFrog Artifactory.

	11.  Heap Memory Max : The maximum amount of heap memory allocated to the JFrog Artifactory JVM.

	12.  Heap Memory Usage : The current heap memory usage of the JFrog Artifactory JVM, expressed as a percentage.

	13.  JVM Up Time : The total uptime of the JFrog Artifactory JVM in seconds.

	14.  Max File Descriptor Count : The maximum number of file descriptors that the JFrog Artifactory process can open.

	15.  No of Repositories : The total number of repositories (local, remote, and virtual) in JFrog Artifactory.

	16.  None Heap Memory Usage : The current non-heap memory usage of the JFrog Artifactory JVM, expressed as a percentage.

	17.  Number Of Cores : The number of CPU cores available on the system hosting JFrog Artifactory.

	18.  Open File Descriptor Count : The current number of open file descriptors by the JFrog Artifactory process.

	19.  Optimization : The level of optimization in JFrog Artifactory, expressed as a percentage.

	20.  Process Cpu Load : The current CPU load on the JFrog Artifactory process, expressed as a percentage.

	21.  Process Cpu Time : The total CPU time used by the JFrog Artifactory process since it started, measured in milliseconds.

	22.  Security Groups : The number of security groups defined in JFrog Artifactory.

	23.  Security Users : The number of security users defined in JFrog Artifactory.

	24.  System Cpu Load : The current CPU load on the entire system hosting JFrog Artifactory, expressed as a percentage.

	25.  Thread Count : The current number of active threads in the JFrog Artifactory JVM.

	26.  Total Physical Memory Size : The total amount of physical memory available on the system hosting JFrog Artifactor.

	27.  Total Space : The total disk space available for storing artifacts in JFrog Artifactory.

	28.  Total Swap Space Size : The total amount of swap space available on the system hosting JFrog Artifactory.

	29.  Used Space : The amount of disk space currently used for storing artifacts in JFrog Artifactory.

	30.  Used Space in % : The percentage of disk space currently used for storing artifacts in JFrog Artifactory.

	31.  status : The current status of JFrog Artifactory, represented by a numeric code.

	32.  licensedTo : The entity or organization for which JFrog Artifactory is licensed.

	33.  type : The type of license

	34.  validThrough : The date until which the current license remains valid.
