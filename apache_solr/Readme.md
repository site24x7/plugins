Plugin for monitoring the Apache Solr 
==============================================

This plugin monitors the collection of detailed performance-oriented metrics throughout the life cycle of Solr service and its various components.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "JPype" python library. This module is used to execute the jmx query and get data. Execute the below command to install python JPype modeule in your server.  

		pip install JPype1
		
- JMX connection should be enabled in the Apache Solr installation folder. To enable the JMX connection follow the below steps: Open bin/solr.in.sh inside the installation folder of Apache Solr and change the following attributes

		ENABLE_REMOTE_JMX_OPTS=”true”
		RMI_PORT=18983
		

### Plugin installation
---
##### Linux 

- Create a directory "solr" under Site24x7 Linux Agent plugin directory : 

      Linux             ->   /opt/site24x7/monagent/plugins/apache_solr

##### Windows 

- Create a directory "solr" under Site24x7 Windows Agent plugin directory : 

      Windows           ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\apache_solr
      
---

- Download all the files in "solr" folder and place it under the "solr" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/apache_solr/apache_solr.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/apache_solr/apache_solr.cfg
	
- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python apache_solr.py --host_name=localhost --port=18983 --domain_name=<your_domain_name>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations
---
	[display_name]
	host_name = “<your_host_name>”
	port = “18983”
	domain_name = “<your_domain_name>”

### Metrics Captured
---
	document_cache_evictions -> metric calculate the number of cache evictions across document caches since this node has been running in your Apache Solr Setup. [eviction]

	document_cache_hits -> metric calculate the number of cache hits across document caches since this node has been running in your Apache Solr Setup. [hit]

	document_cache_inserts -> metric calculate the number of cache insertions across document caches since this node has been running in your Apache Solr Setup. [set]

	document_cache_lookups -> metric calculate the number of cache lookups across document caches since this node has been running in your Apache Solr Setup. [get]

	filter_cache_evictions -> metric calculate the number of cache evictions across filter caches since this node has been running in your Apache Solr Setup. [eviction]

	filter_cache_hits -> metric calculate the number of cache hits across filter caches since this node has been running in your Apache Solr Setup. [hit]

	filter_cache_inserts -> metric calculate the number of cache insertions across filter caches since this node has been running in your Apache Solr Setup. [set]

	filter_cache_lookups -> metric calculate the number of cache lookups across filter caches since this node has been running in your Apache Solr Setup. [get]

	query_result_cache_evictions -> metric calculate the number of cache evictions across query result caches since this node has been running in your Apache Solr Setup. [eviction]

	query_result_cache_hits -> metric calculate the number of cache hits across query result caches since this node has been running in your Apache Solr Setup. [hit]

	query_result_cache_inserts -> metric calculate the number of cache insertions across query result caches since this node has been running in your Apache Solr Setup. [set]

	query_result_cache_lookups -> metric calculate the number of cache lookups across query result caches since this node has been running in your Apache Solr Setup. [get]

	query_request_times_50thpercent -> metric calculate the request processing time for the request which belongs to the 50th Percentile. E.g., if 100 requests are received, then the 50th fastest request time will be reported by this statistic. [request]

	query_request_times_75thpercent -> metric calculate the request processing time for the request which belongs to the 75th Percentile. E.g., if 100 requests are received, then the 75th fastest request time will be reported by this statistic. [request]

	query_request_times_95thpercent -> metric calculate the request processing time for the request which belongs to the 95th Percentile. E.g., if 100 requests are received, then the 95th fastest request time will be reported by this statistic. [request]

	query_request_times_98thpercent -> metric calculate the request processing time for the request which belongs to the 98th Percentile. E.g., if 100 requests are received, then the 98th fastest request time will be reported by this statistic. [request]

	query_request_times_99thpercent -> metric calculate the request processing time for the request which belongs to the 99th Percentile. E.g., if 100 requests are received, then the 99th fastest request time will be reported by this statistic. [request]

	query_request_times_999thpercent -> metric calculate the request processing time for the request which belongs to the 99.9th Percentile. E.g., if 1000 requests are received, then the 999th fastest request time will be reported by this statistic. [request]

	query_request_times_mean -> metric calculate the mean of all the request processing time since this node has been running in your Apache Solr Setup. [request/second]

	query_request_times_mean_rate -> metric calculate the average number of requests received per second since the Solr core was first created in your Apache Solr Setup. [request/second]

	query_request_times_oneminuterate -> metric calculate the number of requests per second received over the past one minute since this node has been running in your Apache Solr Setup. [request/second]
	
	searcher_maxdoc -> metric calculate the number of updates that have occurred since the last commit in your Apache Solr Setup. [document]

	searcher_numdocs -> metric calculate the total number of indexed documents that can be searched in your Apache Solr Setup. [document]

	searcher_warmup_time -> metric calculate the total time spent on warming up the cache by pre-populating some cache items in your Apache Solr Setup. [millisecond]
	
	query_requests -> metric calculate the total number of requests per second processed by the query handler. [request]
	
	query_timeouts -> metric calculate the total number of responses per second received with partial results. [request]
	
	query_time -> metric calculate the sum of all requests processing times. [millisecond]
	
	query_errors -> metric calculate the number of errors per second encountered by the handler. [erroe]
