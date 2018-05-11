#=======
### This plugin is used for checking mail server status in windows

#if any impacting changes to this plugin kindly increment the plugin version here.
$pluginVersion = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
$heartbeat="true"
$displayName = "MailServerStatusCheck" #Name of this plugin

#pop server configurations
$popEnabled = 1 # value 1-pop enabled ; value 0 - pop disabled
$popServer = "popserver"
$popPort = "popport"

#imap server configurations
$imapEnabled = 0 # value 1-imap enabled ; value 0 - imap disabled
$imapServer = "imapserver"
$imapPort = "imapport"

#credentials
$userName = "user@domain.com"
$password = "password"

$imapStatus  = 0
$popStatus = 0
$msg = ""

$invocation = (Get-Variable MyInvocation).Value
$directorypath = Split-Path $invocation.MyCommand.Path

if($popEnabled)
{
#pop
	try
	{
	$dependencypath = $directorypath + '\OpenPop.dll'
	[Reflection.Assembly]::LoadFile($dependencypath) | Out-Null

		$pop = new-object OpenPop.Pop3.Pop3Client
		$pop.Connect($popServer, $popPort, 1);
		$pop.Authenticate($userName,$password,"UsernameAndPassword");
		$popStatus = 1;
		$msg = "Successfully connected to the mail server via POP"
	}
	catch
	{
		$msg = "failed to connect to the mail server via POP"
	}
	$data = "{""popStatus"":""$popStatus""}"
}
ElseIf($imapEnabled)
{
	#imap
	$dependencypath = $directorypath + '\S22Imap\S22.Imap.dll'
	[Reflection.Assembly]::LoadFile($dependencypath) | Out-Null

	try
	{
		$imap = new-object S22.Imap.ImapClient($imapServer,$imapPort,$userName,$password,"Login",1)
		$imapStatus = 1;
		$msg = "Successfully connected to the mail server via IMAP"
	}
	catch
	{
		$msg = "failed to connect to the mail server via IMAP"
	}
	$data = "{""imapStatus"":""$imapStatus""}"
}


$toReturn = "{ `"version`" : `"$pluginVersion`",`"heartbeat`" : `"$heartbeat`",`"displayName`" : `"$displayName`",`"msg`" : `"$msg`",`"data`" : $data }"
Write-Host $toReturn 
