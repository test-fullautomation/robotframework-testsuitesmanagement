# **************************************************************************************************************
#  Copyright 2020-2025 Robert Bosch GmbH
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
# **************************************************************************************************************
#
# tsm-testfile-27-python_inline_code.robot (with variant configuration (GC))
#
# --------------------------------------------------------------------------------------------------------------

*** Settings ***

Library    RobotFramework_TestsuitesManagement    WITH NAME    tm
Library    RobotframeworkExtensions.Collection    WITH NAME    rf.extensions

Suite Setup       tm.testsuite_setup    ./config/tsm-test_variants.jsonp
Suite Teardown    tm.testsuite_teardown
Test Setup        tm.testcase_setup
Test Teardown     tm.testcase_teardown

*** Test Cases ***

Test Case tsm-testfile-27-python_inline_code
    [documentation]    tsm-testfile-27-python_inline_code
    rf.extensions.pretty_print    ${value01}    PARAMS-VERIFIKATION : ({value01} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value02}    PARAMS-VERIFIKATION : ({value02} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value03}    PARAMS-VERIFIKATION : ({value03} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value04}    PARAMS-VERIFIKATION : ({value04} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value05}    PARAMS-VERIFIKATION : ({value05} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value06}    PARAMS-VERIFIKATION : ({value06} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value07}    PARAMS-VERIFIKATION : ({value07} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value08}    PARAMS-VERIFIKATION : ({value08} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value09}    PARAMS-VERIFIKATION : ({value09} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value10}    PARAMS-VERIFIKATION : ({value10} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value11}    PARAMS-VERIFIKATION : ({value11} / tsm-testfile-27-python_inline_code)
    # expression not resolved # rf.extensions.pretty_print    ${value12}    PARAMS-VERIFIKATION : ({value12} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value13}    PARAMS-VERIFIKATION : ({value13} / tsm-testfile-27-python_inline_code)
    # error # rf.extensions.pretty_print    ${value14}    PARAMS-VERIFIKATION : ({value14} / tsm-testfile-27-python_inline_code)
    # error # rf.extensions.pretty_print    ${value15}    PARAMS-VERIFIKATION : ({value15} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value16}    PARAMS-VERIFIKATION : ({value16} / tsm-testfile-27-python_inline_code)
    rf.extensions.pretty_print    ${value17}    PARAMS-VERIFIKATION : ({value17} / tsm-testfile-27-python_inline_code)
    # error # rf.extensions.pretty_print    ${value18}    PARAMS-VERIFIKATION : ({value18} / tsm-testfile-27-python_inline_code)
    # error # rf.extensions.pretty_print    ${value19}    PARAMS-VERIFIKATION : ({value19} / tsm-testfile-27-python_inline_code)


