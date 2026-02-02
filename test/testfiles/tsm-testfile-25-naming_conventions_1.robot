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

Library    RobotFramework_TestsuitesManagement    AS    tm
Library    RobotframeworkExtensions.Collection    AS    rf.extensions

Suite Setup       tm.testsuite_setup    ./config/tsm-test_variants.jsonp
Suite Teardown    tm.testsuite_teardown
Test Setup        tm.testcase_setup
Test Teardown     tm.testcase_teardown

*** Test Cases ***

Test Case tsm-testfile-25-naming_conventions_1
   [documentation]    tsm-testfile-25-naming_conventions_1
   rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-25-naming_conventions_1)

   rf.extensions.pretty_print    ${ABC}            PARAMS-VERIFIKATION : ({ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${Ä_ABC}          PARAMS-VERIFIKATION : ({Ä_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${ABC_ß}          PARAMS-VERIFIKATION : ({ABC_ß} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${𠼭_ABC}         PARAMS-VERIFIKATION : ({𠼭_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${ABC_𠼭}         PARAMS-VERIFIKATION : ({ABC_𠼭} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${ß_01_ABC}       PARAMS-VERIFIKATION : ({ß_01_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${𠼭_01_ABC}      PARAMS-VERIFIKATION : ({𠼭_01_ABC} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${D__E__F}       PARAMS-VERIFIKATION : ({D__E__F} / tsm-testfile-25-naming_conventions_1)
   rf.extensions.pretty_print    ${AB_𠼭_൯}        PARAMS-VERIFIKATION : ({AB_𠼭_൯}} / tsm-testfile-25-naming_conventions_1)

