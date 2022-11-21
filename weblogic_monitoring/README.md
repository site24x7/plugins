Weblogic Monitoring

What is Weblogic ?
...........

Prerequisites
Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you intend to run the plugin
Install the jmxquery module for python. pip install jmxquery
Set up the jmx port for Weblogic





Metrics:

Open Sockets Current Count
The current number of sockets registered for socket muxing on this server.

Open Socket Total Count
The total number of sockets registered for socket muxing on this server.

Thread Pool Percent Socket Readers
The percentage of execute threads from the default queue that can be used as socket readers.

Max Open Sock Count
The maximum number of open sockets allowed in server at a given point of time.

Completed Request Count
The number of completed requests in the priority queue.

Execute Thread Idle Count
The number of idle threads in the pool. This count does not include standby threads and stuck threads. The count indicates threads that are ready to pick up new work when it arrives.

Execute Thread Total Count
The total number of threads in the pool.

Pending User Request Count
The number of pending user requests in the priority queue. The priority queue contains requests from internal subsystems and users. This is just the count of all user requests.


Hogging Thread Count
The threads that are being held by a request at the time of submission.
Overload Rejected Requests Count
Number of requests rejected due to configured Shared Capacity for work managers have been reached.


Queue Length
The number of pending requests in the priority queue. This is the total of internal system requests and user requests.

Shared Capacity For Work Managers
Maximum amount of requests that can be accepted in the priority queue.

Standby Thread Count
The number of threads in the standby pool. Threads that are not needed to handle the present work load are designated as standby and added to the standby pool. These threads are activated when more threads are needed.

Stuck Thread Count
Number of stuck threads in the thread pool.

Thread Pool Runtime Throughput
The mean number of requests completed per second.

JMS Connections Current Count
The current number of connections to WebLogic Server.

JMS Connections Total Count
The total number of connections made to this WebLogic Server since the last reset.

JMS Servers Total Count
The current number of JMS servers that are deployed on this WebLogic Server instance.

Work Manager Pending Requests
The number of waiting requests in the queue, including daemon requests.

Work Manager Completed Requests
The number of requests that have been processed, including daemon requests.

Work Manager Stuck Thread Count
The number of threads that are considered to be stuck on the basis of any stuck thread constraints.

Bytes Received Count
The total number of bytes received on this channel.

Bytes Sent Count
The total number of bytes sent on this channel.

Messages Received Count
The number of messages received on this channel.

Messages Sent Count
The number of messages sent on this channel.

Process CPU Load
Process load of CPU

System CPU Load
System load of CPU

Heap Memory Usage
Total heap memory usage

Health State
Health State of Weblogic






