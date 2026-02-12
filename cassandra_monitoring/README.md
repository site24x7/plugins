# Cassandra Monitoring
## What is Cassandra?

Apache Cassandra is an open-source, distributed NoSQL database management system that is built to handle large volumes of data. It is highly scalable and fault-tolerant, offering users high performance and low latency.

### Monitor the health and performance of your Cassandra database with our plugin integration:

#### Prerequisites
-  Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you intend to run the plugin

-  Install the jmxquery module for python.
	```
	pip install jmxquery
	```
-  Set up  the jmx port for Cassandra:

    1.  Open the cassandra-env.sh file from the location "/etc/cassandra"
    
    2.  By default JMX security is disabled in cassandra, to enable it locate following lines of code in *cassandra-env.sh* file.
		    
        ```
         if [ "$LOCAL_JMX" = "yes" ]; then
  		   JVM_OPTS="$JVM_OPTS -Dcassandra.jmx.local.port=$JMX_PORT -XX:+DisableExplicitGC"
         ```

    3.  Add the following lines to the else block of the above lines in the cassandra-env.sh file
    
        ```
         JVM_OPTS="$JVM_OPTS -Dcassandra.jmx.remote.login.config=CassandraLogin"'
         JVM_OPTS="$JVM_OPTS -Djava.security.auth.login.config=$CASSANDRA_HOME/conf/cassandra-jaas.config"
         JVM_OPTS="$JVM_OPTS -Dcassandra.jmx.authorizer=org.apache.cassandra.auth.jmx.AuthorizationProxy"
         ```
         

    4. Also, comment out the following lines in the cassandra-env.sh file:
        ```
        JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.password.file=/etc/cassandra/jmxremote.password"
        JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.access.file=/etc/cassandra/jmxremote.access"
        ```

    5.  Change the authentication in the cassandra.yaml file to PasswordAuthenticator:

          ```
          authenticator: PasswordAuthenticator
          ```

    6. Change the authorization in the cassandra.yaml file to CassandraAuthorizer:

          ```
          authorizer: CassandraAuthorizer
          ```


    7.  Restart Cassandra once you are done.

#### Plugin Installation

-  Create a directory named "cassandra_monitoring".
    
-  Download all the files in the "cassandra_monitoring" folder and place it under the "cassandra_monitoring" directory.
    ```
    wget https://raw.githubusercontent.com/site24x7/plugins/master/cassandra_monitoring/cassandra_monitoring.py

    wget https://raw.githubusercontent.com/site24x7/plugins/master/cassandra_monitoring/cassandra_monitoring.cfg
    ```

-  Execute the following command in your server to install jmxquery:
    ```
    pip install jmxquery
    ```

-  Execute the below command with appropriate arguments to check fora valid json output:

    ```
     python3 cassandra_monitoring.py --hostname "localhost" --port "7199" --logs_enabled "False"
    ```
    
#### Configurations


-  Provide your Cassandra configurations in the cassandra_monitoring.cfg file.
  
    ```
    [cassandra_1]
    hostname="localhost"
    port="7199"
    logs_enabled="False"
    log_type_name="None"
    log_file_path="None"
    ```
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the cassandra_monitoring.py script.

- Place the "cassandra_monitoring" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/cassandra_monitoring

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

-  Further move the folder "cassandra_monitoring" into the  Site24x7 Windows Agent plugin directory:
    ```
        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\cassandra_monitoring
    ```
    
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

----

### Supported Metrics
The following metrics are captured in the Cassandra monitoring plugin:

### Summary

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Load                        | Total data size on the node in bytes                                   |
| Throughput (Read)           | Number of read requests per second                                     |
| Throughput (Writes)         | Number of write requests per second                                    |

### Latency

| **Metric Name**                           | **Description**                                                        |
|-------------------------------------------|------------------------------------------------------------------------|
| Read Latency 75th Percentile              | 75th percentile of read request latency in microseconds                |
| Read Latency 95th Percentile              | 95th percentile of read request latency in microseconds                |
| Read Latency 99th Percentile              | 99th percentile of read request latency in microseconds                |
| Write Latency 75th Percentile             | 75th percentile of write request latency in microseconds               |
| Write Latency 95th Percentile             | 95th percentile of write request latency in microseconds               |
| Write Latency 99th Percentile             | 99th percentile of write request latency in microseconds               |
| Read Requests One Minute Rate             | Rate of read requests over the last minute                             |
| Write Requests One Minute Rate            | Rate of write requests over the last minute                            |
| Total Latency (Read)                      | Total read response time in microseconds                               |
| Total Latency (Write)                     | Total write response time in microseconds                              |
| Cross Node Latency                        | Time from when a node sends a message until current node receives it   |
| CAS Commit Latency 75th Percentile        | 75th percentile of CAS commit operation latency in microseconds        |
| CAS Commit Latency 95th Percentile        | 95th percentile of CAS commit operation latency in microseconds        |
| CAS Commit One Minute Rate                | Rate of CAS commit operations over the last minute                     |
| CAS Prepare Latency 75th Percentile       | 75th percentile of CAS prepare operation latency in microseconds       |
| CAS Prepare Latency 95th Percentile       | 95th percentile of CAS prepare operation latency in microseconds       |
| CAS Prepare One Minute Rate               | Rate of CAS prepare operations over the last minute                    |
| CAS Propose Latency 75th Percentile       | 75th percentile of CAS propose operation latency in microseconds       |
| CAS Propose Latency 95th Percentile       | 95th percentile of CAS propose operation latency in microseconds       |
| CAS Propose One Minute Rate               | Rate of CAS propose operations over the last minute                    |
| View Lock Acquire Time 75th Percentile    | 75th percentile time to acquire view locks in microseconds             |
| View Lock Acquire Time 95th Percentile    | 95th percentile time to acquire view locks in microseconds             |
| View Lock Acquire One Minute Rate         | Rate of view lock acquisitions over the last minute                    |
| View Read Time 75th Percentile            | 75th percentile of view read operation time in microseconds            |
| View Read Time 95th Percentile            | 95th percentile of view read operation time in microseconds            |
| View Read One Minute Rate                 | Rate of view read operations over the last minute                      |
| Col Update Time Delta 75th Percentile     | 75th percentile of column update time delta in microseconds            |
| Col Update Time Delta 95th Percentile     | 95th percentile of column update time delta in microseconds            |
| Col Update Time Delta Min                 | Minimum column update time delta in microseconds                       |

