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
# tsm-testfile-54-version-control-15.robot (with variant configuration)
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
Test Case tsm-testfile-54-version-control-15
    [documentation]    Robot Interface
    ...                'max_version' is smaller than 'reference_version'
    ...                tsm-testfile-54-version-control-15
    ...                TSM_0459
    # some basics
    rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-54-version-control-15)
    rf.extensions.pretty_print    ${teststring_common}     PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-54-version-control-15)
    rf.extensions.pretty_print    ${teststring_variant}    PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-54-version-control-15)
    rf.extensions.pretty_print    ${teststring_bench}      PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-54-version-control-15)
    # version control
    ${status}    ${result}=    run_keyword_and_ignore_error    tm.check_version    min_version=0.1.0    max_version=0.4.0    reference_version=0.6.0
    rf.extensions.pretty_print    ${status}      PARAMS-VERIFIKATION : ({status} / tsm-testfile-54-version-control-15)
    rf.extensions.pretty_print    ${result}      PARAMS-VERIFIKATION : ({result} / tsm-testfile-54-version-control-15)
    should_be_equal    ${status}    FAIL
    should_be_equal    ${result}    Execution will be aborted because of a failed version check
