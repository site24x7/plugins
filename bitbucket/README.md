# Plugin for monitoring Atlassian Bit Bucket
---
A plugin to monitoring the Atlassian Bit Bucket on-premises solution

### Prerequisites

* Monitoring data is fetched using JMX Configuration

    * How to enable JMX configuration
    ---
    * Go to your *atlassian_home*/shared directory
    * Open the bitbucket.properties file and add this line: `jmx.enabled=true`. If you are not able to find the bitbucket.properties file, see how to run database migration for bitbucket and try again. After doing this, restart your server
    * Go to your *atlassian_home*/atlassian-bitbucket-\*.\*\.*/bin directory and open set-jmx-opts.sh file. For windows, it is set-jmx-opts.bat
    * Set JMX_REMOTE_PORT=3333. You can use any port number you want. Once you made the change, save the file and close
    * Go to *JAVA_HOME*/bin directory and run jconsole. 
    * You can see a service named org.apache.catalina.startup.Bootstrap is running. It denotes your JMX is running properly

    **If you face any problems with the configuration, read the documentation to configure JMX for Bitbucket- [Link](https://confluence.atlassian.com/bitbucketserver/enabling-jmx-counters-for-performance-monitoring-776640189.html)**

## Plugin installation
___

* Create a directory "bitbucket".
* Go to the created directory and run the following commands
`wget https://raw.githubusercontent.com/site24x7/plugins/master/bitbucket/bitbucket.sh`
`wget https://raw.githubusercontent.com/site24x7/plugins/master/bitbucket/Bitbucket.java`


### Plugin configuration
---
* Open bitbucket.sh (or) bitbucket.bat file. Set the values for **HOSTNAME**, **PORT**, **RMI_UNAME**, **RMI_PASSWORD**. If you have not configured any password for JMX, you don't have to change the RMI_UNAME and RMI_PASSWORD fields. The values for RMI_UNAME and RMI_PASSWORD can also be set through environmental variables
* **For linux:** If the java classpath is not set in your machine, run the commaand- `which java`. Copy the output you get and paste it in the *JAVA_HOME* field and uncomment it. Make sure to paste the path to bin directory and not the path to java
* **For windows:** If the java classpath is not set in your machine, you can uncomment **JAVA_HOME** and **PATH** fields and enter the correct path for the respective fields

* Move the folder "bitbucket" into agent directory.
   
   For Linux
   ```
   /opt/site24x7/monagent/plugins/bitbucket
   ```
   
   For Windows
   ```
   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\bitbucket
   ```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics captured
---
* HttpHostingStatistics.CloneBytesRead
* HttpHostingStatistics.CloneBytesWritten
* HttpHostingStatistics.CloneCacheBypass
* HttpHostingStatistics.CloneCacheHit
* HttpHostingStatistics.CloneRequestCount
* HttpHostingStatistics.FetchBytesRead
* HttpHostingStatistics.FetchBytesWritten
* HttpHostingStatistics.FetchRequestCount
* HttpHostingStatistics.RequestCount
* HttpHostingStatistics.TotalBytesRead
* HttpHostingStatistics.TotalBytesWritten
* MailStatistics.AverageMessageSize
* MailStatistics.LargestMessageSent
* MailStatistics.QueueFullEventCount
* MailStatistics.QueuedMessagesCount
* MailStatistics.QueuedMessagesSize
* MailStatistics.TotalMailDataSent
* MailStatistics.TotalMessagesFailed
* MailStatistics.TotalMessagesSent
* Projects.Count
* Repositories.Count
* ScmStatistics.Pulls
* ScmStatistics.Pushes
* MailStatistics.LastMessageFailure
* MailStatistics.LastMessageSuccess
* MailStatistics.LastQueueFullEvent
