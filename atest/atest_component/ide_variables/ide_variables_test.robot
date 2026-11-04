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
*** Settings ***
Library    Collections
Library    ../../resources/atest_libs.py    AS    testlibs
Library    ./robotcode/robot/diagnostics/library_doc.py    AS    robotcode_analysis

*** Variables ***
${ANALYSIS_MODULE}    robotcode.robot.diagnostics.library_doc
${VARIANTS_FILE}      ${CURDIR}/../../general_config/testsuites_config.json

*** Test Cases ***
Test IDE Variables Static Analysis Variant
    ${vars}=      robotcode_analysis.Get Variables Doc    ${VARIANTS_FILE}    variant_2
    Should Be Equal    ${vars['CONFIG'].Project}    G3g-variant_2
    Should Be Equal    ${vars}[gGlobalString]       This is a string
    Should Be Equal    ${vars['dSUT'].tuner.fm.frequency.nMax_MHz}    ${vars}[dSUT][tuner][fm][frequency][nMax_MHz]
    Dictionary Should Not Contain Key    ${vars}[CONFIG][params]    global
    Should Be Equal    ${vars}[CONFIG.Project]    G3g-variant_2
    Should Be Equal    ${vars}[dSUT.tuner.fm.frequency.nMax_MHz]    ${vars}[dSUT][tuner][fm][frequency][nMax_MHz]

Test IDE Variables Static Analysis Unknown Variant
    Run Keyword And Expect Error    *The variant 'unknown' is not defined*
    ...    robotcode_analysis.Get Variables Doc    ${VARIANTS_FILE}    unknown

Test IDE Variables Test Execution
    # test executions started by RobotCode have loaded the analysis modules, but do not analyze
    [Setup]       Evaluate    sys.modules.setdefault($ANALYSIS_MODULE, None)    modules=sys
    ${vars}=      Evaluate    RobotFramework_TestsuitesManagement.ide_variables.get_variables($VARIANTS_FILE)
    ...           modules=RobotFramework_TestsuitesManagement.ide_variables
    Should Be Empty    ${vars}
    ${check}=    Subprocess Execution    ./testsuites/ide_variables_runtime.robot
    Log    ${check}
    Should Be Equal    ${check}    Passed
    [Teardown]    Evaluate    sys.modules.pop($ANALYSIS_MODULE, None)    modules=sys
