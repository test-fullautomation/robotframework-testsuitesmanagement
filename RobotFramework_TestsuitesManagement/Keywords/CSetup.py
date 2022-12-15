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

import copy

import RobotFramework_TestsuitesManagement
from robot.api.deco import keyword
from robot.api import logger

from RobotFramework_TestsuitesManagement.Config import CConfig

from lxml import etree

from robot.libraries.BuiltIn import BuiltIn




class CSetupKeywords(object):
    '''
**Class: CSetupKeywords**

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
**Method: testsuite_setup**

   This testsuite_setup defines the ``Testsuite Setup`` which is used to loads the RobotFramework AIO configuration, 
   checks the version of RobotFramework AIO, and logs out the basic information of the robot run.

**Arguments:**

* ``sTestsuiteCfgFile``

   / *Condition*: required / *Type*: string

   ``sTestsuiteCfgFile=''`` and vairiable ``config_file`` is not set Robotframework AIO will check for configuration
    level 3, and level 4.

   ``sTestsuiteCfgFile`` is set with a <json_config_file_path> and vairiable ``config_file`` is not set Robotframework AIO 
   will load configuration level 2.

**Returns:**

* No return variable
        '''
        if not RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.bLoadedCfg:
            BuiltIn().unknown(CConfig.sLoadedCfgError)
            return
        else:
            if not RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1:
                if sTestsuiteCfgFile != '':
                    RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel2 = True
                    RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel4 = False
                    RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestSuiteCfg = sTestsuiteCfgFile
                    try:
                        RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.loadCfg(RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig)
                    except Exception as error:
                        BuiltIn().unknown(CConfig.sLoadedCfgError)
                else:
                    RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel3 = True
                    RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel4 = False
                    try:
                        RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.loadCfg(RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig)
                    except Exception as error:
                        BuiltIn().unknown(CConfig.sLoadedCfgError)
            else:
                logger.warn(f"The configuration level 1 is set for this Robot run! \nThe configuration '{RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestCfgFile}' \
is using as highest priority")

        if RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1:
            logger.info('Running with configuration level: 1')
        elif RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel2:
            logger.info('Running with configuration level: 2')
            if RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.bConfigLoaded:
                logger.info(f"The parameters in '{RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestCfgFile}' \
will be added into configuration object")
        elif RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.rConfigFiles.sLevel3:
            logger.info('Running with configuration level: 3')
            if RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.bConfigLoaded:
                logger.info(f"The parameters in '{RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestCfgFile}' \
will be added into configuration object")
        else:
            logger.info('Running with configuration level: 4')

        RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.verifyRbfwVersion()
        logger.info(f"Suite Path: {RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestcasePath}")
        logger.info(f"CfgFile Path: {RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sTestCfgFile}")
        logger.info(f"Suite Count: {RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.iSuiteCount}")
        logger.info(f"Total testcases in TestSuite {RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.sRootSuiteName} \
is: {RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.iTotalTestcases}")
        
    @keyword
    def testsuite_teardown(self):
        '''
**Method: testsuite_teardown**

   This testsuite_teardown defines the ``Testsuite Teardown`` keyword, currently this keyword does nothing, 
   it's defined here for future requirements.
        '''
        logger.info('testsuite_teardown: Will be implemented later')
        
    @keyword
    def testcase_setup(self):
        '''
**Method: testcase_setup**

   This testcase_setup defines the ``Testcase Setup`` keyword, currently this keyword does nothing, 
   it's defined here for future requirements.
        '''
        logger.info(f"Test Count: {RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.iTestCount}")
        
    @keyword
    def testcase_teardown(self):
        '''
**Method: testcase_teardown**

   This testcase_teardown defines the ``Testcase Teardown`` keyword, currently this keyword does nothing, 
   it's defined here for future requirements.
        '''
        logger.info('testcase_teardown: Will be implemented later')
        
    @keyword
    def update_config(self, sCfgFile):
        '''
**Method: update_config**

   This update_config defines the ``Update Config`` keyword which is using update the configuration object 
   of RobotFramework AIO.

**Arguments:**

* ``sCfgFile``

   / *Condition*: required / *Type*: string

   The path of Json configuration file.

**Returns:**

* No return variable
        '''
        CConfig.updateCfg(sCfgFile)
        
class CGeneralKeywords(object):
    '''
**Class: CGeneralKeywords**

   This CGeneralKeywords class defines the keywords which will be using in RobotFramework AIO test script.

   ``Get Config`` keyword gets the current config object of robot run.

   ``Load Json`` keyword loads json file then return json object.

   In case new robot keyword is required, it will be defined and implemented in this class.
    '''
     
    @keyword
    def get_config(self):
        '''
**Method: get_config**

   This get_config defines the ``Get Config`` keyword gets the current config object of RobotFramework AIO.

**Arguments:**

* No parameter is required

**Returns:**

* ``oConfig.oConfigParams``

   / *Type*: json /
        '''
        return copy.deepcopy(RobotFramework_TestsuitesManagement.CTestsuitesCfg.oConfig.oConfigParams)
    
    @keyword
    def load_json(self, jsonfile, level=1, variant='default'):
        '''
**Method: load_json**

   This load_json defines the ``Load Json`` keyword which loads json file then return json object.

**Arguments:**

* ``jsonfile``

   / *Condition*: required / *Type*: string

   The path of Json configuration file.

* ``level``

   / *Condition*: required / *Type*: int

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
                logger.error(f"The variant: {variant} is not correct")
                return {}
            jsonFileLoaded = jsonFileDir + oJsonFristLevel[variant]['path'] + '/' + oJsonFristLevel[variant]['name']
            oJsonData = oJsonPreprocessor.jsonLoad(jsonFileLoaded)
            return oJsonData
            