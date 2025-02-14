param([string]$hostName, [string]$username ,[string]$password,[string]$java_path)

$PLUGIN_VERSION = "1"
$HEARTBEAT_REQUIRED = "true"
$HOSTNAME = $hostName
$USERNAME = $username
$PASSWORD = $password
$JAVA_HOME = $java_path

$PLUGIN_PATH = split-path -parent $MyInvocation.MyCommand.Definition

$CLASS_PATH = "$PLUGIN_PATH\json-20140107.jar;$PLUGIN_PATH\jt400.jar"

# Compile the Java file
& "$JAVA_HOME\javac" -cp $CLASS_PATH -d $PLUGIN_PATH "$PLUGIN_PATH\As400DataCollector.java"

# Run the Java program and capture the output
$data = & "$JAVA_HOME\java" -cp "$CLASS_PATH;$PLUGIN_PATH" As400DataCollector $PLUGIN_VERSION $HEARTBEAT_REQUIRED $HOSTNAME $USERNAME $PASSWORD

# Output the data
Write-Output $data
