Plugin for Elasticsearch Monitoring
===========

Install and configure the Elasticsearch plugin to monitor the open source, distributed document store and search engine. It depends strongly on Apache Lucene, a full text search engine in Java. Keep a pulse on the performance of the Elasticsearch environment to ensure you are up to date with the internals of your working cluster.

Get to know how to configure the Elasticsearch plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Elasticsearch clusters 

Learn more https://www.site24x7.com/plugins/elasticsearch-monitoring.html

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

---


### Plugin Installation  

- Create a directory named "elasticsearchnodes".
- Download all the files in the "elasticsearchnodes" folder and place it under the "elasticsearchnodes" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearchnodes/elasticsearchnodes.cfg
		wget https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearchnodes/elasticsearchnodes.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the elasticsearchnodes.py script.
		
- Since it's a python plugin, to run in windows server please follow the steps given [here](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers), remaining configuration steps are exactly the same. 


- Execute the below command with appropriate arguments to check for the valid json output:

		python3 elasticsearchnodes.py --host=<host name> --port=<port no> --node_name=<node name> --username=<elasticsearchnodes username> --password=<elasticsearchnodes password>

### Configurations

- Provide your elasticsearchnodes configurations elasticsearchnodes.cfg file.
```
[elasticsearchcluster]
host= <ELASTICSEARCH_HOST>
port= <ELASTICSEARCH_PORT>
username= <ELASTICSEARCH_USERNAME>
password= <ELASTICSEARCH_PASSWORD>
NODE=<ELASTICSEARCH_NODE_NAME>
```	

- Move the directory "elasticsearchnodes" under the Site24x7 Linux Agent plugin directory: 

		Linux       ->  /opt/site24x7/monagent/plugins/elasticsearchnodes
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---


