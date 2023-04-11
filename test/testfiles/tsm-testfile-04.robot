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
# tsm-testfile-04.robot (with variant configuration and extended logging of parameters from nested
#                        configuration files; all relevant datatypes; logging with pretty_print)
#
# --------------------------------------------------------------------------------------------------------------

*** Settings ***

Library    Collections

Library    RobotFramework_TestsuitesManagement    WITH NAME    tm
Library    RobotframeworkExtensions.Collection    WITH NAME    rf.extensions

Suite Setup       tm.testsuite_setup    ./config/tsm-test_variants.json
Suite Teardown    tm.testsuite_teardown
Test Setup        tm.testcase_setup
Test Teardown     tm.testcase_teardown

*** Test Cases ***
Test Case tsm-testfile-04
   [documentation]    tsm-testfile-04

   # 'PARAMS-VERIFIKATION : .... ' is a prefix string that is added to the beginning of every output line of pretty_print.
   # This prefix string is used by the log file comparison mechanism to identify relevant content to compare.
   # The goal is also to have the name of the printed parameter logged.

   # 'log_dictionary' is not helpful, because only the top level of keys is resolved; this keyword does not work recursively
   # log_dictionary    ${dict_val}
   # rf.extensions.pretty_print solves this issue.
   # rf.extensions.pretty_print also prints the data type, therefore it can be checked, if values like 123 are really realized as
   # integer value or as string.

   rf.extensions.pretty_print    ${CONFIG.WelcomeString}    PARAMS-VERIFIKATION : ({CONFIG.WelcomeString} / tsm-testfile-04)
   rf.extensions.pretty_print    ${CONFIG.Project}          PARAMS-VERIFIKATION : ({CONFIG.Project} / tsm-testfile-04)
   rf.extensions.pretty_print    ${CONFIG.TargetName}       PARAMS-VERIFIKATION : ({CONFIG.TargetName} / tsm-testfile-04)

   rf.extensions.pretty_print    ${CONFIG}[WelcomeString]   PARAMS-VERIFIKATION : ({CONFIG}[WelcomeString] / tsm-testfile-04)
   rf.extensions.pretty_print    ${CONFIG}[Project]         PARAMS-VERIFIKATION : ({CONFIG}[Project] / tsm-testfile-04)
   rf.extensions.pretty_print    ${CONFIG}[TargetName]      PARAMS-VERIFIKATION : ({CONFIG}[TargetName] / tsm-testfile-04)

   rf.extensions.pretty_print    ${CONFIG}                  PARAMS-VERIFIKATION : ({CONFIG} / tsm-testfile-04)

   rf.extensions.pretty_print    ${dict_val}                PARAMS-VERIFIKATION : ({dict_val} / tsm-testfile-04)
   rf.extensions.pretty_print    ${list_val}                PARAMS-VERIFIKATION : ({list_val} / tsm-testfile-04)

   rf.extensions.pretty_print    ${certain_teststring}      PARAMS-VERIFIKATION : ({certain_teststring} / tsm-testfile-04)
   rf.extensions.pretty_print    ${list_val[0]}             PARAMS-VERIFIKATION : ({list_val[0]} / tsm-testfile-04)

   rf.extensions.pretty_print    ${dict_val}[key_2][subkey_23][subsubkey_231]       PARAMS-VERIFIKATION : ({dict_val}[key_2][subkey_23][subsubkey_231] / tsm-testfile-04)
   rf.extensions.pretty_print    ${dict_val.key_2.subkey_23.subsubkey_231}          PARAMS-VERIFIKATION : ({dict_val.key_2.subkey_23.subsubkey_231} / tsm-testfile-04)

   rf.extensions.pretty_print    ${dict_val}[key_2][subkey_23][subsubkey_232][0]    PARAMS-VERIFIKATION : ({dict_val}[key_2][subkey_23][subsubkey_232][0] / tsm-testfile-04)
   rf.extensions.pretty_print    ${dict_val.key_2.subkey_23.subsubkey_232}[0]       PARAMS-VERIFIKATION : ({dict_val.key_2.subkey_23.subsubkey_232}[0] / tsm-testfile-04)

   rf.extensions.pretty_print    ${dict_val}[key_2][subkey_23][dotted.key.name]     PARAMS-VERIFIKATION : ({dict_val}[key_2][subkey_23][dotted.key.name] / tsm-testfile-04)
   rf.extensions.pretty_print    ${dict_val.key_2.subkey_23}[dotted.key.name]       PARAMS-VERIFIKATION : ({dict_val.key_2.subkey_23}[dotted.key.name] / tsm-testfile-04)

   rf.extensions.pretty_print    ${I_am_a_new_int}     PARAMS-VERIFIKATION : ({I_am_a_new_int} / tsm-testfile-04)
   rf.extensions.pretty_print    ${I_am_a_new_str}     PARAMS-VERIFIKATION : ({I_am_a_new_str} / tsm-testfile-04)
   rf.extensions.pretty_print    ${I_am_a_new_None}    PARAMS-VERIFIKATION : ({I_am_a_new_None} / tsm-testfile-04)
   rf.extensions.pretty_print    ${I_am_a_new_dict}    PARAMS-VERIFIKATION : ({I_am_a_new_dict} / tsm-testfile-04)
   rf.extensions.pretty_print    ${I_am_a_new_list}    PARAMS-VERIFIKATION : ({I_am_a_new_list} / tsm-testfile-04)

