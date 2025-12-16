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
#################################################################################
#
# File: CConfig.py
# Initially created by Mai Dinh Nam Son (RBVH/ECM11) / Nov-2020
# Based on TML Framework automation concept
#
# 2021-06-25: Mai Dinh Nam Son (RBVH/ECM1)
#   - Adds CJsonDotDict class to convert json to dotdict object
#   - Converts json config to dotdict config object
#################################################################################


import regex
import os
import platform
import ctypes
import socket
import json
import copy
from jsonschema import validate
from builtins import staticmethod

import RobotFramework_TestsuitesManagement as TM
from RobotFramework_TestsuitesManagement.Utils.struct import CStruct
from RobotFramework_TestsuitesManagement.Utils.version import CVersion, enVersionCheckResult
from RobotFramework_TestsuitesManagement.Utils.app_config import AppConfig

from PythonExtensionsCollection.String.CString import CString

from JsonPreprocessor import CJsonPreprocessor
from robot.api import logger
from robot.version import get_full_version, get_version
from robot.libraries.BuiltIn import BuiltIn
from robot.utils.dotdict import DotDict
import pathlib


class CConfig():
    '''
Defines the properties of configuration and holds the identified config files.

The loading configuration method is divided into 4 levels: level1 has the highest priority, level4 has the lowest priority.

**Level1:** Defined in command line

**Level2:** Read from content of JSON config file

   .. code:: json

      {
         "default": {
            "name": "robot_config.jsonp",
            "path": "./config/"
         },
         "variant_0": {
            "name": "robot_config.jsonp",
            "path": "./config/"
         },
         "variant_1": {
            "name": "robot_config_variant_1.jsonp",
            "path": "./config/"
         },
            ...
            ...
      }

   According to the ``ConfigName``, RobotFramework_TestsuitesManagement will choose the corresponding config file.
   ``"./config/"`` indicates the relative path to json config file.

**Level3:** Read in testsuite folder: ``/config/robot_config.jsonp``

**Level4:** Read from RobotFramework AIO installation folder:

    ``/RobotFramework/defaultconfig/robot_config.jsonp``
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    __single          = None

    def __new__(classtype, *args, **kwargs):
        '''
Makes the CConfig class to singleton.

Checks to see if a __single exists already for this class. Compare class types instead of just looking
for None so that subclasses will create their own __single objects.
        '''
        if classtype != type(classtype.__single):
            classtype.__single = object.__new__(classtype)
        return classtype.__single

    def __init__(self):
        self.root_suite_name   = ''
        self.config_params     = {}
        self.config_name       = 'default'
        self.variable_pattern  = r'^\p{L}[\p{L}\p{Nd}_]*$'
        self.project_name      = None
        self.total_testcases   = 0
        self.suite_count       = 0
        self.test_count        = 0
        self.is_cfg_loaded     = True
        self.loaded_cfg_log    = {"info" : [], "error" : [], "unknown": ''}
        self.testsuite_config  = ''
        self.test_config_file  = ''
        self.testcase_path     = ''
        self.max_version       = None
        self.min_version       = None
        self.local_config      = ''
        self.buitin_variables  = []
        self.config_level      = TM.CConfigLevel.LEVEL_4
        self.meta_data         = CStruct(
                                    version_sw = None,
                                    version_hw     = None,
                                    version_test   = None,
                                    robfw_version  = get_full_version('Robot Framework')
                                )

        # Common configuration parameters
        self.welcome_string  = None
        self.target_name     = None

        # access to application configuration
        self.__tsm_app_config       = None
        self.__tsm_app_config_error = None

        # [X] CConfig / [] key_words / [] verify_version / [] check_version
        try:
            self.__tsm_app_config = AppConfig()
        except Exception as ex:
            # Will be used when method (that requires this config) is executed.
            # No exit here!
            self.__tsm_app_config_error = f"{ex}"

    def __merge_dicts(self, main_dict: dict, update_dict: dict) -> dict:
        """
Merge update_dict which contains updated data to main_dict.

**Arguments:**

* ``main_dict``

  / *Condition*: required / *Type*: dict /

* ``update_dict``

  / *Condition*: required / *Type*: dict /

**Returns:**

* ``main_dict``

  / *Type*: dict /

  Return main_dict which contains update data in update_dict.
        """
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in main_dict:
                self.__merge_dicts(main_dict[key], value)
            else:
                main_dict[key] = value
        return main_dict

    @staticmethod
    def load_config(self):
        '''
