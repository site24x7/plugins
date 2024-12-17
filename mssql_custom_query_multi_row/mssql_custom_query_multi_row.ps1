param(
    [string]$SQLServer,
    [string]$SQLDBName,
    [string]$sqlusername,
    [string]$sqlpassword
)



$output = @{}
$heartbeat = "true"
$version = 1
$QueryFilePath=$PSScriptRoot+"\query.sql"

function Convert-ToTitleCase {
    param (
        [Parameter(Mandatory=$true)]
        [string]$InputString
    )
   # Write-Host $InputString
    #Write-Host ($InputString -split '\s+' | ForEach-Object { $_.Substring(0,1).ToUpper() + $_.Substring(1).ToLower() })
    return ($InputString -split '\s+' | ForEach-Object { $_.Substring(0,1).ToUpper() + $_.Substring(1).ToLower() }) -join ' '
}
Function Get-Data {

    $outdata = @{}
    
    try {
        $connectionString = "Server=$SQLServer;Database=$SQLDBName;User ID=$sqlusername;Password=$sqlpassword;"
        $connection = New-Object System.Data.SqlClient.SqlConnection
        $connection.ConnectionString = $connectionString
        $connection.Open()

        # Read SQL query from file
        $query = Get-Content $QueryFilePath -Raw

        $command = $connection.CreateCommand()
        $command.CommandText = $query
        
        $reader = $command.ExecuteReader()

        $table = New-Object System.Data.DataTable
        $table.Load($reader)
        $log_out=""

         
        $current_time=Get-Date

        for (($i1 = $table.Rows.Count -1); $i1 -ge 0; $i1--) {
            $row = $table.Rows[$i1]
            $current_time=$current_time.AddSeconds(-1)
            $log_str=($current_time.ToString("yyyy/MM/dd-HH:mm:ss"))+",  "
            $log_pattern='$Datetime:date:yyyy/MM/dd-HH:mm:ss$,  ' 

            for ($i = 0; $i -lt $table.Columns.Count; $i++) {
                #$outdata.Add($table.Columns[$i].ColumnName, $row[$i])
                
                
                $log_str=$log_str+$row[$i]+",  "
                $column_name=( $table.Columns[$i].ColumnName -replace "_"," ").Tostring()
               
               # if  ($column_name.Length -gt 3){
                #    $column_name =( Convert-ToTitleCase $column_name  ) -replace " ",""
                # Write-Host $column_name.Length, $column_name

              #  }

                $log_pattern=$log_pattern+"$"+($column_name -replace " ","")+"$,  "
            }
            if ($log_str.Length -ne 0){
                $log_str=$log_str.Substring(0, $log_str.Length - 2)
                $log_pattern=$log_pattern.Substring(0, $log_pattern.Length - 2)
            }

       
        $log_output+="`n"+$log_str#+"`n"
        } 
        #Write-Host $log_output

        $reader.Close()
        $connection.Close()
        $outdata.add("connection","ok")


        if (-not (Test-Path -Path ($PSScriptRoot+"\log_pattern.txt"))) {
               
           $file= New-Item -Path ($PSScriptRoot+"\log_pattern.txt") -ItemType File
           $log_pattern | Out-File -FilePath ($PSScriptRoot+"\log_pattern.txt")
        }

        Remove-Item -Path  ($PSScriptRoot+"\query_output`*.txt")
        $file_time=Get-Date -Format "MM-dd-yyyy-HH-mm-ss"

        $file= New-Item -Path ($PSScriptRoot+"\query_output"+$file_time+".txt") -ItemType File
        $log_output | Out-File -FilePath  ($PSScriptRoot+"\query_output"+$file_time+".txt")
        $outdata.add("Logs written","ok")
        $outdata.add("status","1")
        $outdata.add("Rows fetched",$table.Rows.Count)


        return $outdata
    }
    catch {
        $outdata.Add("status", 0)
        $outdata.Add("msg", $Error[0].Exception.Message)
        #Write-Host $_.Exception


        if ($reader) { $reader.Close() }
        if ($connection) { $connection.Close() }

        return $outdata
    }
}

$output.Add("heartbeat_required", $heartbeat)
$data = Get-Data
$output.Add("data", $data)
$output.Add("plugin_version", $version)

$output | ConvertTo-Json
