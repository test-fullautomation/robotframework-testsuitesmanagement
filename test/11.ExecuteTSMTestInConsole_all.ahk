SetTitleMatchMode, 2

Run, %comspec% /k, ./
WinWait, cmd.exe
WinWaitActive, cmd.exe

Sleep, 500

SendInput "D:\ROBFW\components\robotframework-testsuitesmanagement\test\component_test_2_execute_all.bat"
