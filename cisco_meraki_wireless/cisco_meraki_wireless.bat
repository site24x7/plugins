@echo off
set APIKEY="5075a9e1a4e3bcb5f741cce382f85d84f9e87fa5"
set NETWORKID="L_123456"
set BASEURL="https://api.meraki.com/api/v0"
set POLL_INTERVAL="5"
set PLUGIN_VERSION="1"
set HEARTBEAT_REQUIRED="true"

set JAVA_HOME="C:\Program Files\Java\jdk1.8.0_241\bin"

set PLUGIN_FOLDER_NAME=cisco_meraki_wireless

set PLUGIN_PATH=C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\%PLUGIN_FOLDER_NAME%

set CLASS_PATH="%PLUGIN_PATH%\json.jar";"%PLUGIN_PATH%\httpcore-4.4.10.jar";"%PLUGIN_PATH%\httpclient-4.5.6.jar";"%PLUGIN_PATH%\commons-codec-1.10.jar";"%PLUGIN_PATH%\commons-logging-1.2.jar"

%JAVA_HOME%\javac -cp %CLASS_PATH% -d "%PLUGIN_PATH%" "%PLUGIN_PATH%\MerakiDataCollector.java"
%JAVA_HOME%\java -cp %CLASS_PATH%;"%PLUGIN_PATH%" MerakiDataCollector %APIKEY% %NETWORKID% %BASEURL% %POLL_INTERVAL% %PLUGIN_VERSION% %HEARTBEAT_REQUIRED%

set data = %( "%JAVA_HOME%\java" -cp %CLASS_PATH% "MerakiDataCollector" %APIKEY% %NETWORKID% %BASEURL% %POLL_INTERVAL% %TRAFFIC_UNIT% %PLUGIN_VERSION% %HEARTBEAT_REQUIRED% )%

echo %data%
