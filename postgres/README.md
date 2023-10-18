Plugin for PostGres Monitoring
=============================

PostgreSQL is an ORDBMS server whose primary function is to store data securely, and allows retrieval at the request of other software applications. Analyze and optimize your Postgres server by configuring our Postgres plugin and proactively monitor the availability and performance of business-crtical Postgres database server.

Get to know how to configure the PostgreSQL plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Postgres servers.

Learn more https://www.site24x7.com/plugins/postgres-monitoring.html

### Plugin Installation  

- Create a directory named "postgres".
- Download all the files in the "postgres" folder and place it under the "postgres" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/postgres.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/postgres/postgres.cfg

- Execute the following command in your server to install psycopg2: 

		pip install psycopg2

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

		/opt/site24x7/monagent/plugins/
  #### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

- Move the folder "postgres" under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
