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

from inspect import stack
import os
import RobotFramework_Testsuites
from RobotFramework_Testsuites.Config import CConfig

from .Events import dispatch
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from robot.parsing import SuiteStructureBuilder

class LibListener(object):
    '''
**Class: LibListener**

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
**Method: _start_suite**

   This _start_suite method hooks to every starting testsuite of robot run.

**Arguments:**

* ``data``

   / *Condition*: required / *Type*: dict

   The data of current robot run.

* ``result``

   / *Condition*: required / *Type*: Any

**Returns:**

* No return variable
        '''
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig = CConfig()
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath = ''
        if os.path.isfile(data.source):
            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath = ''
            for item in data.source.split(os.path.sep)[:-1]:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath += item + os.path.sep
        else:
            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath = data.source
        os.chdir(RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath)
        
        if RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iSuiteCount == 0:
            test_suite = None
            test_suite = data
            while test_suite.parent != None:
                test_suite = test_suite.parent

            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sRootSuiteName = test_suite.name
            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iTotalTestcases = test_suite.test_count
            
            if '${variant}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sConfigName = BuiltIn().get_variable_value('${VARIANT}')
            if '${swversion}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rMetaData.sVersionSW = BuiltIn().get_variable_value('${SW_VERSION}')
            if '${hwversion}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rMetaData.sVersionHW = BuiltIn().get_variable_value('${HW_VERSION}')
            if '${testversion}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rMetaData.sVersionTest = BuiltIn().get_variable_value('${TEST_VERSION}')
            if '${configfile}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1 = True
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel4 = False
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestCfgFile = BuiltIn().get_variable_value('${CONFIG_FILE}')
                try:
                    RobotFramework_Testsuites.CTestsuitesCfg.oConfig.loadCfg(RobotFramework_Testsuites.CTestsuitesCfg.oConfig)
                except:
                    RobotFramework_Testsuites.CTestsuitesCfg.oConfig.bLoadedCfg = False
                    pass
                    
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iSuiteCount += 1
        BuiltIn().set_global_variable("${SUITECOUNT}", RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iSuiteCount)
        dispatch('scope_start', data.longname)
        
    def _end_suite(self, data, result):
        '''
**Method: _end_suite**

   This _end_suite method hooks to every ending testsuite of robot run.

**Arguments:**

* ``data``

   / *Condition*: required / *Type*: dict

   The data of current robot run.

* ``result``

   / *Condition*: required / *Type*: Any

**Returns:**

* No return variable
        '''
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel2 = False
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel3 = False
        if not RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1:
            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestCfgFile = ''
        dispatch('scope_end', data.longname)
        
    def _start_test(self, data, result):
        '''
**Method: _start_test**

   This _start_test method hooks to every starting test case of robot run.

**Arguments:**

* ``data``

   / *Condition*: required / *Type*: dict

   The data of current robot run.

* ``result``

   / *Condition*: required / *Type*: Any

**Returns:**

* No return variable
        '''
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iTestCount += 1
        BuiltIn().set_global_variable("${TESTCOUNT}", RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iTestCount)
        dispatch('scope_start', data.longname)
        
    def _end_test(self, data, result):
        '''
**Method: _end_test**

   This _end_test hooks to every ending test case of robot run.

**Arguments:**

* ``data``

   / *Condition*: required / *Type*: dict

   The data of current robot run.

* ``result``

   / *Condition*: required / *Type*: Any

**Returns:**

* No return variable
        '''
        dispatch('scope_end', data.longname)
        