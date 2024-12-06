Plugin for Monitoring the Internet speed 
========================================

### PreRequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "speedtest" python module.
	
- How to install speedtest :
  
      python2:    python -m pip install --upgrade pip speedtest-cli
      python3:    python3 -m pip install --upgrade pip speedtest-cli
      if pip command not present kindly install using the below section

- How to install pip :
      curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
      python get-pip.py

### Plugin installation
---
##### Linux 

- Create a directory "internet_speed_check".

- Download the file "internet_speed_check.py", "internet_speed_check.cfg" and place it under the "internet_speed_check" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/internet_speed_check/internet_speed_check.py
  
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the internet_speed_check.py script.
	
- Execute the below command to check for valid json output

		python internet_speed_check.py
  
- Move the directory "internet_speed_check" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/internet_speed_check

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---

upload - Upload speed of your internet connection

download - Download speed of your internet connection

ping - Reaction time of your internet connection
