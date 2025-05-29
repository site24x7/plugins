# **HiveMQ Monitoring**

### About
HiveMQ is a powerful and scalable MQTT broker designed for fast, reliable, and secure movement of data between connected devices and enterprise systems. It fully supports the MQTT 3.1.1 and 5.0 protocols, making it ideal for IoT, IIoT, and real-time messaging applications. HiveMQ is built for high availability, horizontal scalability, and advanced monitoring, offering robust support for clustering, security, and integration with enterprise systems.

### Prerequisites

- To enable HiveMQ JMX port

    Find the following code block in the ./bin/run.sh script.

    ```  
    JAVA_OPTS="$JAVA_OPTS \
    -Dcom.sun.management.jmxremote \
    -Dcom.sun.management.jmxremote.port=9010 \
    -Dcom.sun.management.jmxremote.rmi.port=9010 \
    -Dcom.sun.management.jmxremote.local.only=false \
    -Dcom.sun.management.jmxremote.authenticate=false \
    -Dcom.sun.management.jmxremote.ssl=false \
    -Djava.rmi.server.hostname=127.0.0.1"
    
    ```
        
- Restart the hiveMQ after the above changes.


## Quick installation

If you're using Linux servers, use the HiveMQ plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/hiveMQ/installer/Site24x7HiveMQPluginInstaller.sh && sudo bash Site24x7HiveMQPluginInstaller.sh
```

## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

- Install the jmxquery module for Python.
  ```
  pip install jmxquery
  ```

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation
- Create a directory named "hiveMQ" 
  
- Download all the files in the "hiveMQ" folder.
  ```
  wget https://raw.githubusercontent.com/site24x7/plugins/master/hiveMQ/hiveMQ.py && sed -i "1s|^.*|#! $(which python3)|" hiveMQ.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/hiveMQ/hiveMQ.cfg
  ```

- Execute the below command with appropriate arguments to check for the valid json output:
    
        python3 hiveMQ.py --hivemq_host "localhost" --hivemq_jmx_port 9010
    
- After above command with parameters gives expected output, please configure the relevant parameters in the hiveMQ.cfg file.

```
[HiveMQ]
hivemq_host=localhost
hivemq_jmx_port=9010
```

#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the kafka.py script.

- Place the "hiveMQ" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/
  
#### Windows
        
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "hiveMQ" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\

## Supported Metrics
The following metrics are captured by the HiveMQ monitoring plugin:

### Summary

| Metric Name                              | Description                                                              |
|------------------------------------------|--------------------------------------------------------------------------|
| Shared Subscription Cache Hit Rate       | Cache hit rate for shared subscriptions (hits/second).                   |
| Shared Subscription Cache Eviction Count | Number of evictions from the shared subscription cache.                  |
| Shared Subscription Cache Miss Count     | Cache miss count for shared subscriptions.                               |
| Shared Subscription Cache Total Load Time| Total time taken to load cache entries (in microseconds).                |
| Rate Limit Exceeded Count                | Count of operations exceeding rate limits.                               |
| Total Bytes Received                     | Total number of bytes received from clients.                             |
| Total Bytes Sent                         | Total number of bytes sent to clients.                                   |
| Cluster Name Request Retry Count         | Number of retry attempts made when requesting cluster name.              |
| Bytes Sent Per Second                    | Rate at which bytes are sent per second.                                 |
| System CPU Load                          | Current system CPU load as a ratio.                                      |
| System Memory Free                       | Amount of free system memory.                                            |


### Message Traffic

| Metric Name                              | Description                                                      |
|------------------------------------------|------------------------------------------------------------------|
| Publish Service Publishes                | MQTT publish message operations for Publish Service Publishes.   |
| Publish Service Publishes to Client      | MQTT publish message operations for Publish Service Publishes to Client. |
| Dropped Messages Total                   | Number of MQTT messages for Dropped Messages Total.              |
| Dropped Messages - Queue Full            | Number of MQTT messages for Dropped Messages - Queue Full.       |
| Dropped Messages - QoS 0 Memory Exceeded | Number of MQTT messages for Dropped Messages - QoS 0 Memory Exceeded. |
| Dropped Messages - Internal Error        | Number of MQTT messages for Dropped Messages - Internal Error.   |
| Expired Messages Count                   | Number of MQTT messages that expired before delivery.            |
| Incoming CONNECT Messages                | Number of incoming CONNECT messages from clients.                |
| Incoming PINGREQ Messages                | Number of incoming PINGREQ messages from clients.                |
| Incoming SUBSCRIBE Messages              | Number of incoming SUBSCRIBE messages from clients.              |
| Incoming UNSUBSCRIBE Messages            | Number of incoming UNSUBSCRIBE messages from clients.            |
| Incoming PUBLISH Messages                | Number of incoming PUBLISH messages from clients.                |
| Incoming Total Message Count             | Total number of all incoming messages.                           |
| Outgoing CONNACK Messages                | Number of outgoing CONNACK messages to clients.                  |
| Outgoing PINGRESP Messages               | Number of outgoing PINGRESP messages to clients.                 |
| Outgoing PUBACK Messages                 | Number of outgoing PUBACK messages to clients.                   |
| Outgoing PUBCOMP Messages                | Number of outgoing PUBCOMP messages to clients.                  |
| Outgoing PUBREL Messages                 | Number of outgoing PUBREL messages to clients.                   |
| Outgoing DISCONNECT Messages             | Number of outgoing DISCONNECT messages to clients.               |
| Outgoing Total Message Count             | Total number of all outgoing messages.                           |
| MQTT 3 CONNECT Count                     | Count of MQTT 3 protocol CONNECT messages.                       |
| MQTT 5 CONNECT Count                     | Count of MQTT 5 protocol CONNECT messages.                       |

### System

| Metric Name           | Description                                                 |
|------------------------|-------------------------------------------------------------|
| Licensed CPU Cores     | Number of CPU cores licensed for use by HiveMQ.             |
| Used CPU Cores         | Number of CPU cores currently used by HiveMQ.               |
| System Memory Total    | Total available system memory.                              |

### Connections

| Metric Name                  | Description                                                      |
|------------------------------|------------------------------------------------------------------|
| Keep Alive Disconnect Count  | Count of client disconnections due to keep-alive timeout.        |
| Connection Closures Total    | Total number of closed client connections.                       |
| Active Session               | Number of active client sessions.                                |
| Subscriptions Count          | Total number of subscriptions across all clients.                |
| Bytes Received Per Second    | Rate at which bytes are received per second.                     |
| Total Bytes Sent             | Total number of bytes sent to clients.                           |

### JVM

| Metric Name                    | Description                                                    |
|--------------------------------|----------------------------------------------------------------|
| JVM Heap Memory Used           | Amount of heap memory used by the JVM.                        |
| JVM Heap Memory Max            | Maximum heap memory available to the JVM.                     |
| JVM Non-Heap Memory Used       | Amount of non-heap memory used by the JVM.                    |
| JVM Non-Heap Memory Committed  | Amount of non-heap memory committed by the JVM.               |
| JVM Thread Count               | Current number of JVM threads.                                |
| JVM Thread Peak                | Peak thread count since the JVM started.                      |
| JVM Thread Daemon              | Number of daemon threads in the JVM.                          |

## Sample Images

![image](https://github.com/user-attachments/assets/f6069dce-7051-4495-8332-2b4de39f5855)
