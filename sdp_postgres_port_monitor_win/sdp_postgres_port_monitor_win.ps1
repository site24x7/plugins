#=======
### This plugin is used for monitoring PostGressql port in windows

#if any impacting changes to this plugin kindly increment the plugin version here.
$pluginVersion = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
$heartbeat="true"
$displayName = "PostGresPortCheckPlugin" #Name of this plugin

$server = "localhost"	#Change this value to host
$port  = "5432"	#Change the port number (5432 by default)
$portStatus  = 1
$msg = ""

try
{
$conn = New-Object System.Net.Sockets.TcpClient($server, $port)
}
catch
{}

if ($conn.Connected) {
    $portStatus  = 1
	$msg = "Successfully connected to the port"
}
else
{
	$portStatus  = 0
	$msg = "Failed to connect to the port"
}

$data = "{""portStatus"":""$portStatus""}"

$toReturn = "{ `"version`" : `"$pluginVersion`",`"heartbeat`" : `"$heartbeat`",`"displayName`" : `"$displayName`",`"msg`" : `"$msg`",`"data`" : $data }"
Write-Host $toReturn 
