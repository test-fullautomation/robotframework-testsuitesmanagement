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
# tsm-testfile-25-naming_conventions_1.robot (with variant configuration and output of several (valid) parameter names (GC))
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

Test Case tsm-testfile-25-naming_conventions_1
   [documentation]    tsm-testfile-25-naming_conventions_1
   rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-25-naming_conventions_1)

   rf.extensions.pretty_print    ${ABC}            PARAMS-VERIFIKATION : ({ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${01ABC}          PARAMS-VERIFIKATION : ({01ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${01_Ä_ABC}       PARAMS-VERIFIKATION : ({01_Ä_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${01_ß_ABC}       PARAMS-VERIFIKATION : ({01_ß_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${01_𠼭_ABC}      PARAMS-VERIFIKATION : ({01_𠼭_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${Ä_01_ABC}       PARAMS-VERIFIKATION : ({Ä_01_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${ß_01_ABC}       PARAMS-VERIFIKATION : ({ß_01_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${𠼭_01_ABC}      PARAMS-VERIFIKATION : ({𠼭_01_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${__DEF}          PARAMS-VERIFIKATION : ({__DEF} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${G__H__I}        PARAMS-VERIFIKATION : ({G__H__I} / tsm-testfile-25-naming_conventions_1)



