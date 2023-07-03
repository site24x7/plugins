# Tomcat MemoryPool Monitoring

                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

#### Linux

- Navigate to the below directory

		/opt/tomcat/conf
		
- Open tomcat-users.xml

- Add the below roles are added to the user.

		<user username="user" password="user" roles="manager-gui,admin-gui"/>
  		<user username="user" password="user" roles="manager-script"/>
  		
- Restart Tomcat server
		
#### Windows

- Navigate to below directory

		<tomcat_dowloaded_directory>\conf
		
- Open tomcat-users.xml
- Add the below roles are added to the user.

		<user username="user" password="user" roles="manager-gui,admin-gui"/>
  		<user username="user" password="user" roles="manager-script"/>
  
- Removing Manager Page restriction. This applies only to Tomcat 8 onward.
  
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

- Restart the Tomcat server after the above changes.
---

### Plugin Installation  

- Create a directory named "tomcat_memorypool".
      
- Download the below files and place them under the "tomcat_memorypool" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/tomcat_memorypool/tomcat_memorypool.py

- Execute the below command with appropriate arguments to check for the valid JSON output:

		python tomcat_memorypool.py
		
---


		
### Move the plugin under the Site24x7 agent

#### Linux

- Move "tomcat_memorypool" directory under the Site24x7 Linux Agent plugin directory: 

		Linux             ->   /opt/site24x7/monagent/plugins/
		
#### Windows

- Move "tomcat_memorypool" directory under the Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
		
The agent will automatically execute the plugin within five minutes and the user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.







