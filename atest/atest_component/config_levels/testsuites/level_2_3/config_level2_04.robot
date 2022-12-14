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
#  Using level 2 configuration also sets in this test suite ../../general_config/testsuites_config.json
#  The variant is set variant_2
#  The configuration level 3 also setup.
#  But the configuration level 2 is higher priority
# 
#######################################################################

*** Variables ***
${variant}    variant_2

*** Settings ***
#Force Tags        atestExcluded
Library      RobotFramework_TestsuitesManagement    WITH NAME    testsuites
Suite Setup      testsuites.testsuite_setup    ../../../../general_config/testsuites_config.json
Suite Teardown   testsuites.testsuite_teardown
Test Setup       testsuites.testcase_setup
Test Teardown    testsuites.testcase_teardown

*** Test Cases ***
Test Dotdict Config Params 001
    Log   ${CONFIG}
    Should Be Equal    ${CONFIG.Project}    G3g-variant_2