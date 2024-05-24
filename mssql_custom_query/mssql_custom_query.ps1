param(
    [string]$SQLServer,
    [string]$SQLDBName,
    [string]$sqlusername,
    [string]$sqlpassword
)

$output = @{}
$heartbeat = "true"
$version = 1
$QueryFilePath="query.sql"

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

        if ($table.Rows.Count -gt 0) {
            $row = $table.Rows[0]
            for ($i = 0; $i -lt $table.Columns.Count; $i++) {
                $outdata.Add($table.Columns[$i].ColumnName, $row[$i])
            }
        } else {
            $outdata.Add("status", 0)
            $outdata.Add("msg", "Rows not found")
        }

        $reader.Close()
        $connection.Close()

        return $outdata
    }
    catch {
        $outdata.Add("status", 0)
        $outdata.Add("msg", $Error[0].Exception.Message)

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
