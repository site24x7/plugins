Plugin for Oracle DB Monitoring
=====================================

For monitoring the performance metrics of your Oracle DB using Site24x7 Server Monitoring Plugins. Make sure you have the Site24x7 Linux server agent installed to add this plugin and monitor your Oracle database.
  

Prerequisites
=============

Ensure the following modules are installed to connect to the Oracle database:
    
    1. 	oracle-instantclient-basic-linux
	
	2.	oracle-instantclient-sdk-linux
	
    3.  cx_Oracle - python module
	
	In case you do not have the Oracle instant client installed already, you can install it by following the steps below:
	#Installing and configuring Oracle instant client
	================================================
	1. Dependencies
	Install the following packages
		apt-get install python-dev build-essential libaio1
	2. Download instant client for Linux x86-64 
		instantclient-basic-linux.x64-12.2.0.1.0.zip
		instantclient-sdk-linux.x64-12.2.0.1.0.zip  
	(http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html).
	Note: You will be prompted to sign in to download the above files
	
	3. Unzip and extract the downloaded zip files into a folder, and extract the zip files there.
	   for example, in a directory 
		mkdir -p /opt/oracle_client 
		
	4.Add environment variables:
   	   Create a file in /etc/profile.d/oracle.sh and add the following lines
		export ORACLE_HOME=/opt/oracle_client/instantclient_12_2
		export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
		
	   Create a file in /etc/ld.so.conf.d/oracle.conf  and add the following lines
		/opt/oracle_client/instantclient_12_2
	   	
	   Execute the command
		sudo ldconfig
		
		**Note: You need to Log out and log in,after this step for the changes to reflect**

	5. Create a symlink 
		cd $ORACLE_HOME
		ln -s libclntsh.so.12.1 libclntsh.so
		
	6. Install cx_oracle python using pip
		pip install cx_Oracle

Configure the agent plugin
==========================
 
1. Make the following changes in the oracle_tablespace_details.py plugin file:
            
            Change the values of ORACLE_HOST, ORACLE_PORT, ORACLE_USERNAME, ORACLE_PASSWORD and ORACLE_SID to match your configuration.
            TABLESPACE_NAME - Enter the name of the TABLESPACE you want to monitor. oracle_tablespace_details plugin collects information specific 
            to a Tablespace mentioned in the "TABLESPACE_NAME" of the config section in the script.
2. To add the oracle_tablespace_details.py plugin to the Site24x7 Linux agent,
            
        1) Go to the agent's installation directory
		        cd /opt/site24x7/monagent/plugins/
	    2) Create a folder named oracle_tablespace_details
		        mkdir oracle_tablespace_details
	    3) Copy the plugin to this folder. (Note: The folder name and the plugin name should be the same)
3. The plugin will be added to Site24x7 automatically. This may take less than five minutes.


#Metrics Collected
===================
		*tablespace_status
		*tablespace_usage_percent %
		*Number of reads in this tablespace
		*writes of reads in this tablespace
		*used_space MB
		*free_space MB
		*free_blocks
		*content - Permanent or Temporary or UNDO
		*logging - Logging or NOLogging

