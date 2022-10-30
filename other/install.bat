@echo off
echo Run this script only if:
echo     You are using windows
echo     You dont have python installed
pause
echo Installing Python ...
start .\python-3.8.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
rem InstallAllUsers=0 DefaultJustForMeTargetDir=%LocalAppData%\Programs\Python
rem setx /M path "%path%;%ProgramFiles%\Python38"

:1
if exist "%ProgramFiles%\Python38" (
echo Done
echo.
pause
exit
) else (
goto :1
)

python .\install
echo.
echo RX Language Has Been Installed Successfully
rem ADD TO PATH
echo.
pause
