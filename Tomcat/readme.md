# Tomcat Monitoring
                                                                                              
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

## Quick installation

If you're using Linux servers, use the Tomcat plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/Tomcat/Installer/Site24x7TomcatPluginInstaller.sh && sudo bash Site24x7TomcatPluginInstaller.sh
```
## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Plugin Installation  

- Create a directory named `Tomcat`.
  
```bash
mkdir Tomcat
cd Tomcat/
```
      
- Download below files and place it under the "Tomcat" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/Tomcat/Tomcat.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/Tomcat/Tomcat.cfg
```

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the Tomcat.py script.

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python Tomcat.py --host='hostname' --port='port' --username='username' --password='password'
```
---

### Configurations

- Provide your tomcat configurations in Tomcat.cfg file.

```bash
[Tomcat]
host = 'localhost'
port = '8080'
username = 'admin'
password = 'admin'
```
		
### Move plugin under Site24x7 agent

#### Linux

- Move "Tomcat" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv Tomcat /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move "Tomcat" directory under the Site24x7 Windows Agent plugin directory:
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

```
Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
