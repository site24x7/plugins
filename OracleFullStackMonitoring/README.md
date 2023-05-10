
# Oracle Full Stack Monitoring
___

## The Oracle Full Stack Monitoring includes the following plugins

- [Oracle Blocking Locks Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OracleBlockingLocks)
- [Oracle Core Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OracleCore)
- [Oracle PDB Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OraclePDB)
- [Oracle Tablespace Details Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OracleTablespaceDetails)
- [Oracle Tablespace Usage Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OracleTablespaceUsage)
- [Oracle Waits Monitoring](https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/OracleWaits)

All the plugins listed are made from the perspective of **Oracle Database Tuning**. By viewing these various plugins and their metrics one can get various insights on how to tune and use their oracle instance efficiently.


## Prerequisites for the Plugins

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Install cx_Oracle module for python
```
  pip3 install cx_Oracle

```
- To install cx_Oracle on windows check this [KBase](https://support.site24x7.com/portal/en/kb/articles/install-and-configure-oracle-plugin-in-windows)
- Roles need to be granted

```
grant select_catalog_role to {username}
```
```
grant create session to {username}
```



## Prerequisites for db's in a cluster

Suppose there are multiple oracle databases in a cluster, in order to grant the above previlieges to all the databases in the cluster the [SetenvPrerequisites.py](https://github.com/site24x7/plugins/blob/master/OracleFullStackMonitoring/SetenvPrerequisites.py) script can be used.

Steps to use the [SetenvPrerequisites.py](https://github.com/site24x7/plugins/blob/master/OracleFullStackMonitoring/SetenvPrerequisites.py) are as follows :

- Download the [SetenvPrerequisites.py](https://github.com/site24x7/plugins/blob/master/OracleFullStackMonitoring/SetenvPrerequisites.py) in the plugin directory of the installed oracle plugin.

- Make sure the ".cfg " file of the plugin is correctly filled for all instances of the oracle plugin.

- Execute the **SetenvPrerequisites.py** file
- Once Excuted the **SetenvPrerequisites.py** will ask for **sysdba username and passsword**, based on the details provided in the ".cfg" file the db will be connected and the necessary previlieges will be granted 

**The cx_Oracle source can be found at : https://github.com/oracle/python-cx_Oracle.**

**Zoho Corporation has made this into one single executable and is licensed under the same [license](https://github.com/oracle/python-cx_Oracle/blob/main/LICENSE.txt) which can be found at: https://github.com/site24x7/plugins/tree/master/OracleFullStackMonitoring/cx_Oracle%20License/License.txt**

