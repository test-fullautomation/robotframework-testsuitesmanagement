#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
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
Library      RobotFramework_Testsuites    WITH NAME    testsuites
Suite Setup      testsuites.testsuite_setup    ../../../general_config/testsuites_config.json
Suite Teardown   testsuites.testsuite_teardown
Test Setup       testsuites.testcase_setup
Test Teardown    testsuites.testcase_teardown

*** Test Cases ***
Test Dotdict Global Params 003
    [Documentation]    "." is included in parameter name -> could not using dotdict but the traiditional way still works
    Log    ${dSUT}[system][hardware][wifi.sAddress]
    Log    ${dSUT}[system][hardware][bt.sAdress]
    Should Be Equal    ${dSUT.system.hardware.sSample}    ${dSUT}[system][hardware][sSample]
    Should Be Equal    ${dSUT}[system][hardware][wifi.sAddress]    123:123:123:123
    Should Be Equal    ${dSUT}[system][hardware][bt.sAdress]    12:12:14:15