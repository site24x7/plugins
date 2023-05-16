# Plugin for monitoring Atlassian Jira
---

On-Premise Solution for Atlassian Jira

### Prerequisites

* Monitoring data is fetched using JMX Configuration

    * How to enable JMX configuration
    ---
    * Access jira console in a browser and go to settings > System > JMX monitoring and enable JMX monitoring
    * Go to *jira_home*/atlassian-jira-\*.\*.*/bin and open catalina.sh file. For windows, open catalina.bat file.
    * Add these lines

    **For windows:**
    ```
    set JAVA_OPTS=-Dcom.sun.management.jmxremote %JAVA_OPTS%
    set JAVA_OPTS=-Dcom.sun.management.jmxremote.port=8099 %JAVA_OPTS%
    ```
    **For linux:**
    ```
    JAVA_OPTS="-Dcom.sun.management.jmxremote ${JAVA_OPTS}"
    JAVA_OPTS="-Dcom.sun.management.jmxremote.port=8099 ${JAVA_OPTS}"
    ```
    * Go to *JAVA_HOME*/bin directory and run jconsole
    * You can see a service named org.apache.catalina.startup.Bootstrap is running. It denotes your JMX is running properly

    **If you face any problems with the configuration, read the documentation to configure JMX for jira- [Link](https://confluence.atlassian.com/adminjiraserver/live-monitoring-using-the-jmx-interface-939707304.html)**


## Plugin installation

### Linux

* Create a directory "jira".

* Go to the created directory and run the following commands

		wget https://raw.githubusercontent.com/site24x7/plugins/master/jira/jira.sh
		wget https://raw.githubusercontent.com/site24x7/plugins/master/jira/Jira.java
		
* Open jira.sh. Set the values for **HOSTNAME**, **PORT**, **RMI_UNAME**, **RMI_PASSWORD**. If you have not configured any password for JMX, you don't have to change the RMI_UNAME and RMI_PASSWORD fields. The values for RMI_UNAME and RMI_PASSWORD can also be set through environmental variables.

* If the java classpath is not set in your machine, run the commaand- `which java`. Copy the output you get and paste it in the *JAVA_HOME* field and uncomment it. Make sure to paste the path to bin directory and not the path to java
		
* Move the directory "jira" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/

### Windows

* Create a directory "jira".

* Download the files “jira.bat” , “Jira.java” and place it under the “jira” directory

		https://raw.githubusercontent.com/site24x7/plugins/master/jira/jira.sh
		https://raw.githubusercontent.com/site24x7/plugins/master/jira/Jira.java

* Open jira.bat file. Set the values for **HOSTNAME**, **PORT**, **RMI_UNAME**, **RMI_PASSWORD**. If you have not configured any password for JMX, you don't have to change the RMI_UNAME and RMI_PASSWORD fields. The values for RMI_UNAME and RMI_PASSWORD can also be set through environmental variables.

* If the java classpath is not set in your machine, you can uncomment **JAVA_HOME** and **PATH** fields and enter the correct path for the respective fields

* Move the directory "jira" under Site24x7 Windows Agent plugin directory - C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics captured
---
* dashboard.view.count
* db.conns.borrowed
* db.conns.invocation.count
* db.conns.time.to.borrow
* db.conns.total.elapsed.time
* db.reads.invocation.count
* db.reads.total.elapsed.time
* db.writes.invocation.count
* db.writes.total.elapsed.time
* entity.attachments.total
* entity.components.total
* entity.customfields.total
* entity.filters.total
* entity.groups.total
* entity.issues.total
* entity.users.total
* entity.versions.total
* issue.assigned.count
* issue.created.count
* issue.link.count
* issue.search.count
* issue.worklogged.count
* jira.license.jira-core.current.user.count
* jira.license.jira-core.max.user.count
* jira.license.jira-core.max.user.count
* web.requests.invocation.count
* web.requests.total.elapsed.time
