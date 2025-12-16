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
from RobotFramework_TestsuitesManagement.Utils.version import CVersion, StatusMessages

class CSetupKeywords(object):
    '''
This class defines the keywords for the setup and the teardown of testcases and testsuites.
    '''

    @keyword
    def testsuite_setup(self, testsuite_cfg_file=''):
        '''
This keyword loads the RobotFramework AIO configuration, checks the version of the RobotFramework AIO
and logs out the basic information about the test execution.

**Arguments:**

* ``testsuite_cfg_file``

  / *Condition*: required / *Type*: string /

  ``testsuite_cfg_file=''`` and variable ``config_file`` is not set RobotFramework AIO will check for configuration
  level 3, and level 4.

  ``testsuite_cfg_file`` is set with a <json_config_file_path> and variable ``config_file`` is not set RobotFramework AIO
  will load configuration level 2.

**Returns:**

* No return variable
        '''
        # levels description
        levels_info = {1 : "configuration file in command line",
                       2 : "variant name in command line",
                       3 : "configuration file in local config folder",
                       4 : "default configuration (fallback solution)"}
        if TM.CTestsuitesCfg.config_obj.config_level==TM.CConfigLevel.LEVEL_1:
            try:
                TM.CTestsuitesCfg.config_obj.load_config(TM.CTestsuitesCfg.config_obj)
            except:
                TM.CTestsuitesCfg.config_obj.is_cfg_loaded = False
                pass
        else:
            if testsuite_cfg_file != '':
                TM.CTestsuitesCfg.config_obj.config_level = TM.CConfigLevel.LEVEL_2
                TM.CTestsuitesCfg.config_obj.testsuite_config = testsuite_cfg_file
            try:
                TM.CTestsuitesCfg.config_obj.load_config(TM.CTestsuitesCfg.config_obj)
            except:
                if len(TM.CTestsuitesCfg.config_obj.loaded_cfg_log['error']) > 0:
                    for error_msg in TM.CTestsuitesCfg.config_obj.loaded_cfg_log['error']:
                        if str(error_msg) != '':
                            logger.error(error_msg)
                if len(TM.CTestsuitesCfg.config_obj.loaded_cfg_log['info']) > 0:
                    for info_msg in TM.CTestsuitesCfg.config_obj.loaded_cfg_log['info']:
                        if str(info_msg) != '':
                            logger.error(info_msg)
                sys.tracebacklimit = 0
                raise Exception(TM.CTestsuitesCfg.config_obj.loaded_cfg_log['unknown'])

        if not TM.CTestsuitesCfg.config_obj.is_cfg_loaded:
            if len(TM.CTestsuitesCfg.config_obj.loaded_cfg_log['error']) > 0:
                for error_msg in TM.CTestsuitesCfg.config_obj.loaded_cfg_log['error']:
                    if str(error_msg) != '':
                        logger.error(error_msg)
            if len(TM.CTestsuitesCfg.config_obj.loaded_cfg_log['info']) > 0:
                for info_msg in TM.CTestsuitesCfg.config_obj.loaded_cfg_log['info']:
                    if str(info_msg) != '':
                        logger.error(info_msg)
            sys.tracebacklimit = 0
            raise Exception(TM.CTestsuitesCfg.config_obj.loaded_cfg_log['unknown'])

        msg = f"Running with configuration level {TM.CTestsuitesCfg.config_obj.config_level.value} \
({levels_info[TM.CTestsuitesCfg.config_obj.config_level.value]})"
        if TM.CTestsuitesCfg.config_obj.config_level==TM.CConfigLevel.LEVEL_4:
            logger.warn(msg)
        else:
            logger.info(msg)

        TM.CTestsuitesCfg.config_obj.check_version()
        logger.info(f"Loaded configuration file '{TM.CTestsuitesCfg.config_obj.test_config_file}'")
        logger.info(f"Suite Path: '{TM.CTestsuitesCfg.config_obj.testcase_path}'")
        if TM.CTestsuitesCfg.config_obj.local_config != '':
            logger.info(f"Local config file: '{TM.CTestsuitesCfg.config_obj.local_config}'")
        logger.info(f"Number of test suites: {TM.CTestsuitesCfg.config_obj.suite_count}")
        logger.info(f"Total number of testcases: {TM.CTestsuitesCfg.config_obj.total_testcases}")

    @keyword
    def testsuite_teardown(self):
        '''
This keyword writes information about the testsuite result to the log files.
        '''
        suite_name = BuiltIn().get_variable_value('${SUITENAME}')
        suite_status = BuiltIn().get_variable_value('${SUITESTATUS}')
        suite_msg = BuiltIn().get_variable_value('${SUITEMESSAGE}')
        teardown_msg = f"SUITE '{suite_name}' finished with result '{suite_status}'"
        if suite_status == 'PASS':
            logger.info(teardown_msg)
        else:
            logger.info(f"{teardown_msg}, reason: {suite_msg}")

    @keyword
    def testcase_setup(self):
        '''
This keyword writes the number of counted tests to the log files.
        '''
        logger.info(f"Test Count: {TM.CTestsuitesCfg.config_obj.test_count}")

    @keyword
    def testcase_teardown(self):
        '''
This keyword writes information about the testcase result to the log files.
        '''
        test_name = BuiltIn().get_variable_value('${TESTNAME}')
        test_status = BuiltIn().get_variable_value('${TESTSTATUS}')
        test_msg = BuiltIn().get_variable_value('${TESTMESSAGE}')
        teardown_msg = f"TEST '{test_name}' finished with result '{test_status}'"
        if test_status == 'PASS':
            logger.info(teardown_msg)
        else:
            logger.info(f"{teardown_msg}, reason: {test_msg}")

