#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
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

# import RobotFramework_Testsuites
from robot.api.deco import keyword
from robot.api import logger

# from RobotFramework_Testsuites.Config import CConfig # Sphinx fix to be verified
from Config import CConfig # Sphinx fix to be verified

from lxml import etree

from robot.libraries.BuiltIn import BuiltIn




class CSetupKeywords(object):
    '''
    Definition setup keywords
    '''
    
    @keyword
    def testsuite_setup(self, sTestsuiteCfgFile=''):
        if not RobotFramework_Testsuites.CTestsuitesCfg.oConfig.bLoadedCfg:
            BuiltIn().unknown("Loading of %s" %(CConfig.sLoadedCfgError))
            return
        else:
            if not RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1:
                if sTestsuiteCfgFile != '':
                    if RobotFramework_Testsuites.CTestsuitesCfg.oConfig.bConfigLoaded:
                        logger.error('Configuration \"%s\" was already loaded for this Robot run!!!' \
                            %(RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestCfgFile))
                        BuiltIn().unknown('Configuration file \"%s\" could not be loaded due to \"%s\" is loaded before' \
                            %(sTestsuiteCfgFile, RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestCfgFile))
                    else:
                        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel2 = True
                        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestSuiteCfg = sTestsuiteCfgFile
                        try:
                            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.loadCfg(RobotFramework_Testsuites.CTestsuitesCfg.oConfig)
                        except Exception as error:
                            BuiltIn().unknown("Loading of %s" %(CConfig.sLoadedCfgError))
                else:
                    if not RobotFramework_Testsuites.CTestsuitesCfg.oConfig.bConfigLoaded:
                        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel3 = True
                        try:
                            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.loadCfg(RobotFramework_Testsuites.CTestsuitesCfg.oConfig)
                        except Exception as error:
                            BuiltIn().unknown("Loading of %s" %(CConfig.sLoadedCfgError))
            else:
                if sTestsuiteCfgFile != '':
                    logger.warn('The configuration level 1 is set for this Robot run! \nThe configuration \"%s\" is using as highest priority' \
                        %(RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestCfgFile))

        if RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1:
            logger.info('Running with configuration level: 1')
        elif RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel2:
            logger.info('Running with configuration level: 2')
        elif RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel3:
            logger.info('Running with configuration level: 3')
        else:
            logger.info('Running with configuration level: 4')

        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.verifyRbfwVersion()
        logger.info('Suite Path: %s' %(RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath))
        logger.info('CfgFile Path: %s' %(RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestCfgFile))
        logger.info('Suite Count: %s' %(RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iSuiteCount))
        
    @keyword
    def testsuite_teardown(self):
        logger.info('testsuite_teardown: Will be implemented later')
        
    @keyword
    def testcase_setup(self):
        logger.info('Test Count: %s' %(RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iTestCount))
        
    @keyword
    def testcase_teardown(self):
        logger.info('testcase_teardown: Will be implemented later')
        
    @keyword
    def update_config(self, sCfgFile):
        CConfig.updateCfg(sCfgFile)
        
class CGeneralKeywords(object):
    '''
    Definition setup keywords
    '''
     
    @keyword
    def get_config(self):
        '''
        oConfigParams: is the dictionary consist of some configuration params which 
        are return to user from get_config_params keyword
        '''
        return copy.deepcopy(RobotFramework_Testsuites.CTestsuitesCfg.oConfig.oConfigParams)
    
    @keyword
    def load_json(self, jsonfile, level=1, variant='default'):
        '''
        This keyword uses to load json file then return json object.
           - Level = 1 -> loads the content of jsonfile.
           - level != 1 -> loads the json file which is set with variant (likes loading
             config level2)
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
                logger.error('The variant: %s is not correct' % variant)
                return {}
            jsonFileLoaded = jsonFileDir + oJsonFristLevel[variant]['path'] + '/' + oJsonFristLevel[variant]['name']
            oJsonData = oJsonPreprocessor.jsonLoad(jsonFileLoaded)
            return oJsonData
            