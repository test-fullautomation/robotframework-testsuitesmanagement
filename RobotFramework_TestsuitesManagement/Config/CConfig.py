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
from RobotFramework_TestsuitesManagement.Utils.CStruct import CStruct
from RobotFramework_TestsuitesManagement.Utils.CVersion import CVersion, enVersionCheckResult, \
    bundle_version, INSTALLER_LOCATION, BUNDLE_NAME, BUNDLE_VERSION
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

The loading configuration method is divided into 4 levels, level1 has the highest priority, Level4 has the lowest priority.

**Level1:** Handed over by command line argument

**Level2:** Read from content of json config file

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
        self.sRootSuiteName    = ''
        self.oConfigParams     = {}
        self.sConfigName       = 'default'
        self.sVariablePattern  = r'^\p{L}[\p{L}\p{Nd}_]*$'
        self.sProjectName      = None
        self.iTotalTestcases   = 0
        self.iSuiteCount       = 0
        self.iTestCount        = 0
        self.sConfigFileName   = None
        self.bLoadedCfg        = True
        self.sLoadedCfgLog     = {"info" : [], "error" : [], "unknown": ''}
        self.sTestSuiteCfg     = ''
        self.sTestCfgFile      = ''
        self.sTestcasePath     = ''
        self.sMaxVersion       = ''
        self.sMinVersion       = ''
        self.sLocalConfig      = ''
        self.lBuitInVariables  = []
        self.configLevel       = TM.CConfigLevel.LEVEL_4
        self.rMetaData      = CStruct(
                                    sVersionSW = None,
                                    sVersionHW     = None,
                                    sVersionTest   = None,
                                    sROBFWVersion  = get_full_version('Robot Framework')
                                )

        # Common configuration parameters
        self.sWelcomeString  = None
        self.sTargetName     = None

    def __mergeDicts(self, dMainDict: dict, dUpdateDict: dict) -> dict:
        """
Merge dUpdateDict which contains updated data to dMainDict.

**Arguments:**

* ``dMainDict``

  / *Condition*: required / *Type*: dict /

* ``dUpdateDict``

  / *Condition*: required / *Type*: dict /

**Returns:**

* ``dMainDict``

  / *Type*: dict /

  Return dMainDict which contains update data in dUpdateDict.
        """
        for key, value in dUpdateDict.items():
            if isinstance(value, dict) and key in dMainDict:
                self.__mergeDicts(dMainDict[key], value)
            else:
                dMainDict[key] = value
        return dMainDict

    @staticmethod
    def loadCfg(self):
        '''
This loadCfg method uses to load configuration's parameters from json files.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        # Detect a configuration level and get the oConfig.sTestCfgFile to handle
        if self.configLevel == TM.CConfigLevel.LEVEL_1:
            # Configuration level 1, the oConfig.sTestCfgFile was already set in the LibListener.py module
            if self.sConfigName != 'default':
                self.bLoadedCfg = False
                self.sLoadedCfgLog['error'].append("Redundant settings detected in command line: Parameter 'variant' \
is used together with parameter 'config_file'.")
                self.sLoadedCfgLog['info'].append("---> It is not possible to use both together, because they belong \
to the same feature (the variant selection).")
                self.sLoadedCfgLog['info'].append("---> Please remove one of them.")
                self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                raise Exception

            if self.sTestCfgFile == '':
                self.bLoadedCfg = False
                self.sLoadedCfgLog['error'].append("The config_file input parameter is empty!!!")
                self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                raise Exception
        else:
            if self.configLevel==TM.CConfigLevel.LEVEL_2:
                # Configuration level 2, the oConfig.sTestCfgFile will be detected in method __loadConfigFileLevel2()
                self.bLoadedCfg = self.__loadConfigFileLevel2()
                if not self.bLoadedCfg:
                    # self.sLoadedCfgLog 'error' or 'info' are already set in method self.__loadConfigFileLevel2()
                    self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                    raise Exception
            else:
                # Configuration level 3
                if r'${variant}' in BuiltIn().get_variables():
                    self.bLoadedCfg = False
                    self.sLoadedCfgLog['error'].append(f"Not able to get a configuration for variant '{self.sConfigName}' \
because of a variant configuration file is not available.")
                    if self.sTestSuiteCfg != '':
                        self.sLoadedCfgLog['error'].append(f"In file: '{self.sTestSuiteCfg}'")
                    elif self.sTestCfgFile != '':
                        self.sLoadedCfgLog['error'].append(f"In file: '{self.sTestCfgFile}'")
                    self.sLoadedCfgLog['info'].append("---> A variant configuration file must be available when executing \
robot with configuration level 2.")
                    self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                    raise Exception
                # Detect the oConfig.sTestCfgFile the configuration level 3
                if os.path.isdir(self.sTestcasePath + 'config'):
                    self.configLevel = TM.CConfigLevel.LEVEL_3
                    sConfigFolder = CString.NormalizePath(f"{self.sTestcasePath}/config")
                    sSuiteFileName = BuiltIn().get_variable_value('${SUITE_SOURCE}').split(os.path.sep)[-1]
                    sJsonFile1 = f"{sConfigFolder}/{os.path.splitext(sSuiteFileName)[0]}.jsonp"
                    sJsonFile2 = f"{sConfigFolder}/{os.path.splitext(sSuiteFileName)[0]}.json"
                    if not os.path.isfile(sJsonFile1) and not os.path.isfile(sJsonFile2):
                        sJsonFile1    = f"{sConfigFolder}/robot_config.jsonp"
                        sJsonFile2    = f"{sConfigFolder}/robot_config.json" # still supported alternative extension

                    if os.path.isfile(sJsonFile1) and os.path.isfile(sJsonFile2):
                        self.bLoadedCfg = False
                        self.sLoadedCfgLog['error'].append("Configuration file duplicate detected (both extensions: 'jsonp' and 'json')!")
                        self.sLoadedCfgLog['info'].append(f"* file 1: '{sJsonFile1}'")
                        self.sLoadedCfgLog['info'].append(f"* file 2: '{sJsonFile2}'")
                        self.sLoadedCfgLog['info'].append(f"Please decide which one to keep and which one to remove. Both together are not allowed.") 
                        self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                        raise Exception
                    elif os.path.isfile(sJsonFile1):
                        self.sTestCfgFile = sJsonFile1
                    elif os.path.isfile(sJsonFile2):
                        self.sTestCfgFile = sJsonFile2
                    else: # meaning: if not os.path.isfile(sJsonFile1) and not os.path.isfile(sJsonFile2)
                        # Pre-condition of the configuration level 3 didn't match, set default configuration level 4.
                        self.configLevel = TM.CConfigLevel.LEVEL_4
                if self.configLevel==TM.CConfigLevel.LEVEL_4:
                    # Handling the configuration level 4
                    sDefaultConfig=str(pathlib.Path(__file__).parent.absolute() / "robot_config.jsonp")
                    self.sTestCfgFile = sDefaultConfig
            self.sTestCfgFile = CString.NormalizePath(self.sTestCfgFile)
        # Handling the oConfig.sTestCfgFile file to load the configuration object
        if not os.path.isfile(self.sTestCfgFile):
            self.bLoadedCfg = False
            self.sLoadedCfgLog['error'].append(f"Did not find configuration file: '{self.sTestCfgFile}'!")
            self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
            raise Exception
        robotCoreData = BuiltIn().get_variables()
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        try:
            oJsonCfgData = oJsonPreprocessor.jsonLoad(self.sTestCfgFile)
        except Exception as error:
            self.bLoadedCfg = False
            bCheck = False
            for line in str(error).splitlines():
                if "In file:" in line: # Check is self.sTestCfgFile path info already present in error?
                    bCheck = True
                self.sLoadedCfgLog['error'].append(f"{line}")
            if not bCheck:
                self.sLoadedCfgLog['error'].append(f"In file: {self.sTestCfgFile}")
            self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
            raise Exception
        # Handling local configuration
        if self.sLocalConfig != '':
            self.sLocalConfig = CString.NormalizePath(self.sLocalConfig)
            try:
                oLocalConfig = oJsonPreprocessor.jsonLoad(self.sLocalConfig)
            except Exception as error:
                self.bLoadedCfg = False
                self.sLoadedCfgLog['error'].append(str(error))
                self.sLoadedCfgLog['error'].append(f"Loading local config failed with file: {self.sLocalConfig}")
                self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                raise Exception
            isLocalConfig = True
            if "WelcomeString" in oLocalConfig:
                self.sLoadedCfgLog['error'].append(f"Loading local config failed with file: {self.sLocalConfig}")
                self.sLoadedCfgLog['info'].append("---> The mandatory 'WelcomeString' element of configuration file is found in local config file")
                self.sLoadedCfgLog['info'].append("---> Wrong local config file was chosen, please check!!!")
                isLocalConfig = False
            elif "default" in oLocalConfig:
                self.sLoadedCfgLog['error'].append(f"Loading local config failed with file: {self.sLocalConfig}")
                self.sLoadedCfgLog['info'].append("---> The variant 'default' element of the variant configuration in the configuration level 2 is found in local config file")
                self.sLoadedCfgLog['info'].append("---> Wrong local config file was chosen, please check!!!")
                isLocalConfig = False
            else:
                oJsonCfgData = self.__mergeDicts(oJsonCfgData, oLocalConfig)

            if not isLocalConfig:
                self.bLoadedCfg = False
                # Loading local configuration failed, the 'error' and 'info' are added above
                self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                raise Exception

        bJsonSchema = True
        try:
            sSchemaFile=str(pathlib.Path(__file__).parent.absolute() / "configuration_schema.json")
            with open(sSchemaFile) as f:
                oJsonSchemaCfg = json.load(f)
        except Exception as err:
            bJsonSchema = False
            self.bLoadedCfg = False
            self.sLoadedCfgLog['error'].append(f"Could not parse configuration JSON schema file: '{str(err)}'")
            self.sLoadedCfgLog['unknown'] = "Parse JSON schema file failed!"
            raise Exception

        if bJsonSchema:
            try:
                validate(instance=oJsonCfgData, schema=oJsonSchemaCfg)
            except Exception as error:
                self.bLoadedCfg = False
                if error.validator == 'additionalProperties':
                    self.sLoadedCfgLog['error'].append(f"Verification against JSON schema failed: '{error.message}'.")
                    self.sLoadedCfgLog['error'].append("Please put the additional params into 'params': { 'global': {...}")
                    self.sLoadedCfgLog['error'].append(f"In file: '{self.sTestCfgFile}'")
                elif error.validator == 'required':
                    param = regex.search("('[A-Za-z0-9]+')", error.message)
                    if param[0] == "'global'":
                        self.sLoadedCfgLog['error'].append(f"Required parameter {param[0]} is missing under 'params' in file '{self.sTestCfgFile}'.")
                    elif param is not None:
                        self.sLoadedCfgLog['error'].append(f"Required parameter {param[0]} is missing in file '{self.sTestCfgFile}'.")
                    else:
                        self.sLoadedCfgLog['error'].append(f"Required parameter {error.message} is missing in file '{self.sTestCfgFile}'.")
                    self.sLoadedCfgLog['error'].append("JSON schema validation failed!")
                else:
                    errParam = error.path.pop()
                    self.sLoadedCfgLog['error'].append(f"Parameter '{errParam}' with invalid value found in JSON configuration file!")
                    self.sLoadedCfgLog['error'].append(f"Reason: {error.message}")
                    self.sLoadedCfgLog['error'].append(f"In file: '{self.sTestCfgFile}'")
                self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                raise Exception

        self.sProjectName = oJsonCfgData['Project']
        self.sTargetName = oJsonCfgData['TargetName']
        self.sWelcomeString = oJsonCfgData['WelcomeString']
        if ("Maximum_version" in oJsonCfgData) and oJsonCfgData["Maximum_version"] != None:
            self.sMaxVersion = oJsonCfgData["Maximum_version"]
            # Check the format of Maximum_version value
            try:
                CVersion.tupleVersion(self.sMaxVersion)
            except Exception as error:
                self.sLoadedCfgLog['error'].append(f"Invalid Maximum version: {error}")
                self.sLoadedCfgLog['error'].append(f"In configuration: '{self.sTestCfgFile}'")
                self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                raise Exception
        if ("Minimum_version" in oJsonCfgData) and oJsonCfgData["Minimum_version"] != None:
            self.sMinVersion = oJsonCfgData["Minimum_version"]
            # Check the format of Minimum_version value
            try:
                CVersion.tupleVersion(self.sMinVersion)
            except Exception as error:
                self.sLoadedCfgLog['error'].append(f"Invalid Minimum version:{error}")
                self.sLoadedCfgLog['error'].append(f"In configuration: '{self.sTestCfgFile}'")
                self.sLoadedCfgLog['unknown'] = "Unable to load the test configuration. The test execution will be aborted!"
                raise Exception
        suiteMetadata = BuiltIn().get_variables()['&{SUITE_METADATA}']
        # Set metadata at top level
        BuiltIn().set_suite_metadata("project", self.sProjectName, top=True)
        BuiltIn().set_suite_metadata("machine", self.__getMachineName(), top=True)
        BuiltIn().set_suite_metadata("tester", self.__getUserName(), top=True)
        BuiltIn().set_suite_metadata("testtool", self.rMetaData.sROBFWVersion, top=True)
        BuiltIn().set_suite_metadata("bundle_version", BUNDLE_VERSION, top=True)
        if not ("version_sw" in suiteMetadata and self.rMetaData.sVersionSW == None):
            BuiltIn().set_suite_metadata("version_sw", self.rMetaData.sVersionSW, top=True)
        if not ("version_hw" in suiteMetadata and self.rMetaData.sVersionHW == None):
            BuiltIn().set_suite_metadata("version_hw", self.rMetaData.sVersionHW, top=True)
        if not ("version_test" in suiteMetadata and self.rMetaData.sVersionTest == None):
            BuiltIn().set_suite_metadata("version_test", self.rMetaData.sVersionTest, top=True)

        self.oConfigParams = copy.deepcopy(oJsonCfgData)

        self.__updateGlobalVariable()
        try:
            del oJsonCfgData['params']['global']
        except:
            pass

        jsonDotdict = DotDict(oJsonCfgData)
        BuiltIn().set_global_variable("${CONFIG}", jsonDotdict)
        if len(oJsonPreprocessor.dUpdatedParams) > 0:
            for param in oJsonPreprocessor.dUpdatedParams:
                logger.info(f"The parameter '{param}' is updated")

    def __setGlobalVariable(self, key, value):
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
        if not regex.match(self.sVariablePattern, key):
            self.sLoadedCfgLog['error'].append(f"Variable name '{key}' is invalid. Expected format: '{self.sVariablePattern}' (letters, digits, underscores)")
            self.sLoadedCfgLog['error'].append(f"Please check variable '{key}' in params['global'] in the configuration file '{self.sTestCfgFile}'")
            raise Exception
        k = key
        v = value
        if isinstance(v, dict):
            jsonDotdict = DotDict(v)
            BuiltIn().set_global_variable(f"${{{k.strip()}}}", jsonDotdict)
        elif isinstance(v, list):
            tmpList = []
            for item in v:
                if isinstance(item, dict):
                    jsonDotdict = DotDict(item)
                    tmpList.append(jsonDotdict)
                else:
                    tmpList.append(item)
            BuiltIn().set_global_variable(f"${{{k.strip()}}}", tmpList)
        else:
            BuiltIn().set_global_variable(f"${{{k.strip()}}}", v)

    def __updateGlobalVariable(self):
        '''
