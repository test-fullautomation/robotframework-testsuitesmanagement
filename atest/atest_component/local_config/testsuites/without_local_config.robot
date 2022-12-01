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
#######################################################################

*** Variables ***
${variant}   variant_1

*** Settings ***
#Force Tags        atestExcluded
Library      RobotFramework_Testsuites    WITH NAME    testsuites
Suite Setup      testsuites.testsuite_setup    ../../../general_config/testsuites_config.json
Suite Teardown   testsuites.testsuite_teardown
Test Setup       testsuites.testcase_setup
Test Teardown    testsuites.testcase_teardown

*** Test Cases ***
Test Local Config With Input Variable 01
    Log   ${CONFIG}
    Should Be Equal    ${CONFIG.WelcomeString}    Hello... ROBFW is running now!
    Should Be Equal    ${gPreproString}    This is a string
    Should Be Equal    ${gGlobalString}    This is a string
    Should Be Equal    ${gGlobalStructure.general}    general