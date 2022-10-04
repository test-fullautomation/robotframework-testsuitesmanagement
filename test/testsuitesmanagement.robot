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

*** Settings ***

# Robot Framework Built-In libraries
Library    Collections
Library    BuiltIn

# own libraries
Library    RobotFramework_Testsuites    WITH NAME    testsuites
Library    RobotframeworkExtensions.Collection    WITH NAME    rf.extensions
Library    ./libs/CTestsuitesTestlib.py

# testsuite_setup from Robotframework AIO
Suite Setup    testsuites.testsuite_setup    ./config/main_config.json

Documentation    Self test of testsuites management

# TODO: needs to be clarified if this shall be valid or not:  Metadata    version     1234
Metadata    testversion     5678


*** Variables ***


*** Test Cases ***

# **************************************************************************************************************

Testsuites_Management_Test_01
   [Documentation]    Set config file

   ${bSuccess}    ${sResult}   set_config_file_as_reference   ./config/testconfig.json
   log    bSuccess: ${bSuccess}    console=yes
   log    sResult: ${sResult}    console=yes
   # [Expectation] Selected configuration file must exist
   should_be_equal    ${bSuccess}    ${True}

# --------------------------------------------------------------------------------------------------------------

Testsuites_Management_Test_02
   [Documentation]    Check maximum version

   ${sMaximumVersion}   ${bSuccess}    ${sResult}   get_maximum_version
   log    sMaximumVersion: ${sMaximumVersion}    console=yes
   log    bSuccess: ${bSuccess}    console=yes
   log    sResult: ${sResult}    console=yes

   # [Expectation] It must be possible to parse the maximum version from selected configuration file
   should_be_equal    ${bSuccess}    ${True}
   # [Expectation] The parsed maximum version must be the same than the suite metadata tells us
   # TODO: needs to be clarified if this shall be valid or not:
   # should_be_equal    ${sMaximumVersion}    ${SUITE METADATA}[version]
   # alternatively hard coded:
   should_be_equal    ${sMaximumVersion}    0.5.2

# --------------------------------------------------------------------------------------------------------------

Testsuites_Management_Test_03
   [Documentation]    Check own value defined in metadata of this file

   log    meta data testversion: ${SUITE METADATA}[testversion]    console=yes

   # [Expectation] Value like defined in 'Settings' section of this file
   # '${SUITE METADATA}[testversion]' is of type string, therefore also 5678 needs to be defined as string (NOT in this way: ${5678})
   should_be_equal   ${SUITE METADATA}[testversion]    5678

# --------------------------------------------------------------------------------------------------------------

Testsuites_Management_Test_04
   [Documentation]    Check global param defined in configuration file

   log    config testparam: ${testparam}    console=yes

   # [Expectation] Value like defined in 'Settings' section of this file
   # 'testparam' is of type integer, therefore also 123 needs to be defined as integer (in this way: ${123})
   should_be_equal   ${testparam}    ${123}

# --------------------------------------------------------------------------------------------------------------

# >>>>> to be continued

# --------------------------------------------------------------------------------------------------------------