This load_config method uses to load configuration's parameters from json files.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        # Detect a configuration level and get the config_obj.test_config_file to handle
        if self.config_level == TM.CConfigLevel.LEVEL_1:
            # Configuration level 1, the config_obj.test_config_file was already set in the lib_listener.py module
            if self.config_name != 'default':
                self.is_cfg_loaded = False
                self.loaded_cfg_log['error'].append("Redundant settings detected in command line: Parameter 'variant' \
is used together with parameter 'config_file'.")
                self.loaded_cfg_log['info'].append("---> It is not possible to use both together, because they belong \
to the same feature (the variant selection).")
                self.loaded_cfg_log['info'].append("---> Please remove one of them.")
                self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                raise Exception(f"The test execution will be aborted!")

            if self.test_config_file == '':
                self.is_cfg_loaded = False
                self.loaded_cfg_log['error'].append("The config_file input parameter is empty!!!")
                self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                raise Exception(f"The test execution will be aborted!")
        else:
            if self.config_level==TM.CConfigLevel.LEVEL_2:
                # Configuration level 2, the config_obj.test_config_file will be detected in method __load_config_file_level2()
                self.is_cfg_loaded = self.__load_config_file_level2()
                if not self.is_cfg_loaded:
                    # self.loaded_cfg_log 'error' or 'info' are already set in method self.__load_config_file_level2()
                    self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                    raise Exception(f"The test execution will be aborted!")
            else:
                # Configuration level 3
                if r'${variant}' in BuiltIn().get_variables():
                    self.is_cfg_loaded = False
                    self.loaded_cfg_log['error'].append(f"Not able to get a configuration for variant '{self.config_name}' \
because of a variant configuration file is not available.")
                    if self.testsuite_config != '':
                        self.loaded_cfg_log['error'].append(f"In file: '{self.testsuite_config}'")
                    elif self.test_config_file != '':
                        self.loaded_cfg_log['error'].append(f"In file: '{self.test_config_file}'")
                    self.loaded_cfg_log['info'].append("---> A variant configuration file must be available when executing \
robot with configuration level 2.")
                    self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                    raise Exception(f"The test execution will be aborted!")
                # Detect the config_obj.test_config_file the configuration level 3
                if os.path.isdir(self.testcase_path + 'config'):
                    self.config_level = TM.CConfigLevel.LEVEL_3
                    config_folder = CString.NormalizePath(f"{self.testcase_path}/config")
                    suite_file_name = BuiltIn().get_variable_value('${SUITE_SOURCE}').split(os.path.sep)[-1]
                    json_file_1 = f"{config_folder}/{os.path.splitext(suite_file_name)[0]}.jsonp"
                    json_file_2 = f"{config_folder}/{os.path.splitext(suite_file_name)[0]}.json"
                    if not os.path.isfile(json_file_1) and not os.path.isfile(json_file_2):
                        json_file_1    = f"{config_folder}/robot_config.jsonp"
                        json_file_2    = f"{config_folder}/robot_config.json" # still supported alternative extension

                    if os.path.isfile(json_file_1) and os.path.isfile(json_file_2):
                        self.is_cfg_loaded = False
                        self.loaded_cfg_log['error'].append("Configuration file duplicate detected (both extensions: 'jsonp' and 'json')!")
                        self.loaded_cfg_log['info'].append(f"* file 1: '{json_file_1}'")
                        self.loaded_cfg_log['info'].append(f"* file 2: '{json_file_2}'")
                        self.loaded_cfg_log['info'].append(f"Please decide which one to keep and which one to remove. Both together are not allowed.") 
                        self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                        raise Exception(f"The test execution will be aborted!")
                    elif os.path.isfile(json_file_1):
                        self.test_config_file = json_file_1
                    elif os.path.isfile(json_file_2):
                        self.test_config_file = json_file_2
                    else: # meaning: if not os.path.isfile(json_file_1) and not os.path.isfile(json_file_2)
                        # Pre-condition of the configuration level 3 didn't match, set default configuration level 4.
                        self.config_level = TM.CConfigLevel.LEVEL_4
                if self.config_level==TM.CConfigLevel.LEVEL_4:
                    # Handling the configuration level 4
                    default_config=str(pathlib.Path(__file__).parent.absolute() / "robot_config.jsonp")
                    self.test_config_file = default_config
            self.test_config_file = CString.NormalizePath(self.test_config_file)
        # Handling the config_obj.test_config_file file to load the configuration object
        if not os.path.isfile(self.test_config_file):
            self.is_cfg_loaded = False
            self.loaded_cfg_log['error'].append(f"Did not find configuration file: '{self.test_config_file}'!")
            self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
            raise Exception(f"The test execution will be aborted!")
        robot_core_data = BuiltIn().get_variables()
        jpp_obj = CJsonPreprocessor(syntax="python")
        try:
            json_config_data = jpp_obj.jsonLoad(self.test_config_file)
        except Exception as error:
            self.is_cfg_loaded = False
            check = False
            for line in str(error).splitlines():
                if "In file:" in line: # Check is self.test_config_file path info already present in error?
                    check = True
                self.loaded_cfg_log['error'].append(f"{line}")
            if not check:
                self.loaded_cfg_log['error'].append(f"In file: {self.test_config_file}")
            self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
            raise Exception(f"The test execution will be aborted!")
        # Handling local configuration
        if self.local_config != '':
            self.local_config = CString.NormalizePath(self.local_config)
            try:
                local_config_obj = jpp_obj.jsonLoad(self.local_config)
            except Exception as error:
                self.is_cfg_loaded = False
                self.loaded_cfg_log['error'].append(str(error))
                self.loaded_cfg_log['error'].append(f"Loading local config failed with file: {self.local_config}")
                self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                raise Exception(f"The test execution will be aborted!")
            local_config = True
            if "WelcomeString" in local_config_obj:
                self.loaded_cfg_log['error'].append(f"Loading local config failed with file: {self.local_config}")
                self.loaded_cfg_log['info'].append("---> The mandatory 'WelcomeString' element of configuration file is found in local config file")
                self.loaded_cfg_log['info'].append("---> Wrong local config file was chosen, please check!!!")
                local_config = False
            elif "default" in local_config_obj:
                self.loaded_cfg_log['error'].append(f"Loading local config failed with file: {self.local_config}")
                self.loaded_cfg_log['info'].append("---> The variant 'default' element of the variant configuration in the configuration level 2 is found in local config file")
                self.loaded_cfg_log['info'].append("---> Wrong local config file was chosen, please check!!!")
                local_config = False
            else:
                json_config_data = self.__merge_dicts(json_config_data, local_config_obj)

            if not local_config:
                self.is_cfg_loaded = False
                # Loading local configuration failed, the 'error' and 'info' are added above
                self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                raise Exception(f"The test execution will be aborted!")

        json_schema = True
        try:
            schema_file=str(pathlib.Path(__file__).parent.absolute() / "configuration_schema.json")
            with open(schema_file) as f:
                json_schema_cfg = json.load(f)
        except Exception as err:
            json_schema = False
            self.is_cfg_loaded = False
            self.loaded_cfg_log['error'].append(f"Could not parse configuration JSON schema file: '{str(err)}'")
            self.loaded_cfg_log['unknown'] = "Failed to parse JSON schema file. The test execution will be aborted!"
            raise Exception(f"The test execution will be aborted!")

        if json_schema:
            try:
                validate(instance=json_config_data, schema=json_schema_cfg)
            except Exception as error:
                self.is_cfg_loaded = False
                if error.validator == 'additionalProperties':
                    self.loaded_cfg_log['error'].append(f"Verification against JSON schema failed: '{error.message}'.")
                    self.loaded_cfg_log['error'].append("Please put the additional params into 'params': { 'global': {...}")
                    self.loaded_cfg_log['error'].append(f"In file: '{self.test_config_file}'")
                elif error.validator == 'required':
                    param = regex.search("('[A-Za-z0-9]+')", error.message)
                    if param[0] == "'global'":
                        self.loaded_cfg_log['error'].append(f"Required parameter {param[0]} is missing under 'params' in file '{self.test_config_file}'.")
                    elif param is not None:
                        self.loaded_cfg_log['error'].append(f"Required parameter {param[0]} is missing in file '{self.test_config_file}'.")
                    else:
                        self.loaded_cfg_log['error'].append(f"Required parameter {error.message} is missing in file '{self.test_config_file}'.")
                    self.loaded_cfg_log['error'].append("JSON schema validation failed!")
                else:
                    errParam = error.path.pop()
                    self.loaded_cfg_log['error'].append(f"Parameter '{errParam}' with invalid value found in JSON configuration file!")
                    self.loaded_cfg_log['error'].append(f"Reason: {error.message}")
                    self.loaded_cfg_log['error'].append(f"In file: '{self.test_config_file}'")
                self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                raise Exception(f"The test execution will be aborted!")

        self.project_name = json_config_data['Project']
        self.target_name = json_config_data['TargetName']
        self.welcome_string = json_config_data['WelcomeString']
        if ("Maximum_version" in json_config_data) and json_config_data["Maximum_version"] != None:
            self.max_version = json_config_data["Maximum_version"]
            # Check the format of Maximum_version value
            # This will be done later again (by TM.CTestsuitesCfg.config_obj.check_version() in key_words).
            # But it is also plausible to do the check already here (as early as possible).
            # Consequence is that the error messages have to be maintained at two different positions in the code (redundancy).
            # Can this be merged anyway?
            try:
                CVersion.tuple_version(self.max_version)
            except Exception as error:
                self.loaded_cfg_log['error'].append(f"Maximum_version: {error}")
                self.loaded_cfg_log['error'].append(f"In configuration: '{self.test_config_file}'")
                self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                raise Exception(f"The test execution will be aborted!")

        if ("Minimum_version" in json_config_data) and json_config_data["Minimum_version"] != None:
            self.min_version = json_config_data["Minimum_version"]
            # Check the format of Minimum_version value
            # This will be done later again (by TM.CTestsuitesCfg.config_obj.check_version() in key_words).
            # But it is also plausible to do the check already here (as early as possible).
            # Consequence is that the error messages have to be maintained at two different positions in the code (redundancy).
            # Can this be merged anyway?
            try:
                CVersion.tuple_version(self.min_version)
            except Exception as error:
                self.loaded_cfg_log['error'].append(f"Minimum_version: {error}")
                self.loaded_cfg_log['error'].append(f"In configuration: '{self.test_config_file}'")
                self.loaded_cfg_log['unknown'] = "Not possible to load the test configuration. The test execution will be aborted!"
                raise Exception(f"The test execution will be aborted!")

        suite_metadata = BuiltIn().get_variables()['&{SUITE_METADATA}']
        # Set metadata at top level
        BuiltIn().set_suite_metadata("project", self.project_name, top=True)
        BuiltIn().set_suite_metadata("machine", self.__get_machine_name(), top=True)
        BuiltIn().set_suite_metadata("tester", self.__get_user_name(), top=True)
        BuiltIn().set_suite_metadata("testtool", self.meta_data.robfw_version, top=True)

        if self.__tsm_app_config:
            reference_version  = self.__tsm_app_config.get_reference_version()
            reference_app_name = self.__tsm_app_config.get_reference_app_name()
            BuiltIn().set_suite_metadata("reference_version", reference_version, top=True)
            BuiltIn().set_suite_metadata("reference_app_name", reference_app_name, top=True)
        else:
            self.loaded_cfg_log['error'].append(self.__tsm_app_config_error)
            self.loaded_cfg_log['unknown'] = "Execution will be aborted because of a critical version check issue!"
            raise Exception(f"Execution will be aborted because it's not possible to load the application configuration")

        if not ("version_sw" in suite_metadata and self.meta_data.version_sw == None):
            BuiltIn().set_suite_metadata("version_sw", self.meta_data.version_sw, top=True)
        if not ("version_hw" in suite_metadata and self.meta_data.version_hw == None):
            BuiltIn().set_suite_metadata("version_hw", self.meta_data.version_hw, top=True)
        if not ("version_test" in suite_metadata and self.meta_data.version_test == None):
            BuiltIn().set_suite_metadata("version_test", self.meta_data.version_test, top=True)

        self.config_params = copy.deepcopy(json_config_data)

        self.__update_global_variable()
        try:
            del json_config_data['params']['global']
        except:
            pass

        json_dotdict = DotDict(json_config_data)
        BuiltIn().set_global_variable("${CONFIG}", json_dotdict)
        if len(jpp_obj.dUpdatedParams) > 0:
            for param in jpp_obj.dUpdatedParams:
                logger.info(f"The parameter '{param}' is updated")

    def __set_global_variable(self, key, value):
        '''
This method set RobotFramework AIO global variable from config object.

**Arguments:**

* ``key``

   / *Condition*: required / *Type*: string /

   key is set as global variable of RobotFramework AIO, user can call ${<key>} in test script.

* ``value``

   / *Condition*: required / *Type*: <variant datatypes> /

**Returns:**

* No return variable
        '''
        if not regex.match(self.variable_pattern, key):
            self.loaded_cfg_log['error'].append(f"Variable name '{key}' is invalid. Expected format: '{self.variable_pattern}' (letters, digits, underscores)")
            self.loaded_cfg_log['error'].append(f"Please check variable '{key}' in params['global'] in the configuration file '{self.test_config_file}'")
            raise Exception(f"The test execution will be aborted!")
        k = key
        v = value
        if isinstance(v, dict):
            json_dotdict = DotDict(v)
            BuiltIn().set_global_variable(f"${{{k.strip()}}}", json_dotdict)
        elif isinstance(v, list):
            tmp_list = []
            for item in v:
                if isinstance(item, dict):
                    json_dotdict = DotDict(item)
                    tmp_list.append(json_dotdict)
                else:
                    tmp_list.append(item)
            BuiltIn().set_global_variable(f"${{{k.strip()}}}", tmp_list)
        else:
            BuiltIn().set_global_variable(f"${{{k.strip()}}}", v)

    def __update_global_variable(self):
        '''
This method updates preprocessor and global params to global variable of RobotFramework AIO.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        reserved_keyword = ['Settings', 'Variables', 'Keywords', 'Comments', 'Documentation', 'Metadata']
        if 'params' in self.config_params and 'global' in self.config_params['params']:
            for k,v in self.config_params['params']['global'].items():
                if k in reserved_keyword:
                    self.loaded_cfg_log['error'].append(f"'{k}' is a reserved keyword in Robot Framework and cannot be used as parameter name.")
                    self.loaded_cfg_log['unknown'] = "A parameter name conflicted with Robot Framework's reserved keywords. The test execution will be aborted!"
                    raise Exception(f"The test execution will be aborted!")
                if k in self.buitin_variables:
                    continue
                try:
                    self.__set_global_variable(k, v)
                except Exception as error:
                    self.loaded_cfg_log['error'].append(error)
                    raise Exception(f"The test execution will be aborted!")

    def __del__(self):
        '''
