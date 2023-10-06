@echo off
"%RobotPythonPath%/python.exe" "./executepytest.py" --pytestcommandline="--junit-prefix=TestsuitesManagement"
echo --------------------------------------
echo executepytest returned ERRORLEVEL : %ERRORLEVEL%
echo --------------------------------------

