# **************************************************************************************************************
#  Copyright 2020-2023 Robert Bosch GmbH
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
# tsm-testfile-20-fatal_error.robot (with variant configuration and several tests; keyword FATAL ERROR)
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

Test Case tsm-testfile-20-fatal_error-1
   [documentation]    tsm-testfile-20-fatal_error-1
   rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-20-fatal_error-1)
   rf.extensions.pretty_print    ${teststring_common}     PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-20-fatal_error-1)
   rf.extensions.pretty_print    ${teststring_variant}    PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-20-fatal_error-1)
   rf.extensions.pretty_print    ${teststring_bench}      PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-20-fatal_error-1)

Test Case tsm-testfile-20-fatal_error-2
   [documentation]    tsm-testfile-20-fatal_error-2
   rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-20-fatal_error-2)
   rf.extensions.pretty_print    ${teststring_common}     PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-20-fatal_error-2)
   rf.extensions.pretty_print    ${teststring_variant}    PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-20-fatal_error-2)
   rf.extensions.pretty_print    ${teststring_bench}      PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-20-fatal_error-2)

   FATAL ERROR

   Log    I must not be executed    console=yes

Test Case tsm-testfile-20-fatal_error-3
   [documentation]    tsm-testfile-20-fatal_error-3
   rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-20-fatal_error-3)
   rf.extensions.pretty_print    ${teststring_common}     PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-20-fatal_error-3)
   rf.extensions.pretty_print    ${teststring_variant}    PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-20-fatal_error-3)
   rf.extensions.pretty_print    ${teststring_bench}      PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-20-fatal_error-3)

   Log    I must not be executed    console=yes

Test Case tsm-testfile-20-fatal_error-4
   [documentation]    tsm-testfile-20-fatal_error-4
   rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-20-fatal_error-4)
   rf.extensions.pretty_print    ${teststring_common}     PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-20-fatal_error-4)
   rf.extensions.pretty_print    ${teststring_variant}    PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-20-fatal_error-4)
   rf.extensions.pretty_print    ${teststring_bench}      PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-20-fatal_error-4)

   Log    I must not be executed    console=yes

