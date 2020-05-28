@echo off
cd "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\jira\"
set HOST=127.0.0.1
set PORT=4501
set PLUGIN_VERSION=1
set HEARTBEAT_REQUIRED=true
set RMI_UNAME=
set RMI_PASSWORD=
:: setx JAVA_HOME "C:\Program Files\Java\jdk1.7.0_04"
:: setx PATH %PATH%;"C:\Program Files\Java\jdk1.7.0_04\bin"
javac Jira.java
java Jira %HOST% %PORT% %PLUGIN_VERSION% %HEARTBEAT_REQUIRED%
