@echo off

set PLUGIN_VERSION="1"
set HEARTBEAT_REQUIRED="true"
set HOST=""
set USERNAME=""
set PASSWORD=""
set JAVA_HOME="C:\Program Files\Java\jdk1.8.0_241\bin"

set PLUGIN_FOLDER_NAME=IBM_iSeries_AS400

set PLUGIN_PATH=C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\%PLUGIN_FOLDER_NAME%

set CLASS_PATH="%PLUGIN_PATH%\json-20140107.jar";"%PLUGIN_PATH%\jt400.jar"

%JAVA_HOME%\javac -cp %CLASS_PATH% -d "%PLUGIN_PATH%" "%PLUGIN_PATH%\As400DataCollector.java"
%JAVA_HOME%\java -cp %CLASS_PATH%;"%PLUGIN_PATH%" As400DataCollector %PLUGIN_VERSION% %HEARTBEAT_REQUIRED% %HOST% %USERNAME% %PASSWORD%

set data = %( "%JAVA_HOME%\java" -cp %CLASS_PATH% "As400DataCollector" %PLUGIN_VERSION% %HEARTBEAT_REQUIRED% %HOST% %USERNAME% %PASSWORD%)%

echo %data%
