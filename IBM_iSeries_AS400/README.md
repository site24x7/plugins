# IBM AS/400 MONITORING

### What is IBM AS/400 ?

IBM iSeries is one of the most reliable and secure servers used by multiple enterprises across industries worldwide. The IBM AS400 comes with hardware, software, security, a database, and other components built in. It is robust, adaptable, and can easily incorporate new technologies. 
 
IBM AS400/iSeries is used by enterprises from industries such as banking, insurance, and manufacturing, where the uptime and performance of applications are business-critical. Site24x7's IBM AS400/iSeries plugin integration tracks server availability and performance, helping you to identify and fix issues before they affect end users.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Make sure you have installed Java installed in your server.

### Linux

- Create a directory named "IBM_iSeries_AS400": 
		
- Download the files "IBM_iSeries_AS400.sh" , "As400DataCollector.java", "json-20140107.jar", "jt400.jar" and place it under the "IBM_iSeries_AS400" directory using following commands:
    
    		wget https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/IBM_iSeries_AS400.sh
    
    		wget https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/As400DataCollector.java
    
    		wget https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/json-20140107.jar
    
    		wget https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/jt400.jar
    		
- Open IBM_iSeries_AS400.sh file and set the values for HOST, USERNAME, PASSWORD, JAVA_HOME

- Run the command- which java. Copy the output you get and paste it in the JAVA_HOME field. Make sure to paste the path to bin directory and not the path to java.

- Move the "IBM_iSeries_AS400" folder to the site24x7 agent directory
```
  Linux             ->   /opt/site24x7/monagent/plugins/IBM_iSeries_AS400
```
- Once configured the agent will automatically execute the plugin in five minutes interval and send performance data to the Site24x7 data center.


### Windows

- Create a directory "IBM_iSeries_AS400" 

- Download the files "IBM_iSeries_AS400.bat" , "As400DataCollector.java", "json-20140107.jar", "jt400.jar" and place it under the "IBM_iSeries_AS400" directory:

     		https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/IBM_iSeries_AS400.bat
    
    		https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/As400DataCollector.java
    
    		https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/json-20140107.jar
    
    		https://raw.githubusercontent.com/site24x7/plugins/master/IBM_iSeries_AS400/jt400.jar
    		
- Open IBM_iSeries_AS400.bat file and set the values for HOST, USERNAME, PASSWORD, JAVA_HOME

- Run the command- where java. Copy the output of, bin directory of jdk and not the path to java.

- Move the "IBM_iSeries_AS400" into the Site24x7 Windows Agent plugin directory.
```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\IBM_iSeries_AS400
```
- Once configured the agent will automatically execute the plugin in five minutes interval and send performance data to the Site24x7 data center.

### Metrics Captured

		1.ASP Percentage - The percentage of the auxiliary storage pool currently in use.
		2.ASP Total - The storage capacity of the system auxiliary storage pool in MB.
		3.CPU Percentage - The average of the elapsed time during which the processing units were in use.
		4.Permanent Address Percentage - The percentage of the maximum possible addresses for permanent objects that have been used.
		5.Temporary Address Percentage - The percentage of the maximum possible addresses for temporary objects that have been used.
		6.Current Unprotected Used - The current amount of storage in use for temporary objects in MB.
		7.Maximum Unprotected - The largest amount of storage for temporary object used at any one time since the last IPL in MB.
		8.Main Storage - The amount of main storage, in kilobytes, in the system.
		9.Number Of Processors - The number of processors that are currently active in this partition.
		10.Number of Pools - The number of system pools.
		11.Users SignedOn - The number of users currently signed on the system.
		12.Total Jobs - The total number of user jobs and system jobs that are currently in the system.
		13.No of Active Jobs - The number of jobs active in the system including both user and system jobs.
		14.No of Batch Jobs - The number of batch jobs currently running on the system.
		15.Jobs Waiting for Message - The number of batch jobs waiting for a reply to a message before they can continue to run.
		16.Active Threads - The number of initial and secondary threads in the system , including both user and system threads.
		17.Batch Jobs Waiting to Print - The number of completed batch jobs that produced printer output that is waiting to print.
		18.Batchjobs Ending - The number of batch jobs that are in the process of ending.
		19.Batchjobs Held on Jobqueue - The number of batch jobs that were submitted, but were held before they could begin running.
		20.Batchjobs Held While Running - The number of batch jobs that had started running, but are now held.
		21.Batchjobs on Held Jobqueue - The number of batch jobs on job queues that have been assigned to a subsystem, but are being held.
		22.Batchjobs on Unassigned Jobqueue - The number of batch jobs on job queues that have not been assigned to a subsystem.
		23.Batchjobs Waitingto Run - The number of batch jobs on the system that are currently waiting to run.
		24.No of Partitions - The number of partitions on the system.
		25.Total Auxiliary Storage - The total auxiliary storage on the system in MB.
		26.User Sessions Ended for Waiting to Print - The number of sessions that have ended with printer output files waiting to print.
		27.User Suspended by Groupjobs - The number of user jobs that have been temporarily suspended by group jobs so that another job may be run.
		28.User Suspended by Systemrequest - The number of user jobs that have been temporarily suspended by system request jobs so that another job may be run.
		29.Users Temporarily Signedoff - The number of jobs that have been disconnected due to either the selection of option 80 (Temporary sign-off) or the entry of the Disconnect Job (DSCJOB) command.
		30.Current Processing Capacity - The amount of current processing capacity of the partition.
		31.Current Interactive Performance Percentage - The percentage of interactive performance assigned to this logical partition.
		32.Maximum Jobs - The maximum number of jobs that are allowed on the system.
		33.Shared Processing Pooler - The percentage of the total shared processor pool capacity used by all partitions using the pool during the elapsed time.
		34.Uncapped CPU Capacity Percentage - The percentage of the uncapped shared processing capacity for the partition that was used during the elapsed time.
		35.System Name - Name of the system
		36.Model - System model.
		37.System Version  -  Version of the system
		38.Serial - System serial number
		39.Security Level - Global security level
		40.Auto Device Configuration - Automatic device configuration indicator. 
		41.System Console - Name of the system console.
		42.Job Message Queue Maximum Size - Initial size of job message queue in KB. 
		43.Job Message Queue Maximum Size - Maximum size of job message queue in KB.
		44.Spooling Control Initial Size - Initial size of spooling control block for a job in bytes.
    
