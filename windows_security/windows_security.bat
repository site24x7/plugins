@echo off
set scriptPath=%~dp0security_events.ps1

set scriptPathQuoted=%scriptPath%

for /f "delims=" %%i in ('powershell -Command "$process= Start-Process PowerShell -ArgumentList '-ExecutionPolicy Bypass -File ""%scriptPathQuoted%""' -PassThru -NoNewWindow -ErrorAction SilentlyContinue; $process | Wait-Process -Timeout 25 -ErrorAction SilentlyContinue; if ($process.ExitCode -ne 0 -or-not $process.HasExited) { Write-Output '{\"Malware Detections\":-1,\"Failed Windows Updates\":-1,\"Account Lockouts\":-1,\"Security Threats Actions\":-1,\"plugin_version\":1,\"heartbeat_required\":\"true\",\"Failed Login Attempts\":-1,\"Threat Detected Quarantined\":-1,\"Antivirus Status\":-1,\"Malware Action Failed\":-1,\"Malware Remediation Failed\":-1,\"RDP_Connections\":[{\"name\":\"-\",\"RDPLocalAddress\":\"-\",\"RDPLocalPort\":-1,\"RDPRemoteAddress\":\"-\",\"RDPRemotePort\":-1,\"RDPState\":\"-\",\"RDPAppliedSettings\":\"-\",\"RDPOwningProcess\":-1}],\"Remote_Connections\":[{\"name\":\"-\",\"RemoteAddress\":\"-\",\"RemotePort\":-1,\"LocalAddress\":\"-\",\"LocalPort\":-1,\"State\":\"-\",\"ProcessName\":\"-\",\"PID\":-1}],\"tabs\":{\"RDP Connections\":{\"order\":1,\"tablist\":[\"RDP_Connections\"]},\"Remote Connections Process details\":{\"order\":2,\"tablist\":[\"Remote_Connections\"]}}}'; Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue }"') do set output=%%i

if not defined output (
    echo {"Malware Detections":-1,"Failed Windows Updates":-1,"Account Lockouts":-1,"Security Threats Actions":-1,"plugin_version":1,"heartbeat_required":"true","Failed Login Attempts":-1,"Threat Detected Quarantined":-1,"Antivirus Status":-1,"Malware Action Failed":-1,"Malware Remediation Failed":-1,"RDP_Connections":[{"name":"-","RDPLocalAddress":"-","RDPLocalPort":-1,"RDPRemoteAddress":"-","RDPRemotePort":-1,"RDPState":"-","RDPAppliedSettings":"-","RDPOwningProcess":-1}],"Remote_Connections":[{"name":"-","RemoteAddress":"-","RemotePort":-1,"LocalAddress":"-","LocalPort":-1,"State":"-","ProcessName":"-","PID":-1}],"tabs":{"RDP Connections":{"order":1,"tablist":["RDP_Connections"]},"Remote Connections Process details":{"order":2,"tablist":["Remote_Connections"]}}}
) else (
    echo %output%
)

exit
