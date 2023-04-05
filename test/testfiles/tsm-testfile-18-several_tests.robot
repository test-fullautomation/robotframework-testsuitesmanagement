# **************************************************************************************************************
#  Copyright 2020-2022 Robert Bosch GmbH
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
# tsm-testfile-18-several_tests.robot (containing several tests, some PASSED, some FAILED, some UNKNOWN)
#
# --------------------------------------------------------------------------------------------------------------

*** Settings ***

Library    RobotFramework_TestsuitesManagement    WITH NAME    tm
Library    RobotframeworkExtensions.Collection    WITH NAME    rf.extensions

Suite Setup       tm.testsuite_setup    ./config/tsm-test_variants.json
Suite Teardown    tm.testsuite_teardown
Test Setup        tm.testcase_setup
Test Teardown     tm.testcase_teardown

*** Test Cases ***

Test Case tsm-testfile-18-several_tests-1-passed
   [documentation]    tsm-testfile-18-several_tests-1-passed
   rf.extensions.pretty_print    ${CONFIG.Project}    PARAMS-VERIFIKATION : (CONFIG.Project)
   Log    teststring_common : ${teststring_common} (tsm-testfile-18-several_tests.robot)      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-testfile-18-several_tests.robot)    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-testfile-18-several_tests.robot)        console=yes

Test Case tsm-testfile-18-several_tests-2-passed
   [documentation]    tsm-testfile-18-several_tests-2-passed
   rf.extensions.pretty_print    ${CONFIG.Project}    PARAMS-VERIFIKATION : (CONFIG.Project)
   Log    teststring_common : ${teststring_common} (tsm-testfile-18-several_tests.robot)      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-testfile-18-several_tests.robot)    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-testfile-18-several_tests.robot)        console=yes

Test Case tsm-testfile-18-several_tests-3-failed
   [documentation]    tsm-testfile-18-several_tests-3-failed
   rf.extensions.pretty_print    ${CONFIG.Project}    PARAMS-VERIFIKATION : (CONFIG.Project)
   Log    teststring_common : ${teststring_common} (tsm-testfile-18-several_tests.robot)      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-testfile-18-several_tests.robot)    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-testfile-18-several_tests.robot)        console=yes

   FAIL

   Log    I must not be executed    console=yes

Test Case tsm-testfile-18-several_tests-4-failed
   [documentation]    tsm-testfile-18-several_tests-4-failed
   rf.extensions.pretty_print    ${CONFIG.Project}    PARAMS-VERIFIKATION : (CONFIG.Project)
   Log    teststring_common : ${teststring_common} (tsm-testfile-18-several_tests.robot)      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-testfile-18-several_tests.robot)    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-testfile-18-several_tests.robot)        console=yes

   FAIL

   Log    I must not be executed    console=yes

Test Case tsm-testfile-18-several_tests-5-failed
   [documentation]    tsm-testfile-18-several_tests-5-failed
   rf.extensions.pretty_print    ${CONFIG.Project}    PARAMS-VERIFIKATION : (CONFIG.Project)
   Log    teststring_common : ${teststring_common} (tsm-testfile-18-several_tests.robot)      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-testfile-18-several_tests.robot)    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-testfile-18-several_tests.robot)        console=yes

   FAIL

   Log    I must not be executed    console=yes

Test Case tsm-testfile-18-several_tests-6-unknown
   [documentation]    tsm-testfile-18-several_tests-6-unknown
   rf.extensions.pretty_print    ${CONFIG.Project}    PARAMS-VERIFIKATION : (CONFIG.Project)
   Log    teststring_common : ${teststring_common} (tsm-testfile-18-several_tests.robot)      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-testfile-18-several_tests.robot)    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-testfile-18-several_tests.robot)        console=yes

   UNKNOWN

   Log    I must not be executed    console=yes

Test Case tsm-testfile-18-several_tests-7-unknown
   [documentation]    tsm-testfile-18-several_tests-7-unknown
   rf.extensions.pretty_print    ${CONFIG.Project}    PARAMS-VERIFIKATION : (CONFIG.Project)
   Log    teststring_common : ${teststring_common} (tsm-testfile-18-several_tests.robot)      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-testfile-18-several_tests.robot)    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-testfile-18-several_tests.robot)        console=yes

   UNKNOWN

   Log    I must not be executed    console=yes

Test Case tsm-testfile-18-several_tests-8-unknown
   [documentation]    tsm-testfile-18-several_tests-8-unknown
   rf.extensions.pretty_print    ${CONFIG.Project}    PARAMS-VERIFIKATION : (CONFIG.Project)
   Log    teststring_common : ${teststring_common} (tsm-testfile-18-several_tests.robot)      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-testfile-18-several_tests.robot)    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-testfile-18-several_tests.robot)        console=yes

   UNKNOWN

   Log    I must not be executed    console=yes

Test Case tsm-testfile-18-several_tests-9-unknown
   [documentation]    tsm-testfile-18-several_tests-9-unknown
   rf.extensions.pretty_print    ${CONFIG.Project}    PARAMS-VERIFIKATION : (CONFIG.Project)
   Log    teststring_common : ${teststring_common} (tsm-testfile-18-several_tests.robot)      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-testfile-18-several_tests.robot)    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-testfile-18-several_tests.robot)        console=yes

   UNKNOWN

   Log    I must not be executed    console=yes

