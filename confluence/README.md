# Plugin for monitoring Atlassian Confluence
---

On-Premise Solution for Atlassian Confluence

### Prerequisites

* Monitoring data is fetched using JMX Configuration

    * How to enable JMX configuration
    ---
        * Go to your *confluence_home*/atlassian-confluence-\*.\*.*/bin directory
        * For windows, open setenv.bat. For linux, open setenv.sh
        * Go to the section where CATALINA_OPTS properties are set and dd these lines at the end

        **For linux:** 
        ```
        CATALINA_OPTS="-Dcom.sun.management.jmxremote ${CATALINA_OPTS}"
        CATALINA_OPTS="-Dcom.sun.management.jmxremote.port=8099 ${CATALINA_OPTS}"
        ```
        **For windows:** 
        ```
        set CATALINA_OPTS=-Dcom.sun.management.jmxremote %CATALINA_OPTS%
        set CATALINA_OPTS=-Dcom.sun.management.jmxremote.port=8099 %CATALINA_OPTS%
        ```
        * Go to *JAVA_HOME*/bin directory and run jconsole
        * You can see a service named org.apache.catalina.startup.Bootstrap is running. It denotes your JMX is running properly
        **If you face any problems with the configuration, read the documentation to configure JMX for confluence- [Link](https://confluence.atlassian.com/doc/live-monitoring-using-the-jmx-interface-150274182.html)**

## Plugin installation

### Linux
* Create a directory "confluence" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/confluence
* Go to the created directory and run the following commands
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/confluence/confluence.sh`
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/confluence/Confluence.java`

### Windows
* Create a directory "confluence" under Site24x7 Linux Agent plugin directory - C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\confluence
* Download the files “confluence.bat” , “Confluence.java” and place it under the “confluence” directory

### Plugin configuration
---
* Open confluence.sh (or) confluence.bat file. Set the values for **HOSTNAME**, **PORT**, **RMI_UNAME**, **RMI_PASSWORD**. If you have not configured any password for JMX, you don't have to change the RMI_UNAME and RMI_PASSWORD fields. The values for RMI_UNAME and RMI_PASSWORD can also be set through environmental variables
* **For linux:**  If the java classpath is not set in your machine, run the commaand- `which java`. Copy the output you get and paste it in the *JAVA_HOME* field and uncomment it. Make sure to paste the path to bin directory and not the path to java
* **For windows:** If the java classpath is not set in your machine, you can uncomment **JAVA_HOME** and **PATH** fields and enter the correct path for the respective fields
### Metrics captured
---
* IndexingStatistics.LastElapsedMilliseconds
* IndexingStatistics.TaskQueueLength
* MailTaskQueue.ErrorQueueSize
* MailTaskQueue.RetryCount
* MailTaskQueue.TasksSize
* RequestMetrics.AverageExecutionTimeForLastTenRequests
* RequestMetrics.CurrentNumberOfRequestsBeingServed
* RequestMetrics.ErrorCount
* RequestMetrics.NumberOfRequestsInLastTenSeconds
* RequestMetrics.RequestsBegan
* RequestMetrics.RequestsServed
* IndexingStatistics.Flushing
* IndexingStatistics.LastReindexingTaskName
* IndexingStatistics.LastStarted
* IndexingStatistics.LastWasRecreated
* IndexingStatistics.ReIndexing
* MailTaskQueue.FlushStarted
* MailTaskQueue.Flushing