This destructor method.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        pass

    def __load_config_file_level2(self) -> bool:
        '''
This __load_config_file_level2 method loads configuration in case config_level is TM.CConfigLevel.LEVEL_2.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        if self.testsuite_config.startswith('.../'):
            testsuite_config_start = self.testsuite_config
            self.testsuite_config = self.testsuite_config[4:]
            if os.path.exists(CString.NormalizePath('./' + self.testsuite_config)):
                self.testsuite_config = './' + self.testsuite_config
            else:
                found_testsuite_cfg = False
                for i in range(0, 30):
                    self.testsuite_config = '../' + self.testsuite_config
                    if os.path.exists(CString.NormalizePath(self.testsuite_config)):
                        found_testsuite_cfg = True
                        break
                if not found_testsuite_cfg:
                    self.loaded_cfg_log['error'].append("Testsuite management - Loading configuration level 2 failed!")
                    self.loaded_cfg_log['error'].append(f"Could not find the variant configuration file: '{testsuite_config_start}'")
                    return False
        jpp_obj = CJsonPreprocessor(syntax="python")
        self.testsuite_config = CString.NormalizePath(self.testsuite_config)
        try:
            suite_config = jpp_obj.jsonLoad(self.testsuite_config)
        except Exception as error:
            self.is_cfg_loaded = False
            check = False
            for line in str(error).splitlines():
                if "In file:" in line: # Checking is self.testsuite_config path info already present in error?
                    check = True
                self.loaded_cfg_log['error'].append(f"{line}")
            if not check:
                self.loaded_cfg_log['error'].append(f"In file: {self.testsuite_config}")
            return False
        list_of_variants = ''
        for item in list(suite_config.keys()):
            list_of_variants = list_of_variants + f"'{item}', "
        if not regex.match(r'^[a-zA-Z0-9.\u0080-\U0010FFFF\_\-\:@\$]+$', self.config_name):
            self.loaded_cfg_log['error'].append("Testsuite management - Loading configuration level 2 failed!")
            self.loaded_cfg_log['error'].append(f"The variant name '{self.config_name}' is invalid.")
            self.loaded_cfg_log['error'].append(f"Please find the suitable variant in this list: {list_of_variants}")
            self.loaded_cfg_log['error'].append(f"In file: '{self.testsuite_config}'")
            return False

        if self.config_name not in suite_config:
            self.loaded_cfg_log['error'].append("Testsuite management - Loading configuration level 2 failed!")
            self.loaded_cfg_log['error'].append(f"The variant '{self.config_name}' is not defined in '{os.path.abspath(self.testsuite_config)}'.")
            self.loaded_cfg_log['error'].append(f"Please find the suitable variant in this list: {list_of_variants}")
            return False

        try:
            self.test_config_file = suite_config[self.config_name]['name']
            test_config_dir = suite_config[self.config_name]['path']
            if regex.match(r'^\.+/*.*', test_config_dir):
                test_config_dir = os.path.dirname(self.testsuite_config) + '/' + test_config_dir + '/'
        except:
            self.loaded_cfg_log['error'].append("Testsuite management - Loading configuration level 2 failed!")
            self.loaded_cfg_log['error'].append(f"The 'name' or 'path' property is not defined for the variant '{self.config_name}'.")
            self.loaded_cfg_log['error'].append(f"In file: '{os.path.abspath(self.testsuite_config)}'")
            return False
        if self.test_config_file.strip() == '':
            self.loaded_cfg_log['error'].append("Testsuite management - Loading configuration level 2 failed!")
            self.loaded_cfg_log['error'].append(f"The configuration file name of variant '{self.config_name}' must not be empty.")
            self.loaded_cfg_log['error'].append(f"In file: '{os.path.abspath(self.testsuite_config)}'")
            return False
        
        self.test_config_file = test_config_dir + self.test_config_file
        return True

    @staticmethod
    def __get_machine_name():
        '''
