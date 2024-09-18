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
from robot.conf import RobotSettings
from tabulate import tabulate


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
                        if errorMsg.strip() != '':
                            logger.error(errorMsg)
                if len(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']) > 0:
                    for infoMsg in TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['info']:
                        if infoMsg.strip() != '':
                            logger.error(infoMsg)
                BuiltIn().unknown(TM.CTestsuitesCfg.oConfig.sLoadedCfgLog['unknown'])

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
        TM.CTestsuitesCfg.oConfig.verifyVersion()
        # -- levels description
        levelsInfo = {1 : "configuration file in command line",
                    2 : "variant name in command line",
                    3 : "configuration file in local config folder",
                    4 : "default configuration (fallback solution)"}
        tableRows = []
        # -- 1. Common information (small extract from what is available in RobotSettings())
        robotSettings = RobotSettings()
        logLevel = robotSettings.log_level
        tableRows.append(["[COMMON]", "Log level", f"{logLevel}"])
        output = robotSettings.output
        tableRows.append(["[COMMON]", "Output", f"{output}"])
        log = robotSettings.log
        tableRows.append(["[COMMON]", "Log", f"{log}"])
        report = robotSettings.report
        tableRows.append(["[COMMON]", "Report", f"{report}"])
        splitLog = robotSettings.split_log
        tableRows.append(["[COMMON]", "Split log", f"{splitLog}"])
        include = robotSettings.include
        if include is not None:
            tableRows.append(["[COMMON]", "Include", f"{include}"])
        exclude = robotSettings.exclude
        if exclude is not None:
            tableRows.append(["[COMMON]", "Exclude", f"{exclude}"])
        pythonPath = robotSettings.pythonpath
        if len(pythonPath)>0:
            tableRows.append(["[COMMON]", "Python path", f"{pythonPath}"])
        elif os.getenv('RobotPythonPath'):
            tableRows.append(["[COMMON]", "Python path", f"{os.getenv('RobotPythonPath')}"])
        statusRc = robotSettings.status_rc
        tableRows.append(["[COMMON]", "Status rc", f"{statusRc}"])
        removeKeywords = robotSettings.remove_keywords
        if len(removeKeywords)>0:
            tableRows.append(["[COMMON]", "Remove keywords", f"{removeKeywords}"])
        # -- 2. Testsuite setup information
        iConfigLevel = TM.CTestsuitesCfg.oConfig.configLevel.value
        sConfigLevelInfo = levelsInfo[iConfigLevel]
        tableRows.append(["[TESTSUITE SETUP]", "Configuration level", f"{iConfigLevel} ({sConfigLevelInfo})"])
        tableRows.append(["[TESTSUITE SETUP]", "Variant configuration file", f"{TM.CTestsuitesCfg.oConfig.sTestSuiteCfg}"])
        tableRows.append(["[TESTSUITE SETUP]", "Loaded configuration file", f"{TM.CTestsuitesCfg.oConfig.sTestCfgFile}"])
        if TM.CTestsuitesCfg.oConfig.sLocalConfig.strip()!='':
            tableRows.append(["[TESTSUITE SETUP]", "Local configuration file", f"{TM.CTestsuitesCfg.oConfig.sLocalConfig}"])
        tableRows.append(["[TESTSUITE SETUP]", "Suite Path", f"{TM.CTestsuitesCfg.oConfig.sTestcasePath}"])
        tableRows.append(["[TESTSUITE SETUP]", "Test suite number", f"{TM.CTestsuitesCfg.oConfig.iSuiteCount}"])
        tableRows.append(["[TESTSUITE SETUP]", "Number of testcases", f"{TM.CTestsuitesCfg.oConfig.iTotalTestcases}"])
        # -- 3. Metadata information
        suiteMetadata = BuiltIn().get_variables()['&{SUITE_METADATA}']
        for key, value in suiteMetadata.items():
            tableRows.append(["[METADATA]", f"{key}", f"{value}"])
        # -- 4. Configuration parameters information
        userConfig = TM.CTestsuitesCfg.oConfig.oConfigParams['params']['global']
        maxChar = 150
        for key, value in userConfig.items():
            strValue = f"{value}"
            if len(strValue) > maxChar:
                value = strValue[:maxChar] + " ..."
            tableRows.append(["[TESTSUITE CONFIG]", f"{key}", f"{value}"])
        # Convert to table and log
        headers = ["Information Type", "Parameter Name", "Value"]
        parameterTable = tabulate(tableRows, headers, tablefmt="fancy_grid")
        BuiltIn().log("\n" + parameterTable, level="INFO", html=False, console=True)

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
    def dump_config_info(self):
        # -- 1. Testsuites configuration - General information
        generalConfig = BuiltIn().get_variable_value('${CONFIG}')
        userConfig = TM.CTestsuitesCfg.oConfig.oConfigParams['params']['global']
        header1 = ['<font face="Arial" color="#FF0000" size="3"><b>General configuration information:</b></font>', '']
        header2 = ['<font face="Arial" color="#FF0000" size="3"><b>Configuration Parameters information:</b></font>', '']
        generalData = []
        testsuiteData = []
        for key, value in generalConfig.items():
            if len(value)>0:
                generalData.append([f'<font face="Arial" color="#00008B" size="3"><b>{key}</b></font>', f'<i><font color="#006400" size="3"><b>{value}</i></b></font>'])
        for key, value in userConfig.items():
            testsuiteData.append([f'<font face="Arial" color="#00008B" size="3"><b>{key}</b></font>', f'<i><font color="#006400" size="3"><b>{value}</i></b></font>'])
        generalDataTable = tabulate(generalData, header1, tablefmt="plain")
        BuiltIn().log("\n" + generalDataTable, level="INFO", html=True, console=False)

        # -- 2. Testsuite configuration - Parameter information
        testsuiteDataTable = tabulate(testsuiteData, header2, tablefmt="plain")
        BuiltIn().log("\n" + testsuiteDataTable, level="INFO", html=True, console=False)
        return TM.CTestsuitesCfg.oConfig.oConfigParams

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
