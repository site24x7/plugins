@echo off

set PLUGIN_VERSION="1"
set HEARTBEAT_REQUIRED="true"
set HOST=""
set PORT=""
set USERNAME=""
set PASSWORD=""
set JAVA_HOME="C:\Program Files\Java\jdk1.8.0_241\bin"

set SCRIPT_DIR=%~dp0
set PLUGIN_PATH=%SCRIPT_DIR:~0,-1%

set CLASS_PATH="%PLUGIN_PATH%\json-20140107.jar";"%PLUGIN_PATH%\jconn4.jar"

%JAVA_HOME%\javac -Xlint:deprecation -cp %CLASS_PATH% -d "%PLUGIN_PATH%" "%PLUGIN_PATH%\sybaseDB.java"
%JAVA_HOME%\java -cp %CLASS_PATH%;"%PLUGIN_PATH%" sybaseDB %PLUGIN_VERSION% %HEARTBEAT_REQUIRED% %HOST% %PORT% %USERNAME% %PASSWORD%

set data = %( "%JAVA_HOME%\java" -cp %CLASS_PATH% "sybaseDB" %PLUGIN_VERSION% %HEARTBEAT_REQUIRED% %HOST% %PORT% %USERNAME% %PASSWORD%)%

echo %data%
