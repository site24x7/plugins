Plugin for Monitoring Kong 
==============================================

Kong is API gateway with enterprise functionality. As part of Kong Konnect, the gateway brokers an organization’s information across all services by allowing customers to manage the full lifecycle of services and APIs. On top of that, it enables users to simplify the management of APIs and microservices across hybrid-cloud and multi-cloud deployments.

Follow the below steps to configure the Kong plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Apache Kong service instances.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---
##### Linux 

- Create a folder "kong".

		mkdir kong
  		cd kong/

- Download all the files in "kong" folder and place it under the "kong" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/kong/kong.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/kong/kong.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the kong.py script.
	
- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python kong.py --host_name "localhost" --port "8001" --service_name "service-name"
		
- Change the below configurations in "kong.cfg":

		[display_name]
		host_name=“host_ip_or_domain”
		port=“8001”
		service_name="service_name"
		
- Move the folder "kong" under Site24x7 Linux Agent plugin directory : 

		mv kong /opt/site24x7/monagent/plugins/


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Captured

Name		            	| Description		            	| Unit
---         		   	|   ---					| ---
connections_waiting | metric calculates the current number of idle client connections waiting for a request. | [connection]
connections_accepted | metric calculates the total number of accepted client connections. | [connection]
connections_handled | metric calculates the total number of handled connections. Generally, the parameter value is the same as accepts unless some resource limits have been reached. | [connection]
connections_active | metric calculates the acurrent number of active client connections including Waiting connections. | [connection]
connections_reading | metric calculates the current number of connections where Kong is reading the request header.  | [connection]
total_requests | metric calculates the total number of client requests. | [connection]
connections_writing | metric calculates the current number of connections where nginx is writing the response back to the client. | [connection]	
kong_bandwidth.egress | metric calculates the total bandwidth (egress->upload) in bytes consumed by the service in Kong. | [byte]
kong_bandwidth.ingress | metric calculates the total bandwidth (ingress->download) in bytes consumed by the service in Kong. | [byte]
kong_datastore_reachable | metric shows whether the kong server datastore is reachable or not (SAFE/CRITICAL).  | [connectivity]
kong_http_status | metric shows the status code for customer per service/route in Kong. | [code]
kong_latency_bucket.kong | metric calculates the latency bucket added by kong latnecy for each service/route in Kong. | [millisecond]
kong_latency_bucket.request | metric calculates the latency bucket added by request latnecy for each service/route in Kong. | [millisecond]
kong_latency_bucket.upstream | metric calculates the latency bucket added by upstream latnecy for each service/route in Kong. | [millisecond]
kong_latency_count.kong | metric calculates the latency count added by kong latnecy for each service/route in Kong. | [millisecond]		
kong_latency_count.request | metric calculates the latency count added by request latnecy for each service/route in Kong. | [millisecond]
kong_latency_count.upstream | metric calculates the latency count added by upstream latnecy for each service/route in Kong. | [millisecond]
kong_latency_sum.kong | metric calculates the latency sum added by kong latnecy for each service/route in Kong. | [millisecond]
kong_latency_sum.request | metric calculates the latency sum added by request latnecy for each service/route in Kong. | [millisecond]
kong_latency_sum.upstream | metric calculates the latency sum added by upstream latnecy for each service/route in Kong. | [millisecond]		
---
