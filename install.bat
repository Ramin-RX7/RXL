@echo off
echo Installing Python ...
start .\python-3.8.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
rem InstallAllUsers=0 DefaultJustForMeTargetDir=%LocalAppData%\Programs\Python
rem setx /M path "%path%;%ProgramFiles%\Python38"

:1
if exist "%ProgramFiles%\Python38" (
echo Don
echo.
pause
exit
) else (
goto :1
)

python .\instal
echo.
echo RX Language Has Been Installed Successfully
rem ADD TO PATH
echo.
pause
