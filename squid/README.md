Plugin for Squid Proxy Monitoring 
==============================================

Squid Proxy is a fully-featured HTTP/1.0 proxy which is almost a fully-featured HTTP/1.1 proxy. Squid offers a rich access control, authorization and logging environment to develop web proxy and content serving applications. Squid offers a rich set of traffic optimization options, most of which are enabled by default for simpler installation and high performance.

Follow the below steps to configure the Kong plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Apache Kong service instances.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---

- Create a folder "squid".

- Download all the files in "squid" folder and place it under the "squid" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/squid/squid.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/squid/squid.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the squid.py script.
	
- Configure the keys to be monitored, as mentioned below in "squid.cfg"

		[display_name]
		host_name=“your_host_ip”
		port=“3128”

- Execute the below command with appropriate arguments to check for the valid json output.  

		python squid.py --host_name "localhost" --port "3128"

##### Linux 

- Move the folder "squid" under Site24x7 Linux Agent plugin directory : 

      Linux            ->   /opt/site24x7/monagent/plugins/

##### Windows 

- Move the folder "squid" under Site24x7 Windows Agent plugin directory : 

      Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
      
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Captured
---
	client_http.requests -> metric calculates the number of HTTP requests received from clients. [request]

	client_http.hits -> metric calculates the number of cache hits in response to client requests. [hit]

	client_http.errors -> metric calculates the number of client transactions that resulted in an error. [error]

	client_http.kbytes_in -> metric calculate the amount of traffic received from clients in their requests. [kibibyte]

	client_http.kbytes_out -> metric calculate the amount of traffic sent to clients in responses. [kibibyte]

	client_http.hit_kbytes_out -> metric calculate the amount of traffic sent to clients in responses that are cache hits. [kibibyte]

	server.all.requests -> metric calculate the number of requests forwarded to origin servers (or neighbor caches) for all server-side protocols. [request]
	
	server.all.errors -> metric calculate the number of server-side requests (all protocols) that resulted in some kind of error. [error]

	server.all.kbytes_in -> metric calculate the amount of traffic read from the server-side for all protocols. [kibibyte]

	server.all.kbytes_out -> metric calculate the amount of traffic written to origin servers and/or neighbor caches for server-side requests. [kibibyte]

	server.http.requests -> metric calculate the number of server-side requests to HTTP servers, including neighbor caches. [request]

	server.http.errors -> metric calculate the number of server-side HTTP requests that resulted in an error. [error]

	server.http.kbytes_in -> metric calculate the amount of traffic read from HTTP origin servers and neighbor caches. [kibibyte]

	server.http.kbytes_out -> metric calculate the amount of traffic written to HTTP origin servers and neighbor caches. [kibibyte]

	server.ftp.requests -> metric calculate the number of requests sent to FTP servers. [request]		

	server.ftp.errors -> metric calculates the number of requests sent to FTP servers that resulted in an error. [error]

	server.ftp.kbytes_in -> metric calculate the amount of traffic read from FTP servers, including control channel trafficp. [kibibyte]

	server.ftp.kbytes_out -> metric calculate the amount of traffic written to FTP servers, including control channel traffic. [kibibyte]

	server.other.requests -> metric calculate the number of "other" server-side requests. Currently, the other protocols are Gopher, WAIS, and SSL. [request]

	server.other.errors -> metric calculate the number of Gopher, WAIS, and SSL requests that resulted in an error. [error]
	
	server.other.kbytes_in -> metric calculate the amount of traffic read from Gopher, WAIS, and SSL servers. [kibibyte]

	server.other.kbytes_out -> metric calculate the amount of traffic written to Gopher, WAIS, and SSL servers. [kibibyte]

	unlink.requests -> metric calculate the number of unlink requests given to the (optional) unlinkd process. [request]

	page_faults -> metric calculate the number of (major) page faults as reported by getrusage( ). [fault]

	aborted_requests -> metric calculate the number of server-side HTTP requests aborted due to client-side aborts. [request]