This method updates preprocessor and global params to global variable of RobotFramework AIO.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        lReservedKeyword = ['Settings', 'Variables', 'Keywords', 'Comments', 'Documentation', 'Metadata']
        if 'params' in self.oConfigParams and 'global' in self.oConfigParams['params']:
            for k,v in self.oConfigParams['params']['global'].items():
                if k in lReservedKeyword:
                    self.sLoadedCfgLog['error'].append(f"'{k}' is a reserved keyword in Robot Framework and cannot be used as parameter name.")
                    self.sLoadedCfgLog['unknown'] = "A parameter name conflicted with Robot Framework's reserved keywords. The test execution will be aborted!"
                    raise Exception
                if k in self.lBuitInVariables:
                    continue
                try:
                    self.__setGlobalVariable(k, v)
                except Exception as error:
                    self.sLoadedCfgLog['error'].append(error)
                    raise Exception

    def __del__(self):
        '''
This destructor method.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        pass

    def __loadConfigFileLevel2(self) -> bool:
        '''
This __loadConfigFileLevel2 method loads configuration in case configLevel is TM.CConfigLevel.LEVEL_2.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        if self.sTestSuiteCfg.startswith('.../'):
            sTestSuiteCfgStart = self.sTestSuiteCfg
            self.sTestSuiteCfg = self.sTestSuiteCfg[4:]
            if os.path.exists(CString.NormalizePath('./' + self.sTestSuiteCfg)):
                self.sTestSuiteCfg = './' + self.sTestSuiteCfg
            else:
                bFoundTestSuiteCfg = False
                for i in range(0, 30):
                    self.sTestSuiteCfg = '../' + self.sTestSuiteCfg
                    if os.path.exists(CString.NormalizePath(self.sTestSuiteCfg)):
                        bFoundTestSuiteCfg = True
                        break
                if not bFoundTestSuiteCfg:
                    self.sLoadedCfgLog['error'].append("Testsuite management - Loading configuration level 2 failed!")
                    self.sLoadedCfgLog['error'].append(f"Could not find the variant configuration file: '{sTestSuiteCfgStart}'")
                    return False
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        self.sTestSuiteCfg = CString.NormalizePath(self.sTestSuiteCfg)
        try:
            oSuiteConfig = oJsonPreprocessor.jsonLoad(self.sTestSuiteCfg)
        except Exception as error:
            self.bLoadedCfg = False
            bCheck = False
            for line in str(error).splitlines():
                if "In file:" in line: # Checking is self.sTestSuiteCfg path info already present in error?
                    bCheck = True
                self.sLoadedCfgLog['error'].append(f"{line}")
            if not bCheck:
                self.sLoadedCfgLog['error'].append(f"In file: {self.sTestSuiteCfg}")
            return False
        sListOfVariants = ''
        for item in list(oSuiteConfig.keys()):
            sListOfVariants = sListOfVariants + f"'{item}', "
        if not regex.match(r'^[a-zA-Z0-9.\u0080-\U0010FFFF\_\-\:@\$]+$', self.sConfigName):
            self.sLoadedCfgLog['error'].append("Testsuite management - Loading configuration level 2 failed!")
            self.sLoadedCfgLog['error'].append(f"The variant name '{self.sConfigName}' is invalid.")
            self.sLoadedCfgLog['error'].append(f"Please find the suitable variant in this list: {sListOfVariants}")
            self.sLoadedCfgLog['error'].append(f"In file: '{self.sTestSuiteCfg}'")
            return False

        if self.sConfigName not in oSuiteConfig:
            self.sLoadedCfgLog['error'].append("Testsuite management - Loading configuration level 2 failed!")
            self.sLoadedCfgLog['error'].append(f"The variant '{self.sConfigName}' is not defined in '{os.path.abspath(self.sTestSuiteCfg)}'.")
            self.sLoadedCfgLog['error'].append(f"Please find the suitable variant in this list: {sListOfVariants}")
            return False

        try:
            self.sTestCfgFile = oSuiteConfig[self.sConfigName]['name']
            sTestCfgDir = oSuiteConfig[self.sConfigName]['path']
            if regex.match(r'^\.+/*.*', sTestCfgDir):
                sTestCfgDir = os.path.dirname(self.sTestSuiteCfg) + '/' + sTestCfgDir + '/'
        except:
            self.sLoadedCfgLog['error'].append("Testsuite management - Loading configuration level 2 failed!")
            self.sLoadedCfgLog['error'].append(f"The 'name' or 'path' property is not defined for the variant '{self.sConfigName}'.")
            self.sLoadedCfgLog['error'].append(f"In file: '{os.path.abspath(self.sTestSuiteCfg)}'")
            return False
        if self.sTestCfgFile.strip() == '':
            self.sLoadedCfgLog['error'].append("Testsuite management - Loading configuration level 2 failed!")
            self.sLoadedCfgLog['error'].append(f"The configuration file name of variant '{self.sConfigName}' must not be empty.")
            self.sLoadedCfgLog['error'].append(f"In file: '{os.path.abspath(self.sTestSuiteCfg)}'")
            return False
        
        self.sTestCfgFile = sTestCfgDir + self.sTestCfgFile
        return True

    @staticmethod
    def __getMachineName():
        '''
This __getMachineName method gets current machine name which is running the test.

**Arguments:**

* No input parameter is required

**Returns:**

* ``sMachineName``

   / *Type*: string /
        '''
        sMachineName = ''
        # Allows windows system access only in windows systems
        if platform.system().lower()!="windows":
            try:
                sMachineName = socket.gethostname()
            except:
                pass
        else:
            try:
                sMachineName = os.getenv("COMPUTERNAME",'')
            except:
                pass

        return sMachineName

    @staticmethod
    def __getUserName():
        '''
This __getUserName method gets current account name login to run the test.

**Arguments:**

* No input parameter is required

**Returns:**

* ``sUserName``

   / *Type*: string /
        '''
        sUserName = ''
        # Allows windows system access only in windows systems
        if platform.system().lower()!="windows":
            try:
                sUserName = os.getenv("USER","")
            except:
                pass
        else:
            try:
                GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
                NameDisplay = 3

                size = ctypes.pointer(ctypes.c_ulong(0))
                GetUserNameEx(NameDisplay, None, size)

                nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
                GetUserNameEx(NameDisplay, nameBuffer, size)
                sUserName = nameBuffer.value
            except:
                pass

        return sUserName

    def versionCheck(self):
        '''
This method validates the current package version with maximum and minimum version.

In case the current version is not between min and max version, then the execution of 
testsuite is terminated with "unknown" state
        '''
        oVersion = CVersion()
        res, reason = oVersion.verifyVersion(self.sMinVersion, self.sMaxVersion)
        if res is None:
            logger.info(f"Running without {BUNDLE_NAME} version check!")
            return
        elif res is True:
            logger.info(f"{BUNDLE_NAME} version check passed!")
            return
        else:
            if reason == enVersionCheckResult.WRONGMINMAX.value:
                header = "Wrong use of max/min version control in configuration."
                detail = f"\nThe configured minimum {BUNDLE_NAME} version                 '{self.sMinVersion}'"
                detail +=f"\nis younger than the configured maximum {BUNDLE_NAME} version '{self.sMaxVersion}'"
                detail +="\nPlease correct the values of 'Maximum_version', 'Minimum_version' in config file"
            elif reason == enVersionCheckResult.CONFLICTMIN.value:
                header = "Version conflict."
                detail = f"\nThe test execution requires minimum {BUNDLE_NAME} version '{self.sMinVersion}'"
                detail +=f"\nbut the installed {BUNDLE_NAME} version is older          '{BUNDLE_VERSION}'"
            elif reason == enVersionCheckResult.CONFLICTMAX.value:
                header = "Version conflict."
                detail = f"\nThe test execution requires maximum {BUNDLE_NAME} version '{self.sMaxVersion}'"
                detail +=f"\nbut the installed {BUNDLE_NAME} version is younger        '{BUNDLE_VERSION}'"
            elif reason == enVersionCheckResult.UNKNOWN.value:
                header = "Internal error"
                detail = "Error when reading the RobotFramework AIO bundle version."

            BuiltIn().log(f"{header}" +
            f"\nTestsuite : {BuiltIn().get_variable_value('${SUITE SOURCE}')}" +
            f"\nconfig    : {self.sTestCfgFile}" +
            f"\n{detail}\n"
            f"\nPlease install the required {BUNDLE_NAME} version." +
            f"\nYou can find an installer here: {INSTALLER_LOCATION}\n", "ERROR")
            raise Exception('Version control error!!!')

if __name__ == "__main__":
    bundle_version()
