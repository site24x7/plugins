# Plugin for Monitoring VPN Host and INTRANET URL

### Plugin installation
---
##### Linux 

- Create a directory "vpn_check" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/vpn_check

- Download the files "vpn_check.py" , "isp.sh" and place it under the "vpn_check" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/vpn_check/vpn_check.py

  wget https://raw.githubusercontent.com/site24x7/plugins/master/vpn_check/isp.sh
	
### Plugin configurations
---

- Configure the VPN host and port to be monitored in the file vpn_check.py

- Configure the url to be monitored in the field 'URL_BEHIND_VPN' in the file vpn_check.py

  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Metrics Captured
---

- VPN status
- URL status
- Response Time of the URL
- ISP Vendor