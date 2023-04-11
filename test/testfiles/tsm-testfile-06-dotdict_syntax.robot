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
# tsm-testfile-06-dotdict_syntax.robot (with variant configuration and extended parameter logging for dotdict syntax in JSON files)
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
Test Case tsm-testfile-06-dotdict_syntax
   [documentation]    tsm-testfile-06-dotdict_syntax
   rf.extensions.pretty_print    ${CONFIG.Project}        PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${teststring_common}     PARAMS-VERIFIKATION : ({teststring_common} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${teststring_variant}    PARAMS-VERIFIKATION : ({teststring_variant} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${teststring_bench}      PARAMS-VERIFIKATION : ({teststring_bench} / tsm-testfile-06-dotdict_syntax)

   rf.extensions.pretty_print    ${dTestDict}    PARAMS-VERIFIKATION : ({dTestDict} / tsm-testfile-06-dotdict_syntax)

   rf.extensions.pretty_print    ${ddKeyB_param}    PARAMS-VERIFIKATION : ({ddKeyB_param} / tsm-testfile-06-dotdict_syntax)

   rf.extensions.pretty_print    ${ddKeyA_2_param_1}    PARAMS-VERIFIKATION : ({ddKeyA_2_param_1} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${ddKeyA_2_param_2}    PARAMS-VERIFIKATION : ({ddKeyA_2_param_2} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${ddKeyA_2_param_3}    PARAMS-VERIFIKATION : ({ddKeyA_2_param_3} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${ddKeyA_2_param_4}    PARAMS-VERIFIKATION : ({ddKeyA_2_param_4} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${ddKeyB_2_param_1}    PARAMS-VERIFIKATION : ({ddKeyB_2_param_1} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${ddKeyB_2_param_2}    PARAMS-VERIFIKATION : ({ddKeyB_2_param_2} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${ddKeyB_2_param_3}    PARAMS-VERIFIKATION : ({ddKeyB_2_param_3} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${ddKeyB_2_param_4}    PARAMS-VERIFIKATION : ({ddKeyB_2_param_4} / tsm-testfile-06-dotdict_syntax)

   rf.extensions.pretty_print    ${dTestDict.ddKeyA.ddKeyA_2_param_1}    PARAMS-VERIFIKATION : ({dTestDict.ddKeyA.ddKeyA_2_param_1} / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${dTestDict.ddKeyB.ddKeyB_2_param_4}    PARAMS-VERIFIKATION : ({dTestDict.ddKeyB.ddKeyB_2_param_4} / tsm-testfile-06-dotdict_syntax)

   rf.extensions.pretty_print    ${dTestDict.ddKeyA}[ddKeyA_2_param_1]    PARAMS-VERIFIKATION : ({dTestDict.ddKeyA}[ddKeyA_2_param_1] / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${dTestDict.ddKeyB}[ddKeyB_2_param_4]    PARAMS-VERIFIKATION : ({dTestDict.ddKeyB}[ddKeyB_2_param_4] / tsm-testfile-06-dotdict_syntax)

   rf.extensions.pretty_print    ${dTestDict}[ddKeyA][ddKeyA_2_param_1]    PARAMS-VERIFIKATION : ({dTestDict}[ddKeyA][ddKeyA_2_param_1] / tsm-testfile-06-dotdict_syntax)
   rf.extensions.pretty_print    ${dTestDict}[ddKeyB][ddKeyB_2_param_4]    PARAMS-VERIFIKATION : ({dTestDict}[ddKeyB][ddKeyB_2_param_4] / tsm-testfile-06-dotdict_syntax)

   # This test is executed with only one single configuration; therefore all parameter values are fix. We can check them already here:

   Should Be Equal    ${ddKeyB_param}        ddKeyB_value
   Should Be Equal    ${ddKeyA_2_param}      ddKeyA_2_value

   Should Be Equal    ${ddKeyA_2_param_1}    ddKeyA_2_value
   Should Be Equal    ${ddKeyA_2_param_2}    ddKeyA_2_value
   Should Be Equal    ${ddKeyA_2_param_3}    ddKeyA_2_value
   Should Be Equal    ${ddKeyA_2_param_4}    ddKeyA_2_value

   Should Be Equal    ${ddKeyB_2_param_1}    ddKeyB_2_value
   Should Be Equal    ${ddKeyB_2_param_2}    ddKeyB_2_value
   Should Be Equal    ${ddKeyB_2_param_3}    ddKeyB_2_value
   Should Be Equal    ${ddKeyB_2_param_4}    ddKeyB_2_value



