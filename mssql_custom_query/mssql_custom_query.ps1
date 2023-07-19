param([string]$SQLServer , [string]$SQLDBName , [string]$query , [string]$sqlusername , [string]$sqlpassword)
$version = 1 #If any changes in the plugin metrics, increment the plugin version here. 
$heartbeat = "true"
$dataObj = @{}
$mainJson=@{}
#incase of sql server authentication
$sqlserverauthetication = $false # make it $false for windows authentication
Function Get-Data()
{
        
        $units = @{}
        try{
            $results=Invoke-Sqlcmd -ConnectionString "Data Source=$SQLServer; User Id=$sqlusername; Password =$sqlpassword; Initial Catalog=$SQLDBName;TrustServerCertificate=True;Encrypt=False" -Query "$query" -ErrorAction Stop 
            $resultlen = $results | Measure-Object | select -ExpandProperty Count
            $results
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
        $connection.Close()
	    }
         }
         catch{
                $isConnectionSuccessful = "No"
                $isOutputReturned = "No"
                $error = "Exception in SQL connection:"+$_.Exception.Message
                $mainJson.Add("status",0)
                $mainJson.Add("msg",$error)
         }
        $dataObj.Add("isOutputReturned",$isOutputReturned)
        $dataObj.Add("isConnectionSuccessful",$isConnectionSuccessful)
        return 1
	
}

$data =Get-Data

$mainJson.add("data",$dataObj)
$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)
return $mainJson | ConvertTo-Json
