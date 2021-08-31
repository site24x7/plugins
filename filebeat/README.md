Plugin for monitoring Filebeat
==============================================

This plugin monitors the performance of Filebeat.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
		
- Run the following command to install metricbeat on your system
   
- Make sure that elasticsearch and metricbeat are properly installed and configured on your server.

---
## To install and configure metricbeat
- sudo nano /etc/elasticsearch/elasticsearch.yml .
  Add the following lines in the elasticsearch.yml
      
      . . .
      network.host: 0.0.0.0
      . . .
      
- sudo systemctl restart elasticsearch

- sudo apt install metricbeat

- sudo metricbeat setup --template -E 'output.elasticsearch.hosts=["localhost:9200"]'

- sudo systemctl start metricbeat
   
- sudo systemctl enable metricbeat
---
### Plugin Installation

- Create a directory "filebeat" under Site24x7 Linux Agent plugin directory : 

        Linux             ->   /opt/site24x7/monagent/plugins/filebeat
      
- Download all the files in "filebeat" folder and place it under the "filebeat" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/filebeat/filebeat.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/filebeat/filebeat.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python filebeat.py --host=<your_host_name> --port=<port_number>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Configurations

		[filebeat]
		host = <host_name>
		port = <port_number>


### Metrics monitored



		network_name                    ->	 Name of the network
		network_in                      ->	 Total Networks in (bytes)
		network_out                     ->	 Total Networks out (bytes)
		network_in_errors               ->	 Error occured in the networks in (bytes)
		network_out_errors              ->	 Error occured in the networks out (bytes)
		network_out_dropped             ->	 Network drops in out networks (bytes)
		syn_recv                        ->	 Syn received in bytes
		syn_sent                        ->	 Syn sent in bytes
		tcp_closing                     ->	 tcp closing (bytes)
		tcp_count                       ->	 tcp count
		tcp_established                 ->	 tcp established (bytes)
		tcp_listening                   ->	 tcp listening (bytes)
		total_files                     ->	 Total file count
		total_freespace                 ->	 Total free space (bytes)
		total_space                     ->	 Total space available (bytes)
		total_spaceused                 ->	 Total space used (bytes)




