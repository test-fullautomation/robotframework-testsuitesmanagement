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
Suite setup    Create Valid Default Local Config File
Suite Teardown    Delete Default Local Config File

*** Test Cases ***
Test Local Config with Valid Input Variable 01
    [Documentation]    Test valid local configuration with configuration level 1. 
    ${check}=    Subprocess Execution    ./testsuites/local_config_form_input_variable_01.robot    --variable local_config:../../../general_config/localconfig/local_config_cmd_input.json --log Valid_Input_Variable_01.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Local Config with Valid Input Variable 02
    [Documentation]    Test valid local configuration with configuration level 2.
    ${check}=    Subprocess Execution    ./testsuites/local_config_form_input_variable_02.robot    --variable local_config:../../../general_config/localconfig/local_config_cmd_input.json --log Valid_Input_Variable_02.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Local Config with Valid Input Variable 03
    [Documentation]    Test valid local configuration with configuration level 3. 
    ${check}=    Subprocess Execution    ./testsuites/local_config_form_input_variable_03.robot    --variable local_config:../../../general_config/localconfig/local_config_cmd_input.json --log Valid_Input_Variable_03.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Local Config with Valid Input Variable 04
    [Documentation]    Test valid local configuration with configuration level 4. 
    ${check}=    Subprocess Execution    ./testsuites/local_config_form_input_variable_04.robot    --variable local_config:../../../general_config/localconfig/local_config_cmd_input_level4.json --log Valid_Input_Variable_04.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Local Config with Invalid Input Variable 01
    ${check}=    Subprocess Execution    ./testsuites/local_config_form_input_variable_01.robot    --variable local_config:../../../general_config/localconfig/not_exist_local_config_cmd_input.json --log Invalid_Input_Variable_01.html
    Log    ${check}
    Should Be Equal    ${check}    Failed

Test Local Config Default 01
    [Documentation]    Test valid default local configuration with configuration level 1. 
    ${check}=    Subprocess Execution    ./testsuites/local_config_default_01.robot    --log Local_Config_Default_01.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Local Config Default 02
    [Documentation]    Test valid default local configuration with configuration level 2. 
    ${check}=    Subprocess Execution    ./testsuites/local_config_default_02.robot    --log Local_Config_Default_02.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Local Config Default 03
    [Documentation]    Test valid default local configuration with configuration level 3. 
    ${check}=    Subprocess Execution    ./testsuites/local_config_default_03.robot    --log Local_Config_Default_03.html
    Log    ${check}
    Should Be Equal    ${check}    Passed

Test Without Local Config
    Delete Default Local Config File
    ${check}=    Subprocess Execution    ./testsuites/without_local_config.robot    --log Without_Local_Config.html
    Log    ${check}
    Should Be Equal    ${check}    Passed
