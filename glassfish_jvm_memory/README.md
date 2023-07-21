Plugin for GlassFish Monitoring
===========

GlassFish is an open source application server project sponsored by Oracle corporation. Configure Site24x7 plugin to monitor the performance of your GlassFish servers.

Get to know how to configure the different Oracle GlassFish plugins and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of GlassFish servers.

Learn more https://www.site24x7.com/plugins/glassfish-plugin-monitoring.html
## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.

---

### Plugin Installation  

- Create a directory named "sendgrid"

- Download the below files and place it under the "sendgrid" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/glassfish_jvm_memory/glassfish_jvm_memory.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the glassfish_jvm_memory.py script.
  
- Execute the below command with appropriate arguments to check for the valid JSON output:

    python glassfish_jvm_memory.py
