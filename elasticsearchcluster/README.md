Plugin for Elasticsearch Monitoring
===========

Install and configure the Elasticsearch plugin to monitor the open source, distributed document store and search engine. It depends strongly on Apache Lucene, a full text search engine in Java. Keep a pulse on the performance of the Elasticsearch environment to ensure you are up to date with the internals of your working cluster.

Get to know how to configure the Elasticsearch plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Elasticsearch clusters.

Learn more https://www.site24x7.com/plugins/elasticsearch-monitoring.html

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

---


### Plugin Installation  

- Create a directory named "elasticsearchcluster".
- Download all the files in the "elasticsearchcluster" folder and place it under the "elasticsearchcluster" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearchcluster/elasticsearchcluster.cfg
		wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearchcluster/elasticsearchcluster.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the elasticsearchcluster.py script.
		
- Since it's a python plugin, to run in windows server please follow the steps given [here](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers), remaining configuration steps are exactly the same. 


- Execute the below command with appropriate arguments to check for the valid json output:

		python3 elasticsearchcluster.py --host=<host name> --port=<port no> --username=<elasticsearchcluster username> --password=<elasticsearchcluster password> 
- Move the directory "elasticsearchcluster" under the Site24x7 Linux Agent plugin directory: 

		Linux       ->  /opt/site24x7/monagent/plugins/elasticsearchcluster
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---

### Configurations

- Provide your elasticsearchcluster configurations elasticsearchcluster.cfg file.
```
[elasticsearchcluster]
host= <ELASTICSEARCH_HOST>
port= <ELASTICSEARCH_PORT>
username= <ELASTICSEARCH_USERNAME>
password= <ELASTICSEARCH_PASSWORD>
```	
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.
