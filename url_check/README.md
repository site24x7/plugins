# Plugin for Monitoring URL/Website

### Plugin installation
---
##### Linux 

- Create a directory "url_check" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/url_check

- Download the file "url_check.py" and place it under the "url_check" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/url_check/url_check.py
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Plugin configurations
---

- Configure the url(s) to be monitored in the URLS_TO_BE_MONITORED field of url_check.py

- Configure the display name for the url in the URLS_VS_DISPLAY_NAME field of url_check.py


### Metrics Captured
---

- URL status

- Response Time