This __get_machine_name method gets current machine name which is running the test.

**Arguments:**

* No input parameter is required

**Returns:**

* ``machine_name``

   / *Type*: string /
        '''
        machine_name = ''
        # Allows windows system access only in windows systems
        if platform.system().lower()!="windows":
            try:
                machine_name = socket.gethostname()
            except:
                pass
        else:
            try:
                machine_name = os.getenv("COMPUTERNAME",'')
            except:
                pass

        return machine_name

    @staticmethod
    def __get_user_name():
        '''
This __get_user_name method gets current account name login to run the test.

**Arguments:**

* No input parameter is required

**Returns:**

* ``user_name``

   / *Type*: string /
        '''
        user_name = ''
        # Allows windows system access only in windows systems
        if platform.system().lower()!="windows":
            try:
                user_name = os.getenv("USER","")
            except:
                pass
        else:
            try:
                get_user_name_ex = ctypes.windll.secur32.GetUserNameExW
                name_display = 3

                size = ctypes.pointer(ctypes.c_ulong(0))
                get_user_name_ex(name_display, None, size)

                name_buffer = ctypes.create_unicode_buffer(size.contents.value)
                get_user_name_ex(name_display, name_buffer, size)
                user_name = name_buffer.value
            except:
                pass

        return user_name

    def check_version(self):
        # same method name like CVersion()::check_version()!
        '''
