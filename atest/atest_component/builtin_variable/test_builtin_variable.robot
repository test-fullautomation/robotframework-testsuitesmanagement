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
Library    ../../resources/atest_libs.py    WITH NAME    testlibs

*** Test Cases ***
Test BuiltIn Variables From Command 01
    [Documentation]    Test builtIn variables from command line with configuration level 1. 
    ${check}=    Subprocess Execution    ./testsuites/builtin_variable_with_config_level_1.robot    --variable gGlobalString:"BuiltIn variables test" --variablefile ../../testdata/templates.py --log builtin_variable_with_config_level_1.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test BuiltIn Variables From Command 02
    [Documentation]    Test builtIn variables from command line with configuration level 2. 
    ${check}=    Subprocess Execution    ./testsuites/builtin_variable_with_config_level_2.robot    --variable variant:variant_2 --variable gGlobalString:"BuiltIn variables test" --variablefile ../../testdata/templates.py --log builtin_variable_with_config_level_2.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test BuiltIn Variables From Command 03
    [Documentation]    Test builtIn variables from command line with configuration level 3. 
    ${check}=    Subprocess Execution    ./testsuites/builtin_variable_with_config_level_3.robot    --variable gGlobalString:"BuiltIn variables test" --variablefile ../../testdata/templates.py --log builtin_variable_with_config_level_3.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test BuiltIn Variables From Command 04
    [Documentation]    Test builtIn variables from command line with local configuration feature. 
    ${check}=    Subprocess Execution    ./testsuites/builtin_variable_with_local_config.robot    --variable variant:variant_2 --variable local_config:./config/local_config.json --variable gGlobalString:"BuiltIn variables test" --variablefile ../../testdata/templates.py --log builtin_variable_with_local_config.html
    Log    ${check}
    Should Be Equal    ${check}    Passed