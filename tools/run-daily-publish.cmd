@echo off
setlocal
set LOGDIR=%~dp0..\logs
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
set LOGFILE=%LOGDIR%\daily-publish.log

echo ==== %date% %time% start ==== >> "%LOGFILE%"
node "%~dp0daily_publish.js" >> "%LOGFILE%" 2>&1
echo ==== %date% %time% exit code %ERRORLEVEL% ==== >> "%LOGFILE%"

endlocal
