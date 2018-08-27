# Plugin for monitoring Apache Solr

Solr is highly reliable, scalable and fault tolerant, providing distributed indexing, replication and load-balanced querying, automated failover and recovery, centralized configuration and more. Solr powers the search and navigation features of many of the world's largest internet sites.

Site24x7 allows the users to monitor solr using apache_solr.py plugin file, by gathering the performance metrics like core size, num of docs present in a core and so on.

# Configure Apache Solr plugin:

apache_solr.py: <https://raw.githubusercontent.com/site24x7/plugins/master/apache_solr/apache_solr.py>

Place the plugin apache_solr.py file in <agent_directory>/plugins/apache_solr/apache_solr.py 

Make sure python exists in the path /usr/bin/python in your server where the plugin is deployed

Edit the port number based on the port where the solr is running -- DEFAULT PORT is 8983

Currently only 25 plugin attributes are supported so if you have many cores in the solr mention any 5 core name in the CORES list or else any five cores will be picked up randomly for monitoring
