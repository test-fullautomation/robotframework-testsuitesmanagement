# **************************************************************************************************************
#  Copyright 2020-2026 Robert Bosch GmbH
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
# tsm-testfile-53-version-control-14.robot (with variant configuration)
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
Test Case tsm-testfile-53-version-control-14
    [documentation]    Robot Interface
    ...                'min_version' is bigger than 'max_version'
    ...                tsm-testfile-53-version-control-14
    ...                TSM_0458
    # some basics
    rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-53-version-control-14)
    rf.extensions.pretty_print    ${teststring_common}     PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-53-version-control-14)
    rf.extensions.pretty_print    ${teststring_variant}    PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-53-version-control-14)
    rf.extensions.pretty_print    ${teststring_bench}      PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-53-version-control-14)
    # version control
    ${status}    ${result}=    run_keyword_and_ignore_error    tm.check_version    min_version=0.10.0    max_version=0.4.0    reference_version=0.3.0
    rf.extensions.pretty_print    ${status}      PARAMS-VERIFIKATION : ({status} / tsm-testfile-53-version-control-14)
    rf.extensions.pretty_print    ${result}      PARAMS-VERIFIKATION : ({result} / tsm-testfile-53-version-control-14)
    should_be_equal    ${status}    FAIL
    should_be_equal    ${result}    Execution will be aborted because of a critical version check issue
