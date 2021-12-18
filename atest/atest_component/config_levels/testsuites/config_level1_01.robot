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
#
#  Configures with level 1 only 
#  Set ${config_file}   ../../general_config/test_config_level_1.json
#  It's similar with execute robot test script with --variable config_file:../../general_config/test_config_level_1.json 
# 
#######################################################################

*** Variables ***
${config_file}   ../../../general_config/test_config_level_1.json

*** Settings ***
#Force Tags        atestExcluded
Library      RobotFramework_Testsuites    WITH NAME    testsuites
Suite Setup      testsuites.testsuite_setup
Suite Teardown   testsuites.testsuite_teardown
Test Setup       testsuites.testcase_setup
Test Teardown    testsuites.testcase_teardown

*** Test Cases ***
Test Dotdict Config Params 001
    Log   ${CONFIG}
    Should Be Equal    ${CONFIG.Project}    G3g-config-level_1