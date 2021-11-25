Plugin for URL Check
==============================================

URL Check plugin monitor the up/down status of the given URL. Collects the response code which can be used to identify the issue in case of URL down. Install and configure the URL Check plugin to monitor how the given URL's are performing, all in a single, intuitive dashboard.

Follow the below steps to configure the URL Check plugin and the monitoring metrics for providing in-depth visibility into the performance and availability stats of URL instances.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 


### Plugin installation
---
##### Linux 

- Create a folder "url_check" under Site24x7 Linux Agent plugin directory : 

      Linux            ->   /opt/site24x7/monagent/plugins/url_check

##### Windows 

- Create a folder "url_check" under Site24x7 Windows Agent plugin directory : 

      Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\url_check
      
---

- Download all the files in "activemq" folder and place it under the "activemq" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/url_check/url_check.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/url_check/url_check.cfg
	
- Configure the URLs to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python url_check.py --url=<your_url>


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations
---
	[display_name]
	url=“<your_url>”

### Metrics Captured
---
	response_time -> metric calculates the time taken request the given URL and get response. [millisecond]

	status_code   -> metric collects the response code which can be used to identify the issue in case of URL down. [code]
