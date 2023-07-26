# IBM DB2 Tablespace Monitoring

                                                                                       
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install ibm_db module for python
```
  pip install ibm_db
```
---



### Plugin Installation  

- Create a directory named "ibm_db2_tablespace".
      
- Download all the files in the "ibm_db2_tablespace" folder and place it under the "ibm_db2_tablespace" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_db2/ibm_db2_tablespace/ibm_db2_tablespace.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/ibm_db2/ibm_db2_tablespace/ibm_db2_tablespace.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the ibm_db2_tablespace.py script.
- Execute the below command with appropriate arguments to check for the valid json output:
	```
	 python3 ibm_db2_tablespace.py --host <hostname> --port <port no> --username <username> --password <password> --sample_db <db name> --tbsp_name <tablespace name>
	 ```
 - Move the folder "ibm_db2_tablespace" into the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/ibm_db2_tablespace
		
Since it's a python plugin, to run in windows server please follow the steps in below link, remaining configuration steps are exactly the same. 

  https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers



---

### Configurations

- Provide your IBM DB2 configurations in ibm_db2_tablespace.cfg file.
```
  [ibm_db_2]
  host 		= "<hostname>"
  port 		= "<port>"
  username	= "<username>"
  password 	= "<password>"
  sample_db	= "<sample_db>"
  tbsp_name 	= "<tablespace name>
```	
		
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics
The following metrics are captured :

- **tbsp_name**
    
    Name of the tablespace

- **tbsp_page_size**

    Tablespace page size

- **tbsp_state**

    State of the tablespace 

- **tbsp_total_pages**
    
    Total pages of the tablespace

- **tbsp_usable_pages**

    Number of pages unusable in tablespace

- **tbsp_used_pages**

    Number of pages used in tablespace
