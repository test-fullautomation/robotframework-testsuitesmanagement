@echo off

REM "%RobotPythonPath%/python.exe" "./component_test.py" --skiplogcompare
REM "%RobotPythonPath%/python.exe" "./component_test.py"
REM "%RobotPythonPath%/python.exe" "./component_test.py" --testid="TSM_0558" --skiplogcompare
REM "%RobotPythonPath%/python.exe" "./component_test.py" --testid="TSM_0555"
REM "%RobotPythonPath%/python.exe" "./component_test.py" --codedump
"%RobotPythonPath%/python.exe" "./component_test.py" --configdump

echo ---------------------------------------
echo component_test returned ERRORLEVEL : %ERRORLEVEL%
echo ---------------------------------------

pause
