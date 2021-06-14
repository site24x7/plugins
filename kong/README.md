Plugin for Monitoring Kong 
==============================================

Kong is API gateway with enterprise functionality. As part of Kong Konnect, the gateway brokers an organization’s information across all services by allowing customers to manage the full lifecycle of services and APIs. On top of that, it enables users to simplify the management of APIs and microservices across hybrid-cloud and multi-cloud deployments.

Follow the below steps to configure the Kong plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Apache Kong service instances.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---
##### Linux 

- Create a folder "kong" under Site24x7 Linux Agent plugin directory : 

      Linux            ->   /opt/site24x7/monagent/plugins/kong

---

- Download all the files in "kong" folder and place it under the "kong" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/kong/kong.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/kong/kong.cfg
	
- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python kong.py --host_name=localhost --port=8001 --service_name=<service-name>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations
---
	[display_name]
	host_name=“<your_host_name>”
	port=“8001”
	service_name="<service_name"

### Metrics Captured
---
	connections_waiting -> metric calculate the current number of connections where nginx is writing the response back to the client. [connection]

	connections_accepted -> metric calculates the total number of accepted client connections. [connection]

	connections_handled -> metric calculates the total number of handled connections. Generally, the parameter value is the same as accepts unless some resource limits have been reached. [connection]

	connections_active -> metric calculate the acurrent number of active client connections including Waiting connections. [connection]

	connections_reading -> metric calculate the current number of connections where Kong is reading the request header. [connection]

	total_requests -> metric calculate the total number of client requests. [connection]

	connections_writing -> metric calculate the current number of connections where nginx is writing the response back to the client. [connection]
	
	kong_bandwidth.egress -> metric calculate the total bandwidth (egress->upload) in bytes consumed by the service in Kong [byte]

	kong_bandwidth.ingress -> metric calculate the total bandwidth (ingress->download) in bytes consumed by the service in Kong [byte]

	kong_datastore_reachable -> metric shows whether the kong server datastore is reachable or not (SAFE/CRITICAL). [connectivity]

	kong_http_status -> metric shows the status code for customer per service/route in Kong [code]

	kong_latency_bucket.kong -> metric calculate the latency bucket added by kong latnecy for each service/route in Kong. [millisecond]

	kong_latency_bucket.request -> metric calculate the latency bucket added by request latnecy for each service/route in Kong. [millisecond]

	kong_latency_bucket.upstream -> metric calculate the latency bucket added by upstream latnecy for each service/route in Kong. [millisecond]

	kong_latency_count.kong -> metric calculate the latency count added by kong latnecy for each service/route in Kong. [millisecond]		

	kong_latency_count.request -> metric calculate the latency count added by request latnecy for each service/route in Kong. [millisecond]

	kong_latency_count.upstream -> metric calculate the latency count added by upstream latnecy for each service/route in Kong. [millisecond]

	kong_latency_sum.kong -> metric calculate the latency sum added by kong latnecy for each service/route in Kong. [millisecond]

	kong_latency_sum.request -> metric calculate the latency sum added by request latnecy for each service/route in Kong. [millisecond]

	kong_latency_sum.upstream -> metric calculate the latency sum added by upstream latnecy for each service/route in Kong. [millisecond]		
