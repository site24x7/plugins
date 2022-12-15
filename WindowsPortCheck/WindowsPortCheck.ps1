param([string]$portNumber, [string]$ipAddress)
$output = @{}

$heartbeat = "true" 
$version=1


function Test-Port
{
    param
    (
        $Address,
        $Port
    )
    try{
        $tcpClient = new-object Net.Sockets.TcpClient
        $outdata=@{}

        try
        {
            $tcpClient.Connect("$Address", $Port)
            $outdata.add("port_status",1)
        }
        catch
        {
            $outdata.add("port_status",0)
        }
        finally
        {
            $tcpClient.Dispose()
        }
        $outdata
    }
    catch{

        $outdata.add("status",0)
        $outdata.add("msg", $Error[0])
        $outdata

    }


}

$output.Add("heartbeat_required", $heartbeat)
$data=Test-Port -Address $ipAddress -Port $portNumber
$output.Add("data", ($data))
$output.Add("plugin_version", $version)

$output | ConvertTo-Json


