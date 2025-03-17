@echo off
set scriptPath=%~dp0security_events.ps1
PowerShell -ExecutionPolicy Bypass -File "%scriptPath%"
exit
