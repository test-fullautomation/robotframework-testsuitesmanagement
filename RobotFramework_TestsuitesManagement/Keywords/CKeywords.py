#  Copyright 2020-2025 Robert Bosch GmbH
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

from RobotFramework_TestsuitesManagement.Utils.app_config import AppConfig
from RobotFramework_TestsuitesManagement.Utils.CVersion import CVersion
from RobotFramework_TestsuitesManagement.Utils.CVersion import StatusMessages

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

        TM.CTestsuitesCfg.oConfig.checkVersion()
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
Class to define general keywords, that have nothing to do with the setups and teardowns
of suites and tests.
    '''

    def __init__(self):
        # access to application configuration
        self.__tsm_app_config       = None
        self.__tsm_app_config_error = None
        # [] CConfig / [X] CKeywords / [] verifyVersion / [] checkVersion
        try:
            self.__tsm_app_config = AppConfig()
        except Exception as ex:
            # Will be used when keyword (that requires this config) is executed.
            # No exit here!
            self.__tsm_app_config_error = f"{ex}"

    @keyword
    def get_config(self):
# !!! TODO: Distinguish between test configuration and app configuration !!!
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


    @keyword
    def is_robotframework_aio(self):
        """
Returns
* ``True``: RobotFramework AIO is installed
* ``False``: RobotFramework AIO is not installed (= standalone installation of TestsuitesManagement)
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.is_robotframework_aio()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_package_context_file(self):
        """
Returns path and name of package context file
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_package_context_file()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_reference_version(self):
        """
Returns the version number used as reference for version checks. The reference is either the RobotFramework AIO
or the TestsuitesManagement, depending on what is installed.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_reference_version()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_reference_version_date(self):
        """
Returns the version date belonging to the reference. The reference is either the RobotFramework AIO
or the TestsuitesManagement, depending on what is installed.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_reference_version_date()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_reference_app_name(self):
        """
Returns the name of the reference application. The reference is either the RobotFramework AIO
or the TestsuitesManagement, depending on what is installed.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_reference_app_name()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_reference_installer_location(self):
        """
Returns the location of the reference installer. The reference is either the RobotFramework AIO
or the TestsuitesManagement, depending on what is installed.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_reference_installer_location()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_tsm_version(self):
        """
Returns the version of the TestsuitesManagement.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_tsm_version()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_tsm_version_date(self):
        """
Returns the version date of the TestsuitesManagement.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_tsm_version_date()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_tsm_app_name(self):
        """
Returns the application name of the TestsuitesManagement.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_tsm_app_name()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_tsm_installer_location(self):
        """
Returns the location of the TestsuitesManagement installer.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_tsm_installer_location()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_bundle_version(self):
        """
Returns the version of the entire RobotFramework AIO bundle.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_bundle_version()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_bundle_version_date(self):
        """
Returns the version date of the entire RobotFramework AIO bundle.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_bundle_version_date()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_bundle_name(self):
        """
Returns the name of the entire RobotFramework AIO bundle.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_bundle_name()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def get_bundle_installer_location(self):
        """
Returns the location of the installer of the entire RobotFramework AIO bundle.
        """
        if self.__tsm_app_config:
            return self.__tsm_app_config.get_bundle_installer_location()
        raise Exception(f"Configuration exception: {self.__tsm_app_config_error}")

    @keyword
    def check_version(self, min_version=None, max_version=None, reference_version=None, status_messages=None):
        """
This keyword executes a version check, min_version and max_version are checked against the reference_version.
        """
        # Keyword wrapper for high level method '``checkVersion``' defined in CVersion.py
        version = CVersion()
        result  = version.checkVersion(min_version, max_version, reference_version, ext_logger=logger, status_messages=status_messages) # 'logger' is the one from robot.api
        return result
    # A corrsponding keyword wrapper for the low level method '``verifyVersion``' is currently not implemented (and most probably will not be required).

    @keyword
    def get_status_messages(self):
        """
Returns the StatusMessages object.
        """
        status_messages      = StatusMessages()
        dict_status_messages = status_messages.get_messages_dict()
        return dict_status_messages

