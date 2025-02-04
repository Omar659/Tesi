@echo off
taskkill /IM python.exe /F > nul 2>&1
taskkill /IM pythonw.exe /F > nul 2>&1
echo Tutti i processi Python sono stati terminati