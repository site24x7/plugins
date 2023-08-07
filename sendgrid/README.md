# SendGrid monitoring with Site24x7 plugins

Install and configure the SendGrid plugin to monitor SendGrid’s cloud-based email infrastructure. Take informed troubleshooting decisions by keeping track of critical metrics like the number of emails delivered, unique clicks, the number of requests and lot more.

Know how to configure the SendGrid plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of SendGrid servers -- https://www.site24x7.com/plugins/sendgrid-monitoring.html

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.

---

### Plugin Installation  

- Create a directory named "sendgrid"

- Download the below files and place it under the "sendgrid" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/sendgrid/sendgrid.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/sendgrid/sendgrid.cfg


- Execute the below command with appropriate arguments to check for the valid JSON output:

		python sendgrid.py  --api_key=<api_key>
  
- Then place the configurations in the sendgrid.cfg file.

		[account_1]
		api_key=<api_key>
  
- The agent will automatically read the configurations in the sendgrid.cfg and execute the plugin. And the user can also give multiple configurations. eg:


		[account_1]
		api_key=<api_key>
  
		[account_2]
		api_key=<api_key>

  ##### Note :

  - Each header should have different name. eg: [account_1], [account_2], [account_3], etc,.
  
  #### Linux
  
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the sendgrid.py script.

- Place the "sendgrid" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/sendgrid

  #### Windows 

- Move the folder "sendgrid" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\sendgrid

