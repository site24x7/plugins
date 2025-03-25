@echo off
set scriptPath=%~dp0security_events.ps1

powershell -Command "Start-Process PowerShell -ArgumentList '-ExecutionPolicy Bypass -File \"%scriptPath%\"' -NoNewWindow -PassThru | ForEach-Object { $_ | Wait-Process -Timeout 15 -ErrorAction SilentlyContinue; if (!$_.HasExited) { Write-Output '{\"Malware Detections\":-1,\"Failed Windows Updates\":-1,\"Account Lockouts\":-1,\"Security Threats Actions\":-1,\"plugin_version\":1,\"heartbeat_required\":\"true\",\"Failed Login Attempts\":-1,\"Threat Detected Quarantined\":-1,\"Antivirus Status\":-1,\"Malware Action Failed\":-1,\"Malware Remediation Failed\":-1}'; Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue } }"

exit
