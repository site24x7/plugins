# Redis Monitoring

## Quick installation

If you're using Linux servers, use the redis plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```
wget https://raw.githubusercontent.com/site24x7/plugins/master/redis/installer/Site24x7RedisPluginInstaller.sh && sudo bash Site24x7RedisPluginInstaller.sh
```
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Execute the following command in your server to install Redis: 

		pip install redis

## Plugin Installation  
- Create a directory named `Redis`.

		mkdir Redis
  		cd Redis/
  
- Download all the files under the `Redis` directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/redis/Redis.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/redis/Redis.cfg



- Execute the below command with appropriate arguments to check for the valid JSON output:

		python Redis.py --host "localhost" --port "6379" --password "" 

- Provide your Redis configurations in Redis.cfg file.

		[redis]
		host = "localhost"
		port = "6379"
		password = ""

  #### Linux
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the Redis.py script.
- Move the `Redis` directory to the Site24x7 Linux Agent plugin directory: 

		mv Redis /opt/site24x7/monagent/plugins/

  #### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.


- Move the folder `Redis` under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


