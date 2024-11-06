# EMQX Monitoring

### Prerequisites
- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.6 or higher version should be installed.

### Installation  

- Create a directory named "emqx".
- Install the **requests** python module.
	```
	pip3 install requests
	```

	
- Download the below files in the "emqx" folder and place it under the "emqx" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/emqx/v4/emqx.py && sed -i "1s|^.*|#! $(which python3)|" emqx.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/emqx/v4/emqx.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```bash
       python3 emqx.py --host "hostname" --port "port no" --username "user name" --password "password"
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the emqx.cfg file.
	```
    [emqx]
    host="localhost"
    port="18083"
    username="user"
    password="user"
	```	
#### Linux
- Move the "emqx" directory under the Site24x7 Linux Agent plugin directory: 

	```bash
	mv emqx /opt/site24x7/monagent/plugins/
	```

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further, move the folder "emqx" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\emqx


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.
