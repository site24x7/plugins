# Plugin for GlassFish Monitoring


GlassFish is an open source application server project sponsored by Oracle corporation. Configure Site24x7 plugin to monitor the performance of your GlassFish servers.

Get to know how to configure the Oracle GlassFish plugins and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of GlassFish servers.

Learn more: https://www.site24x7.com/plugins/glassfish-plugin-monitoring.html

## GlassFish plugin installer

On Linux servers, execute the command below in the terminal to run an installer that checks the prerequisites and installs the plugin.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/installer/Site24x7GlassFishPluginInstaller.sh && sudo bash Site24x7GlassFishPluginInstaller.sh
```

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.

### Plugin Installation  

- Create a directory named `glassfish`.

  ```bash
  mkdir glassfish
  cd glassfish/
  ```
      
- Download all the files and place it under the `glassfish` directory.

  ```bash
  wget https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/glassfish.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/glassfish.cfg
  ```

 
- Execute the below command with appropriate arguments to check for the valid json output:
  ```bash
  python3 glassfish.py --host "hostname" --port "port no" --username "username" --password "password" --ssl "false"  --insecure "false"
  ```


#### Configurations

- Provide your IBM MQ configurations in glassfish.cfg file.
  ```ini
  [localhost]
  host="localhost"
  port="4848"
  ssl="false"  
  insecure="false"
  username="None"
  password="None"
  ```
 - Where,
   - host: The IP address or domain name of the server you're trying to connect to.
   - port: Admin port of the glassfish server.
   - ssl: Connect with https if "true" and http if "false".
   - insecure: If this parameter is set to "true", it allows you to connect even if the certificate is invalid. This should only be used in testing environments.
   - username and password: These credentials are required if any form of authentication is set up for the server.

#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the glassfish.py script.

- Move the folder `glassfish` into the Site24x7 Linux Agent plugin directory: 

		mv glassfish /opt/site24x7/monagent/plugins/
  
#### Windows
		
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Move the folder `glassfish` under Site24x7 Windows Agent plugin folder: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
	
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---	

## Supported Metrics

Name		            		| 	Description
---         		   		|   	---
Used Non Heap Size  			| 	Amount of used non-heap memory in bytes
MaxHeap Size  				| 	Maximum amount of heap memory in bytes that can be used for memory management
Init HeapSize  				| 	Amount of heap memory in bytes that the JVM initially requests from OS for memory management
Init Non Heap Size  			| 	Amount of non-heap memory in bytes that the JVM initially requests from OS for memory management
Used Heap Size  			| 	Amount of used heap memory in bytes
Committed Non Heap Size  		| 	Amount of non-heap memory in bytes that is committed for the JVM to use
Object Pending Finalization Count  	| 	Approximate number of objects for which finalization is pending
Max Non Heap Size  			| 	Maximum amount of non-heap memory in bytes that can be used for memory management
Committed Heap Size  			| 	Amount of heap memory in bytes that is committed for the JVM to use
Dead Locked Threads  			| 	No of threads in deadlock waiting to acquire object monitors or ownable synchronizers
Total Started Thread Count  		| 	No of threads created and also started since the Java virtual machine started
Daemon Thread Count  			| 	No of live daemon threads
Monitor Dead Locked Threads  		| 	number of threads in deadlock waiting to acquire object monitors
Current Thread User Time  		| 	CPU time for a thread executed in user mode
Peak Thread Count  			| 	The peak live thread count since the Java virtual machine started or peak was reset
Thread Count  				| 	Number of live threads including both daemon and non-daemon threads
Current Thread CPU Time  		| 	Total CPU time for the current thread in nanoseconds
Error Count  				| 	Cumulative value of the error count with error count representing the number of cases where the response code was greater than or equal to 400
Avg Processing Time 			| 	Average request processing time
Request Count  				| 	Cumulative number of requests processed so far
Max Time  				| 	Longest response time for a request; not a cumulative value but the largest response time from among the response times
Active Servlets Loaded  		| 	Number of Servlets loaded
Servlet Processing Times  		| 	Cumulative Servlet processing times
Total Servlets Loaded  			| 	Total number of Servlets loaded
Bytes Received  			| 	Total number of bytes received
Bytes Transmitted  			| 	Total number of bytes transmitted
Responses with status code of 200  	| 	Number of responses with a status code of 200
Responses with status code of 401  	| 	Number of responses with a status code of 401
Responses with status code of 404  	| 	Number of responses with a status code of 404
Responses with status code of 503  	|	Number of responses with a status code of 503
2xx					|	Number of responses with a status code in the 2xx range
3xx					|	Number of responses with a status code in the 3xx range
4xx					|	Number of responses with a status code in the 4xx range
5xx					|	Number of responses with a status code in the 5xx range
other					|	Number of responses with a status code outside the 2xx, 3xx, 4xx, and 5xx range
Transactions Committed  		| 	Number of committed transactions
Transactions Rolled Back  		| 	Number of rolled back transactions
Total Sessions  			| 	Total number of sessions
Active Sessions  			| 	Number of active sessions
Expired Sessions  			| 	Total number of expired sessions
Rejected Sessions  			| 	Total number of rejected sessions
GC Count  				| 	Number of garbage collections that have occurred
GC Time  				| 	Approximate accumulated collection elapsed time in milliseconds
Classes Loaded  			|	Number of classes that are currently loaded in the JVM
Total Classes Loaded  			| 	Total number of classes that have been loaded since the JVM has started execution
Classes Unloaded  			| 	Total number of classes that have been unloaded since the JVM has started execution
Uptime  				| 	Amount of time the server has been running in seconds

Sample Screenshots:

![image](https://github.com/user-attachments/assets/d10b8819-acea-4523-9fa1-996e4e04e5df)
![image](https://github.com/user-attachments/assets/0d39be76-5724-416c-a90a-2f0cdd5ba7e7)
![image](https://github.com/user-attachments/assets/576f025c-3381-4005-bda2-c51f21026582)


