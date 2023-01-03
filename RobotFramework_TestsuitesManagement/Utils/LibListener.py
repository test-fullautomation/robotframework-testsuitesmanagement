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
import re
import RobotFramework_TestsuitesManagement
from RobotFramework_TestsuitesManagement.Config import CConfig

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
        RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig = CConfig()
        RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestcasePath = ''
        if os.path.isfile(data.source):
            RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestcasePath = ''
            for item in data.source.split(os.path.sep)[:-1]:
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestcasePath += item + os.path.sep
        else:
            RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestcasePath = data.source
        os.chdir(RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestcasePath)
        
        if RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.iSuiteCount == 0:
            test_suite = None
            test_suite = data
            while test_suite.parent != None:
                test_suite = test_suite.parent

            for k, v in BuiltIn().get_variables()._keys.items():
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.lBuitInVariables.append(re.match('.+{(.+)}', v)[1])

            RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sRootSuiteName = test_suite.name
            RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.iTotalTestcases = test_suite.test_count

            if '${localconfig}' in BuiltIn().get_variables()._keys:
                if re.match('^\s*$', BuiltIn().get_variable_value('${LOCAL_CONFIG}')):
                    logger.error("local_config input must not be empty!!!")
                else:
                    RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sLocalConfig = BuiltIn().get_variable_value('${LOCAL_CONFIG}').strip()
            elif 'ROBOT_LOCAL_CONFIG' in os.environ:
                if os.path.isfile(os.environ['ROBOT_LOCAL_CONFIG']):
                    RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sLocalConfig = os.environ['ROBOT_LOCAL_CONFIG']
                else:
                    logger.error(f"The local configuration file {os.environ['ROBOT_LOCAL_CONFIG']} which set in ROBOT_LOCAL_CONFIG variable is not exist!!!")
                    BuiltIn().unknown(f"The local configuration file {os.environ['ROBOT_LOCAL_CONFIG']} is not exist!!!")

            if '${variant}' in BuiltIn().get_variables()._keys:
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sConfigName = BuiltIn().get_variable_value('${VARIANT}')
            if '${versioncheck}' in BuiltIn().get_variables()._keys:
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.bVersionCheck = BuiltIn().get_variable_value('${VERSION_CHECK}')
            if '${swversion}' in BuiltIn().get_variables()._keys:
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rMetaData.sVersionSW = BuiltIn().get_variable_value('${SW_VERSION}')
            if '${hwversion}' in BuiltIn().get_variables()._keys:
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rMetaData.sVersionHW = BuiltIn().get_variable_value('${HW_VERSION}')
            if '${testversion}' in BuiltIn().get_variables()._keys:
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rMetaData.sVersionTest = BuiltIn().get_variable_value('${TEST_VERSION}')
            if '${configfile}' in BuiltIn().get_variables()._keys:
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1 = True
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel4 = False
                RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestCfgFile = BuiltIn().get_variable_value('${CONFIG_FILE}').strip()
                try:
                    RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.loadCfg(RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig)
                except:
                    RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.bLoadedCfg = False
                    pass
                    
        RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.iSuiteCount += 1
        BuiltIn().set_global_variable("${SUITECOUNT}", RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.iSuiteCount)
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
        RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel2 = False
        RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel3 = False
        if not RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1:
            RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestCfgFile = ''
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
        RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.iTestCount += 1
        BuiltIn().set_global_variable("${TESTCOUNT}", RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.iTestCount)
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
        