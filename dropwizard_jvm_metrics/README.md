Plugin for Dropwizard Monitoring
===========

Dropwizard is a Java framework for developing ops-friendly, high-performance, RESTful web services. Configure Site24x7 plugin to monitor your Dropwizard servers and troubleshoot performance issues as and when they occur.

This document details how to configure the differnt Dropwizard plugins and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Dropwizard servers.

Learn more https://www.site24x7.com/plugins/dropwizard-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "dropwizard_jvm_metrics"

- Download the below files and place it under the "dropwizard_jvm_metrics" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/dropwizard_jvm_metrics/dropwizard_jvm_metrics.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the dropwizard_jvm_metrics.py script.

- Edit the dropwizard_jvm_metrics.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python dropwizard_jvm_metrics.py
  #### Linux

- Place the "dropwizard_jvm_metrics" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/dropwizard_jvm_metrics

  #### Windows 

- Move the folder "dropwizard_jvm_metrics" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\dropwizard_jvm_metrics
