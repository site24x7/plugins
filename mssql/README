
Monitoring Microsoft MSSql in linux environment using site24x7 python plugins

Tested in Ubuntu 16.04, python 2.7, python 3.5

Requirements:
------------
Microsoft SQL Server setup
FreeTDS
UnixODBC
pyodbc


Installation and Configurations
-------------------------------
Microsoft SQL Server setup

Refer: 
https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu
https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-configure-mssql-conf?view=sql-server-2017


FreeTDS
-------

Driver libraries that allows programs to natively talk to Microsoft SQL Server database.

sudo apt-get install -y freetds-bin freetds-common freetds-dev libct4 libsybdb5

Configuration file:  /etc/freetds/freetds.conf :

[SQLDemo]
host = <ip address of the computer running SQL Server>
port = <port>
tds version = 8.0

To test connection:
tsql -S SQLDemo -U <username> -P <password>

UnixODBC
--------
Driver Manager implementation of the ODBC API.

sudo apt-get install -y unixodbc unixodbc-dev unixodbc-bin libodbc1 odbcinst1debian2 tdsodbc php5-odbc

**If getting Problem in above commands in installation of php5-odbc and unixodbc-bin Try below commands to separately install php5-odbc and unixodbc-bin:**
- sudo apt-get install php-odbc
- sudo apt-get install unixodbc-bin=2.3.0-4+b1


Configuration file:  /etc/odbcinst.ini :

[FreeTDS]
Description = TDS driver (Sybase/MS SQL)
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
Setup =  /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
UsageCount = 1

Configuration file:  /etc/odbc.ini :

[SQLDemo]
Description=Datasource Description
Driver=FreeTDS
Database=TESTDB
Servername=SQLDemo


pyodbc
-------

Python Module which uses ODBC to connect to the database. Supports both 2.x and 3.x versions

pip install pyodbc


Creating user and password for plugin:
-------------------------------------
CREATE LOGIN S24X7PLUGIN WITH PASSWORD = 'S24x7PLUGIN';  
GO  
CREATE USER S24X7PLUGIN FOR LOGIN S24X7PLUGIN;  
GO  

Grant Access to the created user:
use [master]
GO
GRANT VIEW SERVER STATE TO S24X7PLUGIN
GO

Attributes Monitored:
Raw counter variables
---------------------
Data File(s) Size (KB)
Percent Log Used
Active Transactions
Log Growths
Log Shrinks
Log Truncations

Processed counter variables
---------------------------
Transactions per sec
Log Cache Hit Ratio
Log Flushes per sec

