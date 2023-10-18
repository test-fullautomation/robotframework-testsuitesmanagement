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
# tsm-testfile-24-composite_expressions_1.robot (with variant configuration and additional log strings to test the string concatenation)
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

Test Case tsm-testfile-24-composite_expressions_1
   [documentation]    tsm-testfile-24-composite_expressions_1
   rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-24-composite_expressions_1)
   rf.extensions.pretty_print    ${teststring_common}     PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-24-composite_expressions_1)
   rf.extensions.pretty_print    ${teststring_variant}    PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-24-composite_expressions_1)
   rf.extensions.pretty_print    ${teststring_bench}      PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-24-composite_expressions_1)

   rf.extensions.pretty_print    ${teststring_1}      PARAMS-VERIFIKATION : ({teststring_1} / tsm-testfile-24-composite_expressions_1)
   rf.extensions.pretty_print    ${teststring_2}      PARAMS-VERIFIKATION : ({teststring_2} / tsm-testfile-24-composite_expressions_1)
   rf.extensions.pretty_print    ${teststring_3}      PARAMS-VERIFIKATION : ({teststring_3} / tsm-testfile-24-composite_expressions_1)

   rf.extensions.pretty_print    ${testdict.key.teststring_4}      PARAMS-VERIFIKATION : ({testdict.key.teststring_4} / tsm-testfile-24-composite_expressions_1)
