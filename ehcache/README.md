Plugin for Ehcache Monitoring
===========

Ehcache is the most widely-used Java based cache service. Configure Site24x7 Ehcache monitoring plugin and monitor the performance of your caches.

Get to know how to configure the Ehcache plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Ehcache servers.

Learn more https://www.site24x7.com/plugins/ehcache-monitoring.html

## Prerequisites:
- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Latest version of java.
- For monitoring Ehcache, your application must register CacheStatistics in the JDK platform MBeanServer. Below is the sample code for how to register MBeanServer:
    ```
    CacheManager manager = new CacheManager();
    MBeanServer mBeanServer = ManagementFactory.getPlatformMBeanServer();
    ManagementService.registerMBeans(manager, mBeanServer, false, false, false, true);
    ```
- JMX creates a standard way of instrumenting classes which makes them available to a monitoring infrastructure. To enable JMX, please execute the below arguments in your application:
    ```
    Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9999
    Dcom.sun.management.jmxremote.ssl=false
    Dcom.sun.management.jmxremote.authenticate=false
    ```


## Ehcache plugin installation:

- Create a directory "ehcache", under the Site24x7 Linux agent's plugin directory - /opt/site24x7/monagent/plugins/
    ```
    cd /opt/site24x7/monagent/plugins/
    sudo mkdir ehcache
    ```
- Download the files "ehcache.sh" and "EhcachePlugin.java" from our GitHub repository and place it under the "ehcache" directory
    ```
    cd ehcache
    wget https://raw.githubusercontent.com/site24x7/plugins/master/ehcache/ehcache.sh
    wget https://raw.githubusercontent.com/site24x7/plugins/master/ehcache/EhcachePlugin.java
    ```
### Ehcache plugin configuration:
- Check the location of the java by using the following command.
     ```
    which java
    ```
- Edit the below line in ehcache.sh if the path to java is different.
    ```
    export JAVA_HOME="/usr/bin/java"
    ```
- Configure host and port values for the Ehcache plugin Eg :

    ```
    HOST = "localhost"
    ADMINPORT = "4848"
    USERNAME = None
    PASSWORD = None
    ```
- Save the changes and restart the agent.
    ```
    /etc/init.d/site24x7monagent restart
    ```
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

