@echo off
set scriptPath=%~dp0security_events.ps1

powershell -Command "$process = Start-Process PowerShell -ArgumentList '-ExecutionPolicy Bypass -File \"%scriptPath%\"' -PassThru -NoNewWindow; $exited = $process | Wait-Process -Timeout 15 -ErrorAction SilentlyContinue; if (-not $exited) { Write-Output '{\"Malware Detections\":-1,\"Failed Windows Updates\":-1,\"Account Lockouts\":-1,\"Security Threats Actions\":-1,\"plugin_version\":1,\"heartbeat_required\":\"true\",\"Failed Login Attempts\":-1,\"Threat Detected Quarantined\":-1,\"Antivirus Status\":-1,\"Malware Action Failed\":-1,\"Malware Remediation Failed\":-1}'; if (-not $process.HasExited) { Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue } }"

exit