### Storage

| **Metric Name**                           | **Description**                                                        |
|-------------------------------------------|------------------------------------------------------------------------|
| Live Disk Space Used                      | Disk space used by live SSTables in bytes                              |
| Total Disk Space Used                     | Total disk space used including snapshots in bytes                     |
| Live SSTable Count                        | Number of live SSTables on disk                                        |
| Compression Ratio                         | Compression ratio of data on disk                                      |
| Total Commit Log Size                     | Total size of commit log in bytes                                      |
| Snapshots Size                            | Total size of all snapshots in bytes                                   |
| Compaction Bytes Written                  | Total bytes written by compaction operations                           |
| Bytes Flushed                             | Total bytes flushed from memtables to disk                             |
| Completed Compaction Tasks                | Number of completed compaction tasks                                   |
| Pending Compaction Tasks                  | Number of compaction tasks waiting in queue                            |
| Max Partition Size                        | Maximum partition size in bytes                                        |
| Mean Partition Size                       | Average partition size in bytes                                        |
| Max Row Size                              | Maximum row size in bytes                                              |
| Mean Row Size                             | Average row size in bytes                                              |
| SSTables Per Read 75th Percentile         | 75th percentile of SSTables accessed per read                          |
| SSTables Per Read 95th Percentile         | 95th percentile of SSTables accessed per read                          |
| Tombstone Scanned 75th Percentile         | 75th percentile of tombstones scanned per query                        |
| Tombstone Scanned 95th Percentile         | 95th percentile of tombstones scanned per query                        |
| Bloom Filter False Ratio                  | Ratio of false positives from bloom filters                            |

### Cache

| **Metric Name**                           | **Description**                                                        |
|-------------------------------------------|------------------------------------------------------------------------|
| Key Cache Hit Rate                        | Rate of key cache hits for read requests                               |
| Row Cache Hits                            | Total number of row cache hits                                         |
| Row Cache Misses                          | Total number of row cache misses                                       |
| Row Cache Hit Out Of Range                | Number of row cache hits for out-of-range queries                      |

### Threads

| **Metric Name**                           | **Description**                                                        |
|-------------------------------------------|------------------------------------------------------------------------|
| Active Tasks                              | Number of currently executing tasks in native transport thread pool    |
| Completed Tasks                           | Total number of completed tasks in native transport thread pool        |
| Pending Tasks                             | Number of tasks waiting in queue for native transport thread pool      |
| Currently Blocked Tasks (Transport)       | Number of currently blocked tasks in native transport thread pool      |
| Currently Blocked Tasks                   | Number of currently blocked tasks in memtable flush thread pool        |
| Total Blocked Tasks                       | Total count of blocked tasks in native transport thread pool           |
| Max Pool Size                             | Maximum number of threads in native transport thread pool              |
| Max Tasks Queued                          | Maximum number of tasks that can be queued                             |
| Oldest Task Queue Time                    | Time the oldest task has been waiting in queue in milliseconds         |
| Blocked On Allocation                     | Number of threads blocked waiting for memtable allocation              |
| Dropped Mutations                         | Number of dropped mutation requests                                    |
| Pending Flushes                           | Number of memtable flush operations pending                            |
| Total Hints                               | Number of hint messages written since node start                       |

### Errors

| **Metric Name**                           | **Description**                                                        |
|-------------------------------------------|------------------------------------------------------------------------|
| Exceptions                                | Total number of requests that encountered errors                       |
| Timeout Exceptions (Read)                 | Number of read requests that timed out                                 |
| Timeout Exceptions (Write)                | Number of write requests that timed out                                |
| Unavailable Exceptions (Read)             | Number of read requests with insufficient replicas available           |
| Unavailable Exceptions (Write)            | Number of write requests with insufficient replicas available          |
| Timeout One Minute Rate (Read)            | Rate of read timeouts over the last minute                             |
| Timeout One Minute Rate (Write)           | Rate of write timeouts over the last minute                            |
| Dropped One Minute Rate                   | Rate of dropped mutation messages over the last minute                 |
| ParNew garbage collections (count)        | Number of young-generation garbage collections                         |
| ParNew garbage collections (time)         | Total time spent in young-generation garbage collections in milliseconds|
| CMS garbage collections (count)           | Number of old-generation garbage collections                           |
| CMS garbage collections (time)            | Total time spent in old-generation garbage collections in milliseconds |

## Sample Image

<img width="1654" height="961" alt="image" src="https://github.com/user-attachments/assets/d4185e0c-1c60-4fda-884e-4e1bf5a03d6b" />
