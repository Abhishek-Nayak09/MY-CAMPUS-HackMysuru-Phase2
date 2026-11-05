@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_my_campus.ps1" %*
if errorlevel 1 pause
