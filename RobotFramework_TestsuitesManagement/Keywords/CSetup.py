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

import copy
import sys

import RobotFramework_TestsuitesManagement as TM
from robot.api.deco import keyword
from robot.api import logger

from robot.libraries.BuiltIn import BuiltIn




class CSetupKeywords(object):
    '''
This class defines the keywords for the setup and the teardown of testcases and testsuites.
    '''

    @keyword
    def testsuite_setup(self, sTestsuiteCfgFile=''):
        '''
This keyword loads the RobotFramework AIO configuration, checks the version of the RobotFramework AIO
and logs out the basic information about the test execution.

**Arguments:**

* ``sTestsuiteCfgFile``

  / *Condition*: required / *Type*: string /

  ``sTestsuiteCfgFile=''`` and variable ``config_file`` is not set RobotFramework AIO will check for configuration
  level 3, and level 4.

  ``sTestsuiteCfgFile`` is set with a <json_config_file_path> and variable ``config_file`` is not set RobotFramework AIO
  will load configuration level 2.

**Returns:**

* No return variable
        '''
        # levels description
        levelsInfo = {1 : "configuration file in command line",
                      2 : "variant name in command line",
                      3 : "configuration file in local config folder",
                      4 : "default configuration (fallback solution)"}
        if TM.CTestsuitesCfg.oConfig.configLevel==TM.CConfigLevel.LEVEL_1:
            try:
                TM.CTestsuitesCfg.oConfig.loadCfg(TM.CTestsuitesCfg.oConfig)
            except:
                TM.CTestsuitesCfg.oConfig.bLoadedCfg = False
                pass
        else:
            if sTestsuiteCfgFile != '':
                TM.CTestsuitesCfg.oConfig.configLevel = TM.CConfigLevel.LEVEL_2
                TM.CTestsuitesCfg.oConfig.sTestSuiteCfg = sTestsuiteCfgFile
            try:
                TM.CTestsuitesCfg.oConfig.loadCfg(TM.CTestsuitesCfg.oConfig)
            except:
                if len(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['error']) > 0:
                    for errorMsg in TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['error']:
                        if str(errorMsg) != '':
                            logger.error(errorMsg)
                if len(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']) > 0:
                    for infoMsg in TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']:
                        if str(infoMsg) != '':
                            logger.error(infoMsg)
                sys.tracebacklimit = 0
                raise Exception(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['unknown'])

        if not TM.CTestsuitesCfg.oConfig.bLoadedCfg:
            if len(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['error']) > 0:
                for errorMsg in TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['error']:
                    if str(errorMsg) != '':
                        logger.error(errorMsg)
            if len(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']) > 0:
                for infoMsg in TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']:
                    if str(infoMsg) != '':
                        logger.error(infoMsg)
            sys.tracebacklimit = 0
            raise Exception(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['unknown'])

        msg = f"Running with configuration level {TM.CTestsuitesCfg.oConfig.configLevel.value} \
({levelsInfo[TM.CTestsuitesCfg.oConfig.configLevel.value]})"
        if TM.CTestsuitesCfg.oConfig.configLevel==TM.CConfigLevel.LEVEL_4:
            logger.warn(msg)
        else:
            logger.info(msg)

        TM.CTestsuitesCfg.oConfig.verifyVersion()
        logger.info(f"Loaded configuration file '{TM.CTestsuitesCfg.oConfig.sTestCfgFile}'")
        logger.info(f"Suite Path: '{TM.CTestsuitesCfg.oConfig.sTestcasePath}'")
        if TM.CTestsuitesCfg.oConfig.sLocalConfig != '':
            logger.info(f"Local config file: '{TM.CTestsuitesCfg.oConfig.sLocalConfig}'")
        logger.info(f"Number of test suites: {TM.CTestsuitesCfg.oConfig.iSuiteCount}")
        logger.info(f"Total number of testcases: {TM.CTestsuitesCfg.oConfig.iTotalTestcases}")

    @keyword
    def testsuite_teardown(self):
        '''
This keyword writes information about the testsuite result to the log files.
        '''
        suiteName = BuiltIn().get_variable_value('${SUITENAME}')
        suiteStatus = BuiltIn().get_variable_value('${SUITESTATUS}')
        suiteMsg = BuiltIn().get_variable_value('${SUITEMESSAGE}')
        teardownMsg = f"SUITE '{suiteName}' finished with result '{suiteStatus}'"
        if suiteStatus == 'PASS':
            logger.info(teardownMsg)
        else:
            logger.info(f"{teardownMsg}, reason: {suiteMsg}")

    @keyword
    def testcase_setup(self):
        '''
This keyword writes the number of counted tests to the log files.
        '''
        logger.info(f"Test Count: {TM.CTestsuitesCfg.oConfig.iTestCount}")

    @keyword
    def testcase_teardown(self):
        '''
This keyword writes information about the testcase result to the log files.
        '''
        testName = BuiltIn().get_variable_value('${TESTNAME}')
        testStatus = BuiltIn().get_variable_value('${TESTSTATUS}')
        testMsg = BuiltIn().get_variable_value('${TESTMESSAGE}')
        teardownMsg = f"TEST '{testName}' finished with result '{testStatus}'"
        if testStatus == 'PASS':
            logger.info(teardownMsg)
        else:
            logger.info(f"{teardownMsg}, reason: {testMsg}")

class CGeneralKeywords(object):
    '''
This CGeneralKeywords class defines the keywords which will be using in RobotFramework AIO test script.

``Get Config`` keyword gets the current config object of robot run.

``Load Json`` keyword loads json file then return json object.

In case new robot keyword is required, it will be defined and implemented in this class.
    '''

    @keyword
    def get_config(self):
        '''
This get_config defines the ``Get Config`` keyword gets the current config object of RobotFramework AIO.

**Arguments:**

* No parameter is required

**Returns:**

* ``oConfig.oConfigParams``

  / *Type*: json /
        '''
        return copy.deepcopy(TM.CTestsuitesCfg.oConfig.oConfigParams)

    @keyword
    def load_json(self, jsonfile, level=1, variant='default'):
        '''
Loads a json file and returns a json object.

**Arguments:**

* ``jsonfile``

  / *Condition*: required / *Type*: string /

  The path of Json configuration file.

* ``level``

  / *Condition*: required / *Type*: int /

  Level = 1 -> loads the content of jsonfile.

  level != 1 -> loads the json file which is set with variant (likes loading config level2)

**Returns:**

* ``oJsonData``

  / *Type*: json /
        '''
        from os.path import abspath, dirname
        from JsonPreprocessor import CJsonPreprocessor
        jsonFileDir = dirname(abspath(jsonfile))
        oJsonPreprocessor = CJsonPreprocessor()
        if level == 1:
            oJsonData = oJsonPreprocessor.jsonLoad(jsonfile)
            return oJsonData
        else:
            oJsonFristLevel = oJsonPreprocessor.jsonLoad(jsonfile)
            if variant not in oJsonFristLevel:
                logger.error(f"The variant: {variant} is not correct!")
                return {}
            jsonFileLoaded = jsonFileDir + oJsonFristLevel[variant]['path'] + '/' + oJsonFristLevel[variant]['name']
            oJsonData = oJsonPreprocessor.jsonLoad(jsonFileLoaded)
            return oJsonData
