# IBM AS/400 MONITORING

### What is IBM AS/400 ?

IBM iSeries is one of the most reliable and secure servers used by multiple enterprises across industries worldwide. The IBM AS400 comes with hardware, software, security, a database, and other components built in. It is robust, adaptable, and can easily incorporate new technologies. 
 
IBM AS400/iSeries is used by enterprises from industries such as banking, insurance, and manufacturing, where the uptime and performance of applications are business-critical. Site24x7's IBM AS400/iSeries plugin integration tracks server availability and performance, helping you to identify and fix issues before they affect end users.

### Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Make sure you have installed Java installed in your server.

### Linux

- Create a directory named `IBM_iSeries_AS400`.

 		mkdir IBM_iSeries_AS400
  		cd IBM_iSeries_AS400/
		
- Download the files "IBM_iSeries_AS400.cfg" , "IBM_iSeries_AS400.py" , "As400DataCollector.java", "json-20140107.jar", "jt400.jar" and place it under the "IBM_iSeries_AS400" directory using following commands:
  	```
  	 wget https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/IBM_iSeries_AS400.py
  	 wget https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/IBM_iSeries_AS400.cfg
  	 wget https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/As400DataCollector.java
  	 wget https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/json-20140107.jar
  	 wget https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/jt400.jar
   	```
- Open IBM_iSeries_AS400.cfg file and set the values for host, username, password, java_path.

	```ini
 	[IBM_iSeries_AS400]
	host="localhost"
	username="user" 
	password="test"
	java_path="/usr/bin"
 	```

- Run the command- which java. Copy the output you get and paste it in the JAVA_HOME field. Make sure to paste the path to bin directory and not the path to java.

- Run the below command with apprpriate values to check the manual execution of the plugin.

	```bash
 	python3 IBM_iSeries_AS400.py --host "localhost" --username "user" --password "test" --java_path "/usr/bin"
	```

- Move the `IBM_iSeries_AS400` folder to the site24x7 agent directory.
	```
	mv IBM_iSeries_AS400 /opt/site24x7/monagent/plugins/IBM_iSeries_AS400
	```
- Once configured the agent will automatically execute the plugin in five minutes interval and send performance data to the Site24x7 data center.


### Windows

- Create a directory `IBM_iSeries_AS400`. 

