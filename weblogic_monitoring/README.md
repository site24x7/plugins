# Weblogic Monitoring

## What is Oracle Weblogic Server ?

Oracle Weblogic Server is a unified and scalable platform for developing and deploying enterprise applications like Java. It offers a robust, secure and highly available environment for business-critical applications. 

Monitor the availability and performance of your Weblogic Server with Site24x7's Weblogic Monitoring plugin integration.

## Prerequisites
- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you intend to run the plugin

- Install the jmxquery module for python. 

  ```
  pip install jmxquery
  
  ```
  
- Set up the jmx port for Weblogic.
	- Open the setDomainEnv.sh in the domain folder of the weblogic instance
	- Exporting jmx port **insecurely**
		```
		JAVA_OPTIONS="${JAVA_OPTIONS} -Dcom.sun.management.jmxremote 
			       -Dcom.sun.management.jmxremote.port=9010 
			       -Dcom.sun.management.jmxremote.rmi.port=9010
			       -Dcom.sun.management.jmxremote.host=127.0.0.1
			       -Dcom.sun.management.jmxremote.ssl=false  
			       -Dcom.sun.management.jmxremote.authenticate=false
			       -Dcom.sun.management.jmxremote.local.only=true
			       -Djavax.management.builder.initial=weblogic.management.jmx.mbeanserver.WLSMBeanServerBuilder
			       -Djava.rmi.server.hostname=127.0.0.1"
		
		```
	- For the above configuration the authentication is false, that is there is no username and password required.
	- Exporting jmx port **securely**
		```
		JAVA_OPTIONS="${JAVA_OPTIONS} -Dcom.sun.management.jmxremote 
			       -Dcom.sun.management.jmxremote.port=9010 
			       -Dcom.sun.management.jmxremote.rmi.port=9010
			       -Dcom.sun.management.jmxremote.host=127.0.0.1
			       -Dcom.sun.management.jmxremote.ssl=false  
			       -Dcom.sun.management.jmxremote.authenticate=false
			       -Dcom.sun.management.jmxremote.local.only=true
			       -Djavax.management.builder.initial=weblogic.management.jmx.mbeanserver.WLSMBeanServerBuilder
			       -Djava.rmi.server.hostname=127.0.0.1
			       -Dcom.sun.management.jmxremote.access.file=jmxremote.access
			       -Dcom.sun.management.jmxremote.password.file=jmxremote.password"
		```
	- Please provide the below details appropriately based on the weblogic instance configured
		- jmxremote.port
		- jmxremote.host
		- jmxremote.access.file (jmxremote.access file path)
		- jmxremote.password.file(jmxremote.password file path)
	- Restart the weblogic instance after the following changes
		
	   
		



## Plugin Installation
- Create a directory named "weblogic_monitoring" under the Site24x7 Linux Agent plugin directory:

  ```
	 Linux             ->   /opt/site24x7/monagent/plugins/weblogic_monitoring
  ```

- Download all the files in the "weblogic_monitoring" folder and place it under the "weblogic_monitoring" directory.

 ```
  wget https://raw.githubusercontent.com/site24x7/plugins/master/weblogic_monitoring/weblogic_monitoring.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/weblogic_monitoring/weblogic_monitoring.cfg
 ```
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the weblogic_monitoring.py script.
  
- Execute the following command in your server to install jmxquery
  
  ```
  pip install jmxquery
  ```



## Configurations

**Provide your Weblogic configurations in the weblogic_monitoring.cfg file:**

```
[weblogic_1]
hostname=<HOSTNAME>
port=<PORT NUMBER>
server_name=<SERVER_NAME>
username=<WEBLOGIC PASSWORD>
password=<WEBLOGIC PASSWORD>
logs_enabled=False
log_type_name=None
log_file_path=None
```

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.
Log in to Site24x7 and go to Server > Plugin Integrations > click on the name of the plugin monitor. You will be able to view performance charts and set thresholds for the various performance metrics.

## Metrics:
- **Open Sockets Current Count:**

  The current number of sockets registered for socket muxing on the server.
- **Open Socket Total Count:**

  The total number of sockets registered for socket muxing on the server.
- **Thread Pool Percent Socket Readers:**

  The percentage of execute threads from the default queue that can be used as socket readers.
- **Max Open Sock Count:**

  The maximum number of open sockets allowed in the server at a given point of time.
- **Completed Request Count:**

  The number of completed requests in the priority queue.

- **Execute Thread Idle Count:**

  The number of idle threads in the pool. This count does not include standby threads and stuck threads. The count indicates threads that are ready to pick up new work when it arrives.
- **Execute Thread Total Count:**

  The total number of available threads in the pool.
- **Pending User Request Count:** 

  The number of pending user requests in the priority queue. The priority queue contains requests from internal subsystems and users. This is just the count of all user requests.
- **Hogging Thread Count:** 

  The threads that are being held by a request at the time of submission.
-  **Rejected Requests Count:** 

    The number of requests rejected due to configured Shared Capacity for work managers have been reached.
- **Queue Length:**

  The number of pending requests in the priority queue. This is the total of internal system requests and user requests.
- **Shared Capacity For Work Managers:** 

  The maximum amount of requests that can be accepted in the priority queue.
- **Standby Thread Count:** 

  The number of threads in the standby pool. Threads that are not needed to handle the present workload are designated as standby and added to the standby pool. These threads are activated when more threads are needed.

- **Stuck Thread Count:** 

  The number of stuck threads in the thread pool.
- **Thread Pool Runtime Throughput:**

  The mean number of requests completed per second.
- **JMS Connections Current Count:** 

  The current number of connections to the WebLogic server.
- **JMS Connections Total Count:**

  The total number of connections made to the WebLogic Server since the last reset.
- **JMS Servers Total Count:** 

  The current number of JMS servers that are deployed on the particular WebLogic Server instance.
- **Work Manager Pending Requests:** 

  The number of waiting requests in the queue, including daemon requests.
- **Work Manager Completed Requests:** 

  The number of requests that have been processed, including daemon requests.
- **Work Manager Stuck Thread Count:** 

  The number of threads that are considered to be stuck on the basis of any stuck thread constraints.
- **Bytes Received Count:** 

  The total number of bytes received on this channel.
- **Bytes Sent Count:** 

  The total number of bytes sent on this channel.
- **Messages Received Count:** 

  The number of messages received on this channel.
- **Messages Sent Count:** 

  The number of messages sent on this channel.
- **Process CPU Load:** 

  Process load of the CPU.
- **System CPU Load:** 

  System load of the CPU.
- **Heap Memory Usage:**

  The total heap memory usage.
- **Health State:** 

  The health state of Weblogic.

