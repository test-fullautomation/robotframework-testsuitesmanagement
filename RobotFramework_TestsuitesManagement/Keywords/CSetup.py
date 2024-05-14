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
import os

import RobotFramework_TestsuitesManagement as TM
from robot.api.deco import keyword
from robot.api import logger

from robot.libraries.BuiltIn import BuiltIn




class CSetupKeywords(object):
    '''
This CSetupKeywords class uses to define the setup keywords which are using in suite setup and teardown of
robot test script.

``Testsuite Setup`` keyword loads the RobotFramework AIO configuration, checks the version of RobotFramework AIO,
and logs out the basic information of the robot run.

``Testsuite Teardown`` keyword currently do nothing, it's defined here for future requirements.

``Testcase Setup`` keyword currently do nothing, it's defined here for future requirements.

``Testcase Teardown`` keyword currently do nothing, it's defined here for future requirements.
    '''

    @keyword
    def testsuite_setup(self, sTestsuiteCfgFile=''):
        '''
This testsuite_setup defines the ``Testsuite Setup`` which is used to loads the RobotFramework AIO configuration,
checks the version of RobotFramework AIO, and logs out the basic information of the robot run.

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
        if not TM.CTestsuitesCfg.oConfig.bLoadedCfg:
            if len(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['error']) > 0:
                for errorMsg in TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['error']:
                    if errorMsg.strip() != '':
                        logger.error(errorMsg)
            if len(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']) > 0:
                for infoMsg in TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']:
                    if infoMsg.strip() != '':
                        logger.error(infoMsg)
            BuiltIn().unknown(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['unknown'])
            return
        if not TM.CTestsuitesCfg.oConfig.rConfigFiles.bLevel1:
            if sTestsuiteCfgFile != '':
                TM.CTestsuitesCfg.oConfig.rConfigFiles.bLevel2 = True
                TM.CTestsuitesCfg.oConfig.rConfigFiles.bLevel4 = False
                TM.CTestsuitesCfg.oConfig.sTestSuiteCfg = os.path.abspath(sTestsuiteCfgFile)
            else:
                TM.CTestsuitesCfg.oConfig.rConfigFiles.bLevel3 = True
                TM.CTestsuitesCfg.oConfig.rConfigFiles.bLevel4 = False
            try:
                TM.CTestsuitesCfg.oConfig.loadCfg(TM.CTestsuitesCfg.oConfig)
            except:
                if len(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['error']) > 0:
                    for errorMsg in TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['error']:
                        if errorMsg.strip() != '':
                            logger.error(errorMsg)
                if len(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']) > 0:
                    for infoMsg in TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']:
                        if infoMsg.strip() != '':
                            logger.error(infoMsg)
                BuiltIn().unknown(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['unknown'])

        if TM.CTestsuitesCfg.oConfig.rConfigFiles.bLevel1:
            logger.info('Running with configuration level 1')
        elif TM.CTestsuitesCfg.oConfig.rConfigFiles.bLevel2:
            logger.info('Running with configuration level 2')
        elif TM.CTestsuitesCfg.oConfig.rConfigFiles.bLevel3:
            logger.info('Running with configuration level 3')
        else:
            logger.warn("Running with configuration level 4!")

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
This testsuite_teardown defines the ``Testsuite Teardown`` keyword, currently this keyword does nothing,
it's defined here for future requirements.
        '''
        logger.info('testsuite_teardown: Will be implemented later')

    @keyword
    def testcase_setup(self):
        '''
This testcase_setup defines the ``Testcase Setup`` keyword, currently this keyword does nothing,
it's defined here for future requirements.
        '''
        logger.info(f"Test Count: {TM.CTestsuitesCfg.oConfig.iTestCount}")

    @keyword
    def testcase_teardown(self):
        '''
This testcase_teardown defines the ``Testcase Teardown`` keyword, currently this keyword does nothing,
it's defined here for future requirements.
        '''
        logger.info('testcase_teardown: Will be implemented later')

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
        import os
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