- Download the files [IBM_iSeries_AS400.cfg](https://github.com/site24x7/plugins/blob/master/IBM_iSeries_AS400/IBM_iSeries_AS400.cfg) , [IBM_iSeries_AS400.ps1](https://github.com/site24x7/plugins/blob/master/IBM_iSeries_AS400/IBM_iSeries_AS400.ps1), [As400DataCollector.java](https://github.com/site24x7/plugins/blob/master/IBM_iSeries_AS400/As400DataCollector.java), [json-20140107.jar](https://github.com/site24x7/plugins/blob/master/IBM_iSeries_AS400/json-20140107.jar), [jt400.jar](https://github.com/site24x7/plugins/blob/master/IBM_iSeries_AS400/jt400.jar) and place it under the `IBM_iSeries_AS400` directory.

- Open IBM_iSeries_AS400.cfg file and set the values for host, username, password, java_path.

	```ini
 	[IBM_iSeries_AS400]
	host="localhost"
	username="user" 
	password="test"
	java_path="C:\Program Files\Java\jdk1.8.0_241\bin"
 	```
 
- Run the command- where java. Copy the output of, bin directory of jdk and not the path to java.

- Run the below command with apprpriate values to check the manual execution of the plugin.
	```bash
 	python IBM_iSeries_AS400.py --host "localhost" --username "user" --password "test" --java_path "C:\Program Files\Java\jdk1.8.0_241\bin"
 	```
 
- Move the `IBM_iSeries_AS400` into the Site24x7 Windows Agent plugin directory.
	```
	 C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\IBM_iSeries_AS400
	```
- Once configured the agent will automatically execute the plugin in five minutes interval and send performance data to the Site24x7 data center.

### Metrics Captured

Name		        			| Description
---         					|   ---
ASP Percentage 					|	 The percentage of the auxiliary storage pool currently in use.
ASP Total 					|	 The storage capacity of the system auxiliary storage pool in MB.
CPU Percentage 					|	 The average of the elapsed time during which the processing units were in use.
Permanent Address Percentage 			|	 The percentage of the maximum possible addresses for permanent objects that have been used.
Temporary Address Percentage 			|	 The percentage of the maximum possible addresses for temporary objects that have been used.
Current Unprotected Used 			|	 The current amount of storage in use for temporary objects in MB.
Maximum Unprotected 				|	 The largest amount of storage for temporary object used at any one time since the last IPL in MB.
Main Storage 					|	 The amount of main storage, in kilobytes, in the system.
Number Of Processors 				|	 The number of processors that are currently active in this partition.
Number of Pools 				|	 The number of system pools.
Users SignedOn 					|	 The number of users currently signed on the system.
Total Jobs 					|	The total number of user jobs and system jobs that are currently in the system.
No of Active Jobs 				|	 The number of jobs active in the system including both user and system jobs.
No of Batch Jobs 				|	 The number of batch jobs currently running on the system.
Jobs Waiting for Message 			|	 The number of batch jobs waiting for a reply to a message before they can continue to run.
Active Threads 					|	 The number of initial and secondary threads in the system , including both user and system threads.
Batch Jobs Waiting to Print 			|	 The number of completed batch jobs that produced printer output that is waiting to print.
Batchjobs Ending 				|	 The number of batch jobs that are in the process of ending.
Batchjobs Held on Jobqueue 			|	 The number of batch jobs that were submitted, but were held before they could begin running.
Batchjobs Held While Running 			|	 The number of batch jobs that had started running, but are now held.
Batchjobs on Held Jobqueue 			|	 The number of batch jobs on job queues that have been assigned to a subsystem, but are being held.
Batchjobs on Unassigned Jobqueue 		|	 The number of batch jobs on job queues that have not been assigned to a subsystem.
Batchjobs Waitingto Run 			|	 The number of batch jobs on the system that are currently waiting to run.
No of Partitions 				|	 The number of partitions on the system.
Total Auxiliary Storage 			|	 The total auxiliary storage on the system in MB.
User Sessions Ended for Waiting to Print	|	 The number of sessions that have ended with printer output files waiting to print.
User Suspended by Groupjobs 			|	 The number of user jobs that have been temporarily suspended by group jobs so that another job may be run.
User Suspended by Systemrequest 		|	 The number of user jobs that have been temporarily suspended by system request jobs so that another job may be run.
Users Temporarily Signedoff 			|	 The number of jobs that have been disconnected due to either the selection of option 80 (Temporary sign-off) or the entry of the Disconnect Job (DSCJOB) command.
Current Processing Capacity 			|	 The amount of current processing capacity of the partition.
Current Interactive Performance Percentage 	|	 The percentage of interactive performance assigned to this logical partition.
Maximum Jobs 					|	 The maximum number of jobs that are allowed on the system.
Shared Processing Pooler 			|	 The percentage of the total shared processor pool capacity used by all partitions using the pool during the elapsed time.
Uncapped CPU Capacity Percentage 		|	 The percentage of the uncapped shared processing capacity for the partition that was used during the elapsed time.
System Name					|	 Name of the system
Model 						|	 System model.
System Version  				|	  Version of the system
Serial 						|	 System serial number
Security Level					|	 Global security level
Auto Device Configuration 			|	 Automatic device configuration indicator. 
System Console 					|	 Name of the system console.
Job Message Queue Maximum Size 			|	 Initial size of job message queue in KB. 
Job Message Queue Maximum Size 			|	 Maximum size of job message queue in KB.
Spooling Control Initial Size 			|	 Initial size of spooling control block for a job in bytes.
    