class CGeneralKeywords(object):
    '''
Class to define general keywords, that have nothing to do with the setups and teardowns
of suites and tests.
    '''

    def __init__(self):
        # access to application configuration
        self.__tsm_app_config       = None
        self.__tsm_app_config_error = None
        # [] config / [X] key_words / [] verify_version / [] check_version
        try:
            self.__tsm_app_config = AppConfig()
        except Exception as ex:
            # Will be used when keyword (that requires this config) is executed.
            # No exit here!
            self.__tsm_app_config_error = f"{ex}"

    @keyword
    def get_config(self):
    # !!! TODO: A better distinction by name between the newly introduced application-specific configuration (AppConfig)
    # and the configuration that relates to the test (the variant configuration) would be desirable.
    # Maybe rename this keyword from 'get_config' to 'get_test_config'.
        '''
This get_config defines the ``Get Config`` keyword gets the current config object of RobotFramework AIO.

**Arguments:**

* No parameter is required

**Returns:**

* ``config_obj.config_params``

  / *Type*: json /
        '''
        return copy.deepcopy(TM.CTestsuitesCfg.config_obj.config_params)

    @keyword
    def load_json(self, json_file, level=1, variant='default'):
        '''
Loads a json file and returns a json object.

**Arguments:**

* ``json_file``

  / *Condition*: required / *Type*: string /

  The path of Json configuration file.

* ``level``

  / *Condition*: required / *Type*: int /

  Level = 1 -> loads the content of json_file.

  level != 1 -> loads the json file which is set with variant (likes loading config level2)

**Returns:**

* ``json_data``

  / *Type*: json /
        '''
        from os.path import abspath, dirname
        from JsonPreprocessor import CJsonPreprocessor
        json_file_dir = dirname(abspath(json_file))
        jpp_obj = CJsonPreprocessor()
        if level == 1:
            json_data = jpp_obj.jsonLoad(json_file)
            return json_data
        else:
            json_frist_level = jpp_obj.jsonLoad(json_file)
            if variant not in json_frist_level:
                logger.error(f"The variant: {variant} is not correct!")
                return {}
            json_file_loaded = json_file_dir + json_frist_level[variant]['path'] + '/' + json_frist_level[variant]['name']
            json_data = jpp_obj.jsonLoad(json_file_loaded)
            return json_data


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
        # Keyword wrapper for high level method '``check_version``' defined in CVersion.py
        version = CVersion()
        result  = version.check_version(min_version, max_version, reference_version, ext_logger=logger, status_messages=status_messages) # 'logger' is the one from robot.api
        # In case of an error, 'result' contains the outcome of this error (abort of test execution), that is not very detailed.
        # More helpful details are provided by the last error. Therefore, we return this one.
        # Relevant only in case of 'run_keyword_and_ignore_error' is used. Otherwise the exception is already thrown.
        last_error = version.get_last_error()
        if last_error:
            result = last_error
        return result
    # A corrsponding keyword wrapper for the low level method '``verify_version``' is currently not implemented (and most probably will not be required).

    @keyword
    def get_status_messages(self):
        """
Returns the StatusMessages object.
        """
        status_messages      = StatusMessages()
        dict_status_messages = status_messages.get_messages_dict()
        return dict_status_messages

