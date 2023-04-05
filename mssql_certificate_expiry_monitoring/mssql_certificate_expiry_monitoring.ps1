param([string]$server,[string]$database,[string]$username,[string]$password)

$data = @{}
$heartbeat = "true"
$version = 1

Function Get-Data
{
    $units = @{}
    $now = Get-Date
    
    $results=Invoke-Sqlcmd -ConnectionString "Data Source=$server; User Id=$username; Password =$password" -Query "Select name,issuer_name,expiry_date,start_date from master.sys.certificates where pvt_key_encryption_type_desc='ENCRYPTED_BY_MASTER_KEY' "
    
    $data.Add("Certificate Name",$results.name)
    $data.Add("Certificate Issuer Name",$results.issuer_name)
    $data.Add("Certificate Start Date",($results.start_date).ToString())
    $results= $results | select expiry_date -expandproperty expiry_date
    $results=($results-$now).Days
    $data.Add("Certificate Expiry Date", $results)
    $units.Add("Certificate Expiry Date","days")
    $data.Add("units",$units)
    return 1
}
$data.Add("heartbeat_required", $heartbeat)
$output =Get-Data
$data.Add("plugin_version", $version)

$data | ConvertTo-Json


