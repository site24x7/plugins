Plugin for PostGres Monitoring
=============================

PostgreSQL is an ORDBMS server whose primary function is to store data securely, and allows retrieval at the request of other software applications. Analyze and optimize your Postgres server by configuring our Postgres plugin and proactively monitor the availability and performance of business-crtical Postgres database server.

Get to know how to configure the PostgreSQL plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Postgres servers.

Learn more https://www.site24x7.com/plugins/postgres-monitoring.html

## Quick installation

If you're using Linux servers, use the postgres plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```
wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/installer/Site24x7PostgresPluginInstaller.sh && sudo bash Site24x7PostgresPluginInstaller.sh
```

### Prerequisites

- Python version 3 or higher.
- Execute the following command in your server to install psycopg2: 

		pip3 install psycopg2-binary

### Plugin Installation  

- Create a directory named "postgres".

		mkdir postgres
  		cd postgres/
  
- Download all the files in the "postgres" folder and place it under the "postgres" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/postgres.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/postgres.cfg

- Execute the following command in your server to install psycopg2: 

		pip3 install psycopg2-binary
  
- Ensure **pg_read_all_stats** permission is provided to the user. For example, create a user 'site24x7' with password 'site24x7' and provide 'pg_read_all_stats' permission to the 'site24x7' user created.
- Execute the below command with appropriate arguments to check for the valid json output:

		python3 postgres.py  --host "ip-address" --port "port-no" --username "username" --password "password" --db "db-name"

- Provide your Postgres DB configurations in postgres.cfg file.

    ```
	[dbname]
    host=localhost
    port=5432
    username=None
    password=None
    db=postgres
    ```
    
  #### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the postgres.py script.
- Move the directory "postgres" under the Site24x7 Linux Agent plugin directory: 

		mv postgres /opt/site24x7/monagent/plugins/
  #### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.


- Move the folder "postgres" under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
