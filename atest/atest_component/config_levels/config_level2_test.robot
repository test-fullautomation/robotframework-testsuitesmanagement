#  Copyright 2020-2023 Robert Bosch GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
*** Settings ***
Library    ../../resources/atest_libs.py    WITH NAME    testlibs

*** Test Cases ***
Test Config Level_2_01
    ${check}=    Subprocess Execution    ./testsuites/config_level2_01.robot
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Config Level_2_02
    ${check}=    Subprocess Execution    ./testsuites/config_level2_02.robot
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Config Level_2_03
    ${check}=    Subprocess Execution    ./testsuites/level_2_3/config_level2_03.robot
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Config Level_2_04
    ${check}=    Subprocess Execution    ./testsuites/level_2_3/config_level2_04.robot
    Log    ${check}
    Should Be Equal    ${check}    Passed
