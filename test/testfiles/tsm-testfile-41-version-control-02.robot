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
# tsm-testfile-41-version-control-02.robot (with variant configuration)
#
# --------------------------------------------------------------------------------------------------------------

*** Settings ***

Library    RobotFramework_TestsuitesManagement    AS    tm
Library    RobotframeworkExtensions.Collection    AS    rf.extensions

Suite Setup       tm.testsuite_setup    ./config/tsm-test_variants.jsonp
Suite Teardown    tm.testsuite_teardown
Test Setup        tm.testcase_setup
Test Teardown     tm.testcase_teardown

*** Test Cases ***
Test Case tsm-testfile-41-version-control-02
    [documentation]    Robot Interface
    ...                'max_version' initialized with 'None', 'min_version' initialized with 'null', 'reference_version' not defined
    ...                tsm-testfile-41-version-control-02
    ...                TSM_0405
    # some basics
    rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-41-version-control-02)
    rf.extensions.pretty_print    ${teststring_common}     PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-41-version-control-02)
    rf.extensions.pretty_print    ${teststring_variant}    PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-41-version-control-02)
    rf.extensions.pretty_print    ${teststring_bench}      PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-41-version-control-02)
    # version control
    ${result}=    tm.check_version    max_version=${None}    min_version=${null}
    rf.extensions.pretty_print    ${result}      PARAMS-VERIFIKATION : ({result} / tsm-testfile-41-version-control-02)
    should_be_equal    ${result}    ${True}
