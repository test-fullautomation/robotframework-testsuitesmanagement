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

from inspect import stack
import os
import regex
import RobotFramework_TestsuitesManagement as TM
from RobotFramework_TestsuitesManagement.Config import CConfig

from .Events import dispatch
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from robot.parsing import SuiteStructureBuilder

class LibListener(object):
    '''
This ``LibListener`` class defines the hook methods.

* ``_start_suite`` hooks to every starting testsuite of robot run.

* ``_end_suite`` hooks to every ending testsuite of robot run.

* ``_start_test`` hooks to every starting test case of robot run.

* ``_end_test`` hooks to every ending test case of robot run.
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LISTENER_API_VERSION = 3

    def _start_suite(self, data, result):
        '''
This _start_suite method hooks to every starting testsuite of robot run.

**Arguments:**

* ``data``

  / *Condition*: required / *Type*: dict /

  The data of current robot run.

* ``result``

  / *Condition*: required / *Type*: any /

**Returns:**

* No return variable
        '''
        TM.CTestsuitesCfg.oConfig = CConfig()
        TM.CTestsuitesCfg.oConfig.sTestcasePath = ''
        if os.path.isfile(data.source.__str__()):
            TM.CTestsuitesCfg.oConfig.sTestcasePath = ''
            for item in data.source.__str__().split(os.path.sep)[:-1]:
                TM.CTestsuitesCfg.oConfig.sTestcasePath += item + os.path.sep
        elif os.path.isdir(data.source.__str__()):
            TM.CTestsuitesCfg.oConfig.sTestcasePath = data.source.__str__()
        if TM.CTestsuitesCfg.oConfig.sTestcasePath != '':
            os.chdir(TM.CTestsuitesCfg.oConfig.sTestcasePath)

        if TM.CTestsuitesCfg.oConfig.iSuiteCount == 0:
            test_suite = None
            test_suite = data
            while test_suite.parent != None:
                test_suite = test_suite.parent

            for k, v in BuiltIn().get_variables()._keys.items():
                TM.CTestsuitesCfg.oConfig.lBuitInVariables.append(regex.match('.+{(.+)}', v)[1])

            TM.CTestsuitesCfg.oConfig.sRootSuiteName = test_suite.name
            TM.CTestsuitesCfg.oConfig.iTotalTestcases = test_suite.test_count

            if '${localconfig}' in BuiltIn().get_variables()._keys:
                if regex.match('^\s*$', BuiltIn().get_variable_value('${LOCAL_CONFIG}')):
                    CConfig.sLoadedCfgLog['error'] = "Local_config input must not be empty!!!"
                    logger.error(CConfig.sLoadedCfgLog['error'])
                else:
                    TM.CTestsuitesCfg.oConfig.sLocalConfig = os.path.abspath(BuiltIn().get_variable_value('${LOCAL_CONFIG}').strip())

            elif 'ROBOT_LOCAL_CONFIG' in os.environ:
                localConfigFile = os.path.abspath(os.environ['ROBOT_LOCAL_CONFIG'])
                if os.path.isfile(localConfigFile):
                    TM.CTestsuitesCfg.oConfig.sLocalConfig = localConfigFile
                else:
                    TM.CTestsuitesCfg.oConfig.bLoadedCfg = False
                    CConfig.sLoadedCfgLog['error'] = f"The local configuration file {localConfigFile} which set in ROBOT_LOCAL_CONFIG variable, does not exist!!!"
                    logger.error(CConfig.sLoadedCfgLog['error'])

            if '${variant}' in BuiltIn().get_variables()._keys:
                TM.CTestsuitesCfg.oConfig.sConfigName = BuiltIn().get_variable_value('${VARIANT}').strip()
            if '${versionsw}' in BuiltIn().get_variables()._keys:
                TM.CTestsuitesCfg.oConfig.rMetaData.sVersionSW = BuiltIn().get_variable_value('${VERSION_SW}')
            if '${versionhw}' in BuiltIn().get_variables()._keys:
                TM.CTestsuitesCfg.oConfig.rMetaData.sVersionHW = BuiltIn().get_variable_value('${VERSION_HW}')
            if '${versiontest}' in BuiltIn().get_variables()._keys:
                TM.CTestsuitesCfg.oConfig.rMetaData.sVersionTest = BuiltIn().get_variable_value('${VERSION_TEST}')
            if '${configfile}' in BuiltIn().get_variables()._keys:
                TM.CTestsuitesCfg.oConfig.configLevel = TM.CConfigLevel.LEVEL_1
                TM.CTestsuitesCfg.oConfig.sTestCfgFile = os.path.abspath(BuiltIn().get_variable_value('${CONFIG_FILE}').strip())

        TM.CTestsuitesCfg.oConfig.iSuiteCount += 1
        BuiltIn().set_global_variable("${SUITECOUNT}", TM.CTestsuitesCfg.oConfig.iSuiteCount)
        dispatch('scope_start', data.longname)

    def _end_suite(self, data, result):
        '''
This _end_suite method hooks to every ending testsuite of robot run.

**Arguments:**

* ``data``

  / *Condition*: required / *Type*: dict /

  The data of current robot run.

* ``result``

  / *Condition*: required / *Type*: any /

**Returns:**

* No return variable
        '''
        if TM.CTestsuitesCfg.oConfig.configLevel != TM.CConfigLevel.LEVEL_1:
            TM.CTestsuitesCfg.oConfig.sTestCfgFile = ''
        TM.CTestsuitesCfg.oConfig.configLevel = TM.CConfigLevel.LEVEL_4
        dispatch('scope_end', data.longname)

    def _start_test(self, data, result):
        '''
This _start_test method hooks to every starting test case of robot run.

**Arguments:**

* ``data``

  / *Condition*: required / *Type*: dict /

  The data of current robot run.

* ``result``

  / *Condition*: required / *Type*: any /

**Returns:**

* No return variable
        '''
        TM.CTestsuitesCfg.oConfig.iTestCount += 1
        BuiltIn().set_global_variable("${TESTCOUNT}", TM.CTestsuitesCfg.oConfig.iTestCount)
        dispatch('scope_start', data.longname)

    def _end_test(self, data, result):
        '''
This _end_test hooks to every ending test case of robot run.

**Arguments:**

* ``data``

  / *Condition*: required / *Type*: dict /

  The data of current robot run.

* ``result``

  / *Condition*: required / *Type*: any /

**Returns:**

* No return variable
        '''
        dispatch('scope_end', data.longname)