This method validates the current package version with maximum and minimum version.

In case the current version is not between min and max version, then the execution of 
testsuite is terminated with "unknown" state
        '''
        version_obj = CVersion()
        # We use the LOW LEVEL method 'version_obj.verify_version' here (instead of the HIGH LEVEL method 'version_obj.check_version()'),
        # to be able to provide error messages that are a bit more in scope of RobotFramework AIO tests (whereas
        # 'version_obj.check_version()' itself contains more generic error messages for Python developers, who use the version check
        # outside RobotFramework AIO tests.
        # Nevertheless, details about what happened we (mostly) get from 'version_obj.get_last_error()'. These error messages are
        # most precise. Partially the error messages are hard coded here.

        # from application configuration get reference information required for versioning and logging
        if self.__tsm_app_config:
            reference_version            = self.__tsm_app_config.get_reference_version()
            reference_app_name           = self.__tsm_app_config.get_reference_app_name()
            reference_installer_location = self.__tsm_app_config.get_reference_installer_location()
        else:
            logger.error(f"{self.__tsm_app_config_error}")
            raise Exception(f"Execution will be aborted because it's not possible to load the application configuration")

        # call of LOW LEVEL version control method
        result = version_obj.verify_version(self.min_version, self.max_version)

        version_check_has_issue = False
        exception               = None
        error                   = None
        last_error              = None
        addition1               = None # set in case of exception only
        addition2               = None # set in case of exception only

        # -- good cases
        if result==enVersionCheckResult.CHECK_NOT_EXECUTED.value:
            logger.info(f"Running without {reference_app_name} version check!")
            return
        elif result==enVersionCheckResult.CHECK_PASSED.value:
            logger.info(f"{reference_app_name} version check passed!")
            return
        # -- bad cases
        elif result in (enVersionCheckResult.WRONG_MINMAX_RELATION.value,
                        enVersionCheckResult.FORMAT_ERROR.value,
                        enVersionCheckResult.INTERNAL_ERROR.value):
            version_check_has_issue = True
            error      = "Something basic went wrong with the version check. This requires to fix the defined version numbers."
            last_error = version_obj.get_last_error()
            if result == enVersionCheckResult.FORMAT_ERROR.value:
                addition1 = "The expected version format is 'major.minor.patch' (e.g. 0.1.2)"
            addition2  = f"Affected configuration file: '{self.test_config_file}'"
            exception  = "Execution will be aborted because of a critical version check issue."
        elif result in (enVersionCheckResult.CONFLICT_MIN.value,
                        enVersionCheckResult.CONFLICT_MAX.value):
            version_check_has_issue = True
            error      = f"A failed version check requires to update the used software or to adapt the expected minimum version and the expected maximum version."
            last_error = version_obj.get_last_error()
            addition1  = f"Affected configuration file: '{self.test_config_file}'"
            addition2  = f"{reference_app_name} installer are available here: '{reference_installer_location}'"
            exception  = "Execution will be aborted because of a failed version check."
        else:
            # paranoia handling
            version_check_has_issue = True
            last_error = f"Code internal error: got not handled version check result: '{result}'."
            exception  = "Execution will be aborted because of an internal code error. Please contact the AIO team."

        test_suite = CString.NormalizePath(f"{BuiltIn().get_variable_value('${SUITE SOURCE}')}")
        logger.info(f"Testsuite : '{test_suite}'")

        if version_check_has_issue:
            if error:
                logger.error(f"{error}")
            logger.error(f"{last_error}")
            if addition1:
                logger.info(f"{addition1}")
            if addition2:
                logger.info(f"{addition2}")
            raise Exception(f"{exception}")

        return

if __name__ == "__main__":
    # small test:
    app_config = None
    print()
    try:
        app_config = AppConfig()
        print(f"==> is_robotframework_aio     : '{app_config.is_robotframework_aio()}'")
        print(f"==> tsm_version               : '{app_config.get_tsm_version()}'")
        print(f"==> tsm_version_date          : '{app_config.get_tsm_version_date()}'")
        print(f"==> tsm_app_name              : '{app_config.get_tsm_app_name()}'")
        print(f"==> tsm_installer_location    : '{app_config.get_tsm_installer_location()}'")
        print(f"==> bundle_version            : '{app_config.get_bundle_version()}'")
        print(f"==> bundle_version_date       : '{app_config.get_bundle_version_date()}'")
        print(f"==> bundle_name               : '{app_config.get_bundle_name()}'")
        print(f"==> bundle_installer_location : '{app_config.get_bundle_installer_location()}'")
    except Exception as ex:
        print(f"Exception in __main__: {ex}")
    print()















