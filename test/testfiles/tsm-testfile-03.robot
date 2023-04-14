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
# tsm-testfile-03.robot (with variant configuration and extended logging of parameters from nested
#                        configuration files)
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
Test Case tsm-testfile-03
   [documentation]    tsm-testfile-03
   rf.extensions.pretty_print    ${CONFIG.Project}                                  PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-03)
   rf.extensions.pretty_print    ${teststring_common}                               PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-03)
   rf.extensions.pretty_print    ${teststring_variant}                              PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-03)
   rf.extensions.pretty_print    ${teststring_bench}                                PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-03)
   rf.extensions.pretty_print    ${testdictionary_variant.tdv_key_1.tdv_key_1_1}    PARAMS-VERIFIKATION : ({testdictionary_variant.tdv_key_1.tdv_key_1_1} / tsm-testfile-03)
   rf.extensions.pretty_print    ${testdictionary_variant.tdv_key_1.tdv_key_1_2}    PARAMS-VERIFIKATION : ({testdictionary_variant.tdv_key_1.tdv_key_1_2} / tsm-testfile-03)
   rf.extensions.pretty_print    ${testdictionary_variant.tdv_key_2.tdv_key_2_1}    PARAMS-VERIFIKATION : ({testdictionary_variant.tdv_key_2.tdv_key_2_1} / tsm-testfile-03)
   rf.extensions.pretty_print    ${testdictionary_variant.tdv_key_3.tdv_key_3_1}    PARAMS-VERIFIKATION : ({testdictionary_variant.tdv_key_3.tdv_key_3_1} / tsm-testfile-03)
   rf.extensions.pretty_print    ${testlist_variant}[0]                             PARAMS-VERIFIKATION : ({testlist_variant}[0]} / tsm-testfile-03)
   rf.extensions.pretty_print    ${testlist_variant}[1]                             PARAMS-VERIFIKATION : ({testlist_variant}[1]} / tsm-testfile-03)
   rf.extensions.pretty_print    ${testlist_variant}[2]                             PARAMS-VERIFIKATION : ({testlist_variant}[2]} / tsm-testfile-03)
