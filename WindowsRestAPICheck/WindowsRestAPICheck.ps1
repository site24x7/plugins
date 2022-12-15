param([string]$restApi)
$output = @{}

$heartbeat = "true" 
$version=1


function Test-Rest
{
    param
    (
        $Url
    )
    try{

    $output = @{}

    $response = Invoke-WebRequest -Uri $Url -Method Get
    $output.Add("response_code",$response.StatusCode)
    $output

    }
    catch{

        $outdata.add("status",0)
        $outdata.add("msg", $Error[0])
        $outdata

    }


}

$output.Add("heartbeat_required", $heartbeat)
$data=Test-Rest -Url $restApi
$output.Add("data", ($data))
$output.Add("plugin_version", $version)

$output | ConvertTo-Json


