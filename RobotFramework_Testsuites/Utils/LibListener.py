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

import os
import RobotFramework_Testsuites
from RobotFramework_Testsuites.Config import CConfig
from .Events import dispatch
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from robot.parsing import SuiteStructureBuilder

class LibListener(object):
    '''
    Define some hook methods
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LISTENER_API_VERSION = 2
    
    def _start_suite(self, name, attrs):
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig = CConfig()
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath = ''
        if os.path.isfile(attrs['source']):
            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath = ''
            for item in attrs['source'].split(os.path.sep)[:-1]:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath += item + os.path.sep
        else:
            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath = attrs['source']
        os.chdir(RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestcasePath)
        
        if RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iSuiteCount == 0:
            
            from robot.running import TestSuiteBuilder
            from robot.model import SuiteVisitor
            '''
            This TestCasesCollect class collects all the testcases.
            '''
            class TestCasesCollect(SuiteVisitor):
                '''
                Collect test cases in testsuites
                '''

                def __init__(self):
                    self.testcases = []
                
                '''
                Overridden visit_test() method in SuiteVisitor object
                '''
                def visit_test(self, testcase):
                    self.testcases.append(testcase)
                    
            datasources = SuiteStructureBuilder.data_sources
            for source in datasources:
                try:
                    suiteBuilder = TestSuiteBuilder()
                    testsuite = suiteBuilder.build(source)
                    testcases = TestCasesCollect()
                    testsuite.visit(testcases)
                    RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iTotalTestcases += len(testcases.testcases)
                except:
                    logger.info("The directory %s contains no tests or tasks!!!" % (source))
                    pass
            BuiltIn().set_global_variable("${TOTALTESTCASES}", RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iTotalTestcases)
            
            if '${configfile}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1 = True
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sTestCfgFile = BuiltIn().get_variable_value('${CONFIG_FILE}')
            if '${variant}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.sConfigName = BuiltIn().get_variable_value('${VARIANT}')
            if '${swversion}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rMetaData.sVersionSW = BuiltIn().get_variable_value('${SW_VERSION}')
            if '${hwversion}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rMetaData.sVersionHW = BuiltIn().get_variable_value('${HW_VERSION}')
            if '${testversion}' in BuiltIn().get_variables()._keys:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rMetaData.sVersionTest = BuiltIn().get_variable_value('${TEST_VERSION}')
                
            try:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.loadCfg(RobotFramework_Testsuites.CTestsuitesCfg.oConfig)
            except:
                RobotFramework_Testsuites.CTestsuitesCfg.oConfig.bLoadedCfg = False
                pass
            
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iSuiteCount += 1
        BuiltIn().set_global_variable("${SUITECOUNT}", RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iSuiteCount)
        dispatch('scope_start', attrs['longname'])
        
    def _end_suite(self, name, attrs):
        if not RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel1:
            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel2 = False
            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel3 = False
            RobotFramework_Testsuites.CTestsuitesCfg.oConfig.rConfigFiles.sLevel4 = False
        dispatch('scope_end', attrs['longname'])
        
    def _start_test(self, name, attrs):
        RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iTestCount += 1
        BuiltIn().set_global_variable("${TESTCOUNT}", RobotFramework_Testsuites.CTestsuitesCfg.oConfig.iTestCount)
        dispatch('scope_start', attrs['longname'])
        
    def _end_test(self, name, attrs):
        dispatch('scope_end', attrs['longname'])
        