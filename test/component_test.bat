@echo off

REM "%RobotPythonPath%/python.exe" "./component_test.py" --skiplogcompare
REM "%RobotPythonPath%/python.exe" "./component_test.py"
REM "%RobotPythonPath%/python.exe" "./component_test.py" --testid="TSM_0004" --skiplogcompare
REM "%RobotPythonPath%/python.exe" "./component_test.py" --testid="TSM_1050" --skiplogcompare
REM "%RobotPythonPath%/python.exe" "./component_test.py" --testid="TSM_0200"
"%RobotPythonPath%/python.exe" "./component_test.py" --testid="TSM_1200"
REM "%RobotPythonPath%/python.exe" "./component_test.py" --testid="TSM_0064"
REM "%RobotPythonPath%/python.exe" "./component_test.py" --codedump
REM "%RobotPythonPath%/python.exe" "./component_test.py" --configdump

echo ---------------------------------------
echo component_test returned ERRORLEVEL : %ERRORLEVEL%
echo ---------------------------------------

