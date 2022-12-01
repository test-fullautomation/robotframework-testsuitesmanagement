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
${config_file}   ../../../general_config/robot_config_variant_1.json

*** Settings ***
#Force Tags        atestExcluded
Library      RobotFramework_Testsuites    WITH NAME    testsuites
Suite Setup      testsuites.testsuite_setup
Suite Teardown   testsuites.testsuite_teardown
Test Setup       testsuites.testcase_setup
Test Teardown    testsuites.testcase_teardown

*** Test Cases ***
Test Local Config Default 01
    Log   ${CONFIG}
    Should Be Equal    ${CONFIG.WelcomeString}    Default - Test local config!
    Should Be Equal    ${gPreproString}    Default - Preprocessor - Test local config updated!
    Should Be Equal    ${gGlobalString}    Default - Local configuration test!
    Should Be Equal    ${testNewVar}    ${1.111}
    Should Be Equal    ${gGlobalStructure.local_config_add}    ${1101}