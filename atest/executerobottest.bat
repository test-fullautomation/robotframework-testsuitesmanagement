@echo off
"%RobotPythonPath%/python.exe" "./executerobottest.py" --robotcommandline "--exclude atestExcluded"
echo -----------------------------------------
echo executerobottest returned ERRORLEVEL : %ERRORLEVEL%
echo -----------------------------------------

