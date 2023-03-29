param([string]$SQLServer , [string]$SQLDBName , [string]$query , [string]$sqlusername , [string]$sqlpassword)
$version = 1 #If any changes in the plugin metrics, increment the plugin version here. 
$heartbeat = "true"
$dataObj = @{}
#incase of sql server authentication
$sqlserverauthetication = $false # make it $false for windows authentication
Function Get-Data()
{
        
        $units = @{}
        try{
            $results=Invoke-Sqlcmd -ConnectionString "Data Source=$SQLServer; User Id=$sqlusername; Password =$sqlpassword" -Query "$query"
            $resultlen = $results | Measure-Object | select -ExpandProperty Count
            if($results)
            {
                $isConnectionSuccessful = "Yes"
                $isOutputReturned = "Yes"
                if($resultlen -gt 1)
                {
                    $results=$results[0]
                }
                for($collen=0; $collen -lt $results.Table.Columns.Count; $collen=$collen+1)
                {
                    
                    $dataObj.Add($results.Table.Columns[$collen].ColumnName,$results[$collen]);
                }
            }
            else
	    {
		$isOutputReturned = "No"
		$error = "No error"
               $dataObj.Add("error",$error)
	    }
         }
         catch{
                $isConnectionSuccessful = "No"
                $isOutputReturned = "No"
                $error = "Exception in SQL connection"
                $dataObj.Add("error",$error)
         }
        $dataObj.Add("isOutputReturned",$isOutputReturned)
        $dataObj.Add("isConnectionSuccessful",$isConnectionSuccessful)
        $dataObj.Add("units",$units)
        return 1
	
}
$dataObj.Add("plugin_version", $version)
$dataObj.Add("heartbeat_required", $heartbeat)
$data =Get-Data

$dataObj | ConvertTo-Json
