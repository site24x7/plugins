# Tomcat Connector Monitoring

- Tomcat Connector is a component that handles communication between the Tomcat server and external clients, such as web browsers or other web servers. 
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

#### Linux

- Navigate to below directory

		/opt/tomcat/conf
		
- Open tomcat-users.xml

- Add below roles are added to the user.

		<user username="user" password="user" roles="manager-gui,admin-gui"/>
  		<user username="user" password="user" roles="manager-script"/>
  		
- Restart tomcat server
		
#### Windows

- Naviagate to below directory

		<tomcat_dowloaded_directory>\conf
		
- Open tomcat-users.xml
- Add below roles are added to the user.

		<user username="user" password="user" roles="manager-gui,admin-gui"/>
  		<user username="user" password="user" roles="manager-script"/>
  
- Removing Manager Page restriction. This applies only for tomcat 8 onward's.
  
	- Open the `context.xml` file.
  	```
  	vi /opt/tomcat/webapps/manager/META-INF/context.xml
   	```
   	- Find the below block of code in context.xml.
  	```
	    <Valve className="org.apache.catalina.valves.RemoteAddrValve"
	     allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" /> 
	    <Manager sessionAttributeValueClassNameFilter="java\.lang\.(?:Boolean|Integer|Long|Number|String)|org\.apache\.catalina\.filters\.Csr>
   	```
   	- And `comment` it.
  	```
   	...
	<Context antiResourceLocking="false" privileged="true" >
	  <CookieProcessor className="org.apache.tomcat.util.http.Rfc6265CookieProcessor"
	                   sameSiteCookies="strict" />
	<!--  <Valve className="org.apache.catalina.valves.RemoteAddrValve"
	         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" /> -->
	  <Manager sessionAttributeValueClassNameFilter="java\.lang\.(?:Boolean|Integer|Long|Number|String)|org\.apache\.catalina\.filters\.Csr>
	</Context>
   	```
   	- Follow the same steps and do the same for **Host Manager**.
   		- ``` vi /opt/tomcat/webapps/host-manager/META-INF/context.xml ```

- Restart tomcat server after the above changes.
---

### Plugin Installation  

- Create a directory named "tomcat_connector".
      
- Download below files and place it under the "tomcat_connector" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/tomcat_connector/tomcat_connector.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/tomcat_connector/tomcat_connector.cfg

- Execute the below command with appropriate arguments to check for the valid json output:

		python tomcat_connector.py --host='hostname' --port='port' --username='username' --password='password'
		
---

### Configurations

- Provide your tomcat configurations in tomcat_connector.cfg file.

		[1]
		host = 'localhost'
		port = '8080'
		username = 'admin'
		password = 'admin'
		
### Move plugin under Site24x7 agent

#### Linux

- Move "tomcat_connector" directory under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/
		
#### Windows

- Move "tomcat_connector" directory under the Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
		
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics Monitored

		Bytes Received
		Bytes Sent
		Error Count
		Name
		Processing Time
		Request Count
		Thread Allowed
		Thread Busy
		Thread Count
		Tomcat Version






