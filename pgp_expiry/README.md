Plugin for monitoring expiry days for PGP public keys
=====================================================

To monitor the number of days to expire for the public keys in PGP. For more details regarding pgp key configurations, please refer https://packaging.ubuntu.com/html/getting-set-up.html

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "python-gnupg driver" python module.

- How to install python-gnupg :

		default:    /usr/bin/python -m pip install python-gnupg
		python2:    python -m pip install python-gnupg
		python3:    python3 -m pip install python-gnupg

For more details on the python-gnupg driver , refer https://pypi.org/project/python-gnupg/#description. If pip command not present kindly install using the below section

- How to install pip :
      curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
      python get-pip.py

### Plugin installation
---
##### Linux 

- Create a directory "internet_speed_check" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/internet_speed_check

- Download the file "internet_speed_check.py" and place it under the "internet_speed_check" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/internet_speed_check/internet_speed_check.py
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations
---

	keys_to_check - the absolute path of file name containing the gpg public keys to check
	key_server - key server name - default : "keyserver.ubuntu.com"
	gpg_location - gpg location - default "/home/local/.gnupg"
	plugin_version = 1
	heartbeat = True

### Metrics Captured
---
    keyname - No of days for expiry from today
