# Plugin for monitoring Cisco Meraki Wireless Controller
---

### Prerequisites
* Make sure you have installed Java installed in your server.
* Collect the **BASEURL** **APIKEY** **NETWORKID** informations using the following link : https://developer.cisco.com/meraki/api/#!getting-started

### Linux
* Create a directory "cisco_meraki_wireless" under Site24x7 Linux Agent plugin directory using the command:
 
    mkdir /opt/site24x7/monagent/plugins/cisco_meraki_wireless

* Download the files "cisco_meraki_wireless.sh" , "MerakiDataCollector.java", "json.jar", "httpcore-4.4.10.jar", "httpclient-4.5.6.jar", "commons-logging-1.2.jar", "commons-codec-1.10.jar" and place it under the "cisco_meraki_wireless" directory using following commands:

     cd /opt/site24x7/monagent/plugins/cisco_meraki_wireless
    
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/cisco_meraki_wireless.sh`
    
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/cisco_meraki_wireless.cfg`
    
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/MerakiDataCollector.java`
    
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/json.jar`
    
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/httpcore-4.4.10.jar`
    
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/httpclient-4.5.6.jar`
    
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/commons-logging-1.2.jar`
    
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/commons-codec-1.10.jar`


### Windows
* Create a directory "cisco_meraki_wireless" under Site24x7 Windows Agent plugin directory - C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\cisco_meraki_wireless
* Download the files "cisco_meraki_wireless.bat" , "MerakiDataCollector.java", "json.jar", "httpcore-4.4.10.jar", "httpclient-4.5.6.jar", "commons-logging-1.2.jar", "commons-codec-1.10.jar" and place it under the "cisco_meraki_wireless" directory
`https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/cisco_meraki_wireless.bat`
`wget https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/cisco_meraki_wireless.cfg`
`https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/MerakiDataCollector.java`
`https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/json.jar`
`https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/httpcore-4.4.10.jar`
`https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/httpclient-4.5.6.jar`
`https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/commons-logging-1.2.jar`
`https://raw.githubusercontent.com/site24x7/plugins/master/cisco_meraki_wireless/commons-codec-1.10.jar`

### Plugin configuration
* Open cisco_meraki_wireless.cfg file and set the values for **APIKEY**, **NETWORKID**, **BASEURL**, **JAVA_HOME**
* Run the commaand- `which java`. Copy the output you get and paste it in the **JAVA_HOME** field. Make sure to paste the path to bin directory and not the path to java.


### Demo mode
* In the file 'MerakiDataCollector.java', change the boolean variable 'IS_DEMO' to true, if you want to simulate random values for testing purposes.
* Setting this to true, will collect Simulated Values instead of collecting actual data.
* Use this for development and testing purposes.

### Developer notes
* To add more metrics, just write another method similar to the ones that already exist and add it to outputJson. 
* Now increment the **PLUGIN_VERSION** value in 'cisco_meraki_wireless.bat' or 'cisco_meraki_wireless.sh' file.
* In the next poll new metrics will be added and can be viewed in the site24x7 client.
* You can find the documentation for configuring Cisco Meraki in [this](https://developer.cisco.com/meraki/api/#!get-organization-api-requests) link.

### Metrics captured
---
* Average Background Traffic
* Average BestEffort Traffic
* Average Video Traffic
* Average Voice Traffic
* Assoc
* Auth
* DHCP
* DNS
* Number of Successful Connections
* Number of Failed Connections
* PollingInterval
* status
* error_message
