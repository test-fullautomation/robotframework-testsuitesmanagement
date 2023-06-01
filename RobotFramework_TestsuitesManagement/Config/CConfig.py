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


import re
import os
import platform
import ctypes
import socket
import json
import copy
from jsonschema import validate
from builtins import staticmethod

from RobotFramework_TestsuitesManagement.Utils.CStruct import CStruct
from PythonExtensionsCollection.String.CString import CString

from JsonPreprocessor import CJsonPreprocessor
from robot.api import logger
from robot.version import get_full_version, get_version
from robot.libraries.BuiltIn import BuiltIn
from robot.utils.dotdict import DotDict
import pathlib
from RobotFramework_TestsuitesManagement.version import VERSION, VERSION_DATE

INSTALLER_LOCATION = "https://github.com/test-fullautomation/robotframework-testsuitesmanagement/releases"
BUNDLE_NAME = "RobotFramework_TestsuitesManagement"
BUNDLE_VERSION = VERSION
BUNDLE_VERSION_DATE = VERSION_DATE

# Load package context file
context_filename = "package_context.json"
context_filepath = os.path.join(os.path.dirname(__file__), context_filename)
context_config = None

if os.path.isfile(context_filepath):
    if os.stat(context_filepath).st_size == 0:
        logger.warn(f"The '{context_filepath}' file is existing but empty.")
    else:
        try:
            with open(context_filepath) as f:
                context_config = json.load(f)        
        except Exception as reason:
            logger.error(f"Cannot load the '{context_filepath}' file. Reason: {reason}")
            exit(1)

        if ('installer_location' in context_config) and context_config['installer_location']:
            INSTALLER_LOCATION = context_config['installer_location']
        if ('bundle_name' in context_config) and context_config['bundle_name']:
            BUNDLE_NAME = context_config['bundle_name']
        if ('bundle_version' in context_config) and context_config['bundle_version']:
            BUNDLE_VERSION = context_config['bundle_version']
        if ('bundle_version_date' in context_config) and context_config['bundle_version_date']:
            BUNDLE_VERSION_DATE = context_config['bundle_version_date']

def bundle_version():
   '''
This function prints out the package version which is:

- RobotFramework_TestsuitesManagement version when this module is installed
stand-alone (via `pip` or directly from sourcecode)

- RobotFramework AIO version when this module is bundled with RobotFramework AIO 
package

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
   '''
   print(f"{BUNDLE_VERSION}")

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
            "path": ".../config/"
         },
         "variant_0": {
            "name": "robot_config.jsonp",
            "path": ".../config/"
         },
         "variant_1": {
            "name": "robot_config_variant_1.jsonp",
            "path": ".../config/"
         },
            ...
            ...
      }

   According to the ``ConfigName``, RobotFramework_TestsuitesManagement will choose the corresponding config file.
   ``".../config/"`` indicats the relative path to json config file, RobotFramework_TestsuitesManagement will recursively
   find the ``config`` folder.

**Level3:** Read in testsuite folder: ``/config/robot_config.jsonp``

**Level4:** Read from RobotFramework AIO installation folder:

    ``/RobotFramework/defaultconfig/robot_config.jsonp``
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    __single          = None
    sRootSuiteName    = ''
    bConfigLoaded     = False
    oConfigParams     = {}
    sConfigName       = 'default'
    sProjectName      = None
    iTotalTestcases   = 0
    iSuiteCount       = 0
    iTestCount        = 0
    sConfigFileName   = None
    bLoadedCfg        = True
    sLoadedCfgError   = ''
    sTestSuiteCfg     = ''
    sTestCfgFile      = ''
    sTestcasePath     = ''
    sMaxVersion       = ''
    sMinVersion       = ''
    sLocalConfig      = ''
    lBuitInVariables  = []
    rConfigFiles   = CStruct(
                                bLevel1 = False,
                                bLevel2 = False,
                                bLevel3 = False,
                                bLevel4 = True   #'.../RobotFramework_TestsuitesManagement/Config/robot_config.jsonp'
                            )
    
    rMetaData      = CStruct(
                                sVersionSW = '',
                                sVersionHW     = '',
                                sVersionTest   = '',
                                sROBFWVersion  = get_full_version('Robot Framework')
                            )
    
    # Common configuration parameters 
    sWelcomeString  = None
    sTargetName     = None
    ddictJson = DotDict()
    
    class CJsonDotDict():
        '''
The CJsonDotDict class converts json configuration object to dotdict
        '''
        def __init__(self):
            self.lTmpParam = ['CConfig.ddictJson']
            
        def __del__(self):
            CConfig.ddictJson = DotDict()
            del self.lTmpParam

        def dotdictConvert(self, oJson):
            '''
This dotdictConvert method converts json object to dotdict.

**Arguments:**

* ``oJson``

   / *Condition*: required / *Type*: dict /

   Json object which want to convert to dotdict.

**Returns:**

* ``CConfig.ddictJson``

   / *Type*: dotdict /
            '''
            if len(self.lTmpParam) == 1:
                CConfig.ddictJson.update(oJson)
                
            for k,v in oJson.items():
                sExec = ""
                if isinstance(v, dict):
                    self.lTmpParam.append(k)
                    for i in self.lTmpParam:
                        sExec = i if i==self.lTmpParam[0] else sExec + "." + i
                    sExec = sExec + " = DotDict(" + str(v) + ")"
                    try:
                        exec(sExec, globals())
                    except:
                        logger.info(f"Could not convert: {sExec} to dotdict")
                        pass
                    
                    self.dotdictConvert(v)
                elif isinstance(v, list):
                    n = 0
                    for item in v:
                        if isinstance(item, dict):
                            self.lTmpParam.append(k+"["+str(n)+"]")
                            for i in self.lTmpParam:
                                sExec = i if i == self.lTmpParam[0] else sExec + "." + i
                            sExec = sExec + " = DotDict(" + str(item) + ")"
                            try:
                                exec(sExec, globals())
                            except:
                                logger.info(f"Could not convert: {sExec} to dotdict")
                                pass
                            
                            self.dotdictConvert(item)
                        n = n+1
            self.lTmpParam = self.lTmpParam[:-1]
            return CConfig.ddictJson
     
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
        pass
        

    @staticmethod
    def loadCfg(self):
        '''
This loadCfg method uses to load configuration's parameters from json files.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        bConfigLevel2 = True
        if not self.rConfigFiles.bLevel1:
            if self.rConfigFiles.bLevel2:
                self.rConfigFiles.bLevel4 = False
                bConfigLevel2 = self.__loadConfigFileLevel2()
            else:
                if r'${variant}' in BuiltIn().get_variables():
                    logger.error(f"Not able to get a configuration for variant '{self.sConfigName}' because of a variant configuration file is not available. \n" + \
                                  "          A variant configuration file must be available when executing robot with configuration level 2. \n")
                    BuiltIn().unknown('Loading configuration level 2 failed!')
                    
                if os.path.isdir(self.sTestcasePath + 'config'):
                    sConfigFolder = CString.NormalizePath(f"{self.sTestcasePath}/config")
                    sSuiteFileName = BuiltIn().get_variable_value('${SUITE_SOURCE}').split(os.path.sep)[-1:][0]
                    sJsonFile1 = f"{sConfigFolder}/{sSuiteFileName.split('.')[0]}.jsonp"
                    sJsonFile2 = f"{sConfigFolder}/{sSuiteFileName.split('.')[0]}.json"
                    if not os.path.isfile(sJsonFile1) and not os.path.isfile(sJsonFile2):
                        sJsonFile1    = f"{sConfigFolder}/robot_config.jsonp"
                        sJsonFile2    = f"{sConfigFolder}/robot_config.json" # still supported alternative extension

                    if os.path.isfile(sJsonFile1) and os.path.isfile(sJsonFile2):
                        errorMessage = "Configuration file duplicate detected (both extensions: 'jsonp' and 'json')!\n" + \
                                        f"* file 1: '{sJsonFile1}'\n" + \
                                        f"* file 2: '{sJsonFile2}'\n" + \
                                        "Please decide which one to keep and which one to remove. Both together are not allowed."
                        logger.error(errorMessage)
                        BuiltIn().unknown("Configuration file duplicate detected (both extensions: 'jsonp' and 'json')!")
                    elif os.path.isfile(sJsonFile1):
                        self.sTestCfgFile = sJsonFile1
                        self.rConfigFiles.bLevel4 = False
                    elif os.path.isfile(sJsonFile2):
                        self.sTestCfgFile = sJsonFile2
                        self.rConfigFiles.bLevel4 = False
                    else: # meaning: if not os.path.isfile(sJsonFile1) and not os.path.isfile(sJsonFile2)
                        self.rConfigFiles.bLevel3 = False
                        if not self.bConfigLoaded:
                            sDefaultConfig=str(pathlib.Path(__file__).parent.absolute() / "robot_config.jsonp")
                            self.sTestCfgFile = sDefaultConfig
                else:
                    self.rConfigFiles.bLevel3 = False
                    if not self.bConfigLoaded:
                        sDefaultConfig=str(pathlib.Path(__file__).parent.absolute() / "robot_config.jsonp")
                        self.sTestCfgFile = sDefaultConfig

            if self.sTestCfgFile != '':                      
                self.sTestCfgFile = CString.NormalizePath(self.sTestCfgFile)

        if self.bConfigLoaded:
            if self.rConfigFiles.bLevel1:
                return
            elif not self.rConfigFiles.bLevel2 and not self.rConfigFiles.bLevel3:
                return
        
        if self.rConfigFiles.bLevel1:
            if self.sConfigName != 'default':
                errorMessage = "Redundant settings detected in command line: Parameter 'variant' is used together with parameter 'config_file'.\n" + \
                               "          It is not possible to use both together, because they belong to the same feature (the variant selection).\n" + \
                               "          Please remove one of them.\n"
                logger.error(errorMessage)
                BuiltIn().unknown('Redundant settings detected in command line!')

            if self.sTestCfgFile == '':
                errorMessage = "The config_file input parameter is empty!!!\n"
                logger.error(errorMessage)
                BuiltIn().unknown(errorMessage)

        if not bConfigLevel2:
            BuiltIn().unknown('Loading configuration level 2 failed!')
            return

        if not os.path.isfile(self.sTestCfgFile):
            errorMessage = f"Did not find configuration file: '{self.sTestCfgFile}'!\n"
            logger.error(errorMessage)
            BuiltIn().unknown('The configuration file is not found!')
        
        robotCoreData = BuiltIn().get_variables()
        ROBFW_AIO_Data = {}
        for k, v in robotCoreData.items():
            key = re.findall("\s*{\s*(.+)\s*}\s*", k)[0]
            if 'CONFIG' == key:
                continue
            ROBFW_AIO_Data.update({key:v})
        oJsonPreprocessor = CJsonPreprocessor(syntax="python", currentCfg=ROBFW_AIO_Data)
        try:
            oJsonCfgData = oJsonPreprocessor.jsonLoad(self.sTestCfgFile)
        except Exception as error:
            CConfig.bLoadedCfg = False
            CConfig.sLoadedCfgError = ''
            for item in str(error).split(': \''):
                CConfig.sLoadedCfgError += f"{item}\n                  "
            logger.error(f"Loading of JSON configuration file failed! \n          Reason: {CConfig.sLoadedCfgError}")
            BuiltIn().unknown('Loading of JSON configuration file failed!')
            raise Exception

        if self.sLocalConfig != '':
            try:
                oLocalConfig = oJsonPreprocessor.jsonLoad(CString.NormalizePath(self.sLocalConfig))
            except Exception as error:
                CConfig.bLoadedCfg = False
                CConfig.sLoadedCfgError = str(error)
                logger.error(f"Loading local config failed! Reason: {CConfig.sLoadedCfgError}\n")
                BuiltIn().unknown('Loading local config failed!')
                raise Exception
            
            def __loadLocalConfig(oLocalConfig):
                tmpDict = copy.deepcopy(oLocalConfig)
                for k, v in tmpDict.items():
                    if re.match('.*\${\s*', k):
                        del oLocalConfig[k]
                    elif isinstance(v, dict):
                        __loadLocalConfig(oLocalConfig)
                oJsonCfgData.update(oLocalConfig)
            __loadLocalConfig(oLocalConfig)

        bJsonSchema = True    
        try:
            sSchemaFile=str(pathlib.Path(__file__).parent.absolute() / "configuration_schema.json")
            with open(sSchemaFile) as f:
                oJsonSchemaCfg = json.load(f)
        except Exception as err:
            bJsonSchema = False
            logger.error(f"Could not parse configuration JSON schema file: '{str(err)}'\n")
            BuiltIn().unknown('Parse JSON schema file failed!')
    
        if bJsonSchema:
            try:
                validate(instance=oJsonCfgData, schema=oJsonSchemaCfg)
            except Exception as error:
                if error.validator == 'additionalProperties':
                    logger.error(f"Verification against JSON schema failed: '{error.message}'\n" + \
                                 "          Please put the additional params into 'params': { 'global': {...} \n")
                elif error.validator == 'required':
                    logger.error(f"The parameter {error.message} in configuration file {self.sTestCfgFile}.\n")
                else:
                    errParam = error.path.pop()
                    logger.error(f"Parameter '{errParam}' with invalid value found in JSON configuration file! \n" + \
                                 f"          {error.message}\n")
                BuiltIn().unknown('JSON schema validation failed!')
            
        self.sProjectName = oJsonCfgData['Project']
        self.sTargetName = oJsonCfgData['TargetName']
        self.sWelcomeString = oJsonCfgData['WelcomeString']
        if ("Maximum_version" in oJsonCfgData) and oJsonCfgData["Maximum_version"] != None:
            self.sMaxVersion = oJsonCfgData["Maximum_version"]
        if ("Minimum_version" in oJsonCfgData) and oJsonCfgData["Minimum_version"] != None:
            self.sMinVersion = oJsonCfgData["Minimum_version"]

        suiteMetadata = BuiltIn().get_variables()['&{SUITE_METADATA}']
        # Set metadata at top level
        BuiltIn().set_suite_metadata("project", self.sProjectName, top=True)
        BuiltIn().set_suite_metadata("machine", self.__getMachineName(), top=True)
        BuiltIn().set_suite_metadata("tester", self.__getUserName(), top=True)
        BuiltIn().set_suite_metadata("testtool", self.rMetaData.sROBFWVersion, top=True)
        BuiltIn().set_suite_metadata("bundle_version", BUNDLE_VERSION, top=True)
        if "version_sw" in suiteMetadata and self.rMetaData.sVersionSW == '':
            pass
        else:
            BuiltIn().set_suite_metadata("version_sw", self.rMetaData.sVersionSW, top=True)
        if "version_hw" in suiteMetadata and self.rMetaData.sVersionHW == '':
            pass
        else:
            BuiltIn().set_suite_metadata("version_hw", self.rMetaData.sVersionHW, top=True)
        if "version_test" in suiteMetadata and self.rMetaData.sVersionTest == '':
            pass
        else:
            BuiltIn().set_suite_metadata("version_test", self.rMetaData.sVersionTest, top=True)
        
        CConfig.oConfigParams = copy.deepcopy(oJsonCfgData)
        
        self.__updateGlobalVariable()
        try:    
            del oJsonCfgData['params']['global']
        except:
            pass  
        
        # try:
        #     del oJsonCfgData['preprocessor']['definitions']
        # except:
        #     pass 
        
        bDotdict = False
        dotdictObj = CConfig.CJsonDotDict()
        try:
            jsonDotdict = dotdictObj.dotdictConvert(oJsonCfgData)
            bDotdict = True
        except:
            logger.info("Could not convert JSON config to dotdict!!!")
            pass
        del dotdictObj
        
        if bDotdict:
            BuiltIn().set_global_variable("${CONFIG}", jsonDotdict)
        else:
            BuiltIn().set_global_variable("${CONFIG}",oJsonCfgData)
        self.bConfigLoaded = True

        if len(oJsonPreprocessor.lUpdatedParams) > 0:
            for param in oJsonPreprocessor.lUpdatedParams:
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
        k = key
        v = value
        if isinstance(v, dict):
            bDotdict = False
            dotdictObj = CConfig.CJsonDotDict()
            try:
                jsonDotdict = dotdictObj.dotdictConvert(v)
                bDotdict = True
            except:
                logger.info("Could not convert JSON config to dotdict!!!")
                pass
            del dotdictObj
            if bDotdict:
                BuiltIn().set_global_variable(f"${{{k.strip()}}}", jsonDotdict)
            else:
                BuiltIn().set_global_variable(f"${{{k.strip()}}}", v)
        elif isinstance(v, list):
            tmpList = []
            for item in v:
                if isinstance(item, dict):
                    bDotdict = False
                    dotdictObj = CConfig.CJsonDotDict()
                    try:
                        jsonDotdict = dotdictObj.dotdictConvert(item)
                        bDotdict = True
                    except:
                        logger.info("Could not convert JSON config to dotdict!!!")
                        pass
                    if bDotdict:
                        tmpList.append(jsonDotdict)
                    else:
                        tmpList.append(item)
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
        # try:
        #     for k,v in self.oConfigParams['preprocessor']['definitions'].items():
        #         if k in self.lBuitInVariables:
        #             continue
        #         try:
        #             self.__setGlobalVariable(k, v)
        #         except:
        #             continue
        # except:
        #     pass
        
        try:
            for k,v in self.oConfigParams['params']['global'].items():
                if k in self.lBuitInVariables:
                    continue
                try:
                    self.__setGlobalVariable(k, v)
                except:
                    continue
        except:
            pass  
        
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
This __loadConfigFileLevel2 method loads configuration in case rConfigFiles.bLevel2 == True.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        try:
            oSuiteConfig = oJsonPreprocessor.jsonLoad(CString.NormalizePath(self.sTestSuiteCfg))
        except Exception as error:
            CConfig.bLoadedCfg = False
            CConfig.sLoadedCfgError = ''
            for item in str(error).split(': \''):
                CConfig.sLoadedCfgError += f"{item}\n                  "
            logger.error(f"Loading of JSON configuration file failed! \n          Reason: {CConfig.sLoadedCfgError}\n")
            return False
        sListOfVariants = '\n'
        for item in list(oSuiteConfig.keys()):
            sListOfVariants = sListOfVariants + f"            - '{item}' \n"
        if not re.match(r'^[a-zA-Z0-9.\u0080-\U0010FFFF\_\-\:@\$]+$', self.sConfigName):
            CConfig.sLoadedCfgError = "Testsuite management - Loading configuration level 2 failed! \n" + \
                                      f"          The variant name '{self.sConfigName}' is invalid. \n" + \
                                      f"          Please find the suitable variant in this list: {sListOfVariants}\n"
            logger.error(CConfig.sLoadedCfgError)
            return False

        if self.sConfigName not in oSuiteConfig:
            CConfig.sLoadedCfgError = "Testsuite management - Loading configuration level 2 failed! \n" + \
                                     f"          The variant '{self.sConfigName}' is not defined in '{os.path.abspath(self.sTestSuiteCfg)}' \n" + \
                                     f"          Please find the suitable variant in this list: {sListOfVariants}\n"
            logger.error(CConfig.sLoadedCfgError)
            return False

        try:
            self.sTestCfgFile = oSuiteConfig[self.sConfigName]['name']
            sTestCfgDir = oSuiteConfig[self.sConfigName]['path']
        except:
            CConfig.sLoadedCfgError = "Testsuite management - Loading configuration level 2 failed! \n" + \
                                     "          The 'name' or 'path' property is not defined for the variant" + \
                                    f"'{self.sConfigName}' in '{os.path.abspath(self.sTestSuiteCfg)}'\n"
            logger.error(CConfig.sLoadedCfgError)
            return False
        if self.sTestCfgFile.strip() == '':
            CConfig.sLoadedCfgError = "Testsuite management - Loading configuration level 2 failed! \n" + \
                                      f"          The configuration file name of variant '{self.sConfigName}' " + \
                                      f"must not be empty in '{os.path.abspath(self.sTestSuiteCfg)}'\n"
            logger.error(CConfig.sLoadedCfgError)
            return False
            
        if sTestCfgDir.startswith('.../'):
            sTestCfgDirStart = sTestCfgDir
            sTestCfgDir = sTestCfgDir[4:]
            if os.path.exists(CString.NormalizePath('./' + sTestCfgDir)):
                sTestCfgDir = './' + sTestCfgDir
            else:
                bFoundTestCfgDir = False
                sCheckCfgDir = ''
                for i in range(0, 30):
                    sTestCfgDir = '../' + sTestCfgDir
                    if sCheckCfgDir == CString.NormalizePath(sTestCfgDir):
                        break
                    else:
                        sCheckCfgDir = CString.NormalizePath(sTestCfgDir)
                    if os.path.exists(sCheckCfgDir):
                        bFoundTestCfgDir = True
                        break
                if bFoundTestCfgDir == False:
                    CConfig.sLoadedCfgError = "Testsuite management - Loading configuration level 2 failed! \n" + \
                                             f"          Could not find out config directory: '{sTestCfgDirStart}'"
                    logger.error(CConfig.sLoadedCfgError)
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
            except Exception(reason):
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
    
    def verifyVersion(self):
        '''
This verifyVersion validates the current package version with maximum and 
minimum version (if provided in the configuration file).

The package version is:

- RobotFramework_TestsuitesManagement version when this module is installed
stand-alone (via `pip` or directly from sourcecode)

- RobotFramework AIO version when this module is bundled with RobotFramework AIO 
package

In case the current version is not between min and max version, then the 
execution of testsuite is terminated with "unknown" state

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        sCurrentVersion = BUNDLE_VERSION
        tCurrentVersion = CConfig.tupleVersion(sCurrentVersion)
        
        # Verify format of provided min and max versions then parse to tuples
        tMinVersion = None
        tMaxVersion = None
        if self.sMinVersion.strip() == '' and self.sMaxVersion.strip() == '':
            logger.info(f"Running without {BUNDLE_NAME} version check!")
            return
        if self.sMinVersion != '':
            tMinVersion = CConfig.tupleVersion(self.sMinVersion)
        if self.sMaxVersion != '':
            tMaxVersion = CConfig.tupleVersion(self.sMaxVersion)
        bVersionCheck = True
        if tMinVersion and tMaxVersion and (tMinVersion > tMaxVersion):
            self.versioncontrol_error('wrong_minmax', self.sMinVersion, self.sMaxVersion)
            bVersionCheck = False
        if tMinVersion and not CConfig.bValidateMinVersion(tCurrentVersion, tMinVersion):
            self.versioncontrol_error('conflict_min', self.sMinVersion, sCurrentVersion)
            bVersionCheck = False
        if tMaxVersion and not CConfig.bValidateMaxVersion(tCurrentVersion, tMaxVersion):
            self.versioncontrol_error('conflict_max', self.sMaxVersion, sCurrentVersion)
            bVersionCheck = False

        if bVersionCheck:
            logger.info(f"{BUNDLE_NAME} version check passed!")

    @staticmethod
    def bValidateMinVersion(tCurrentVersion, tMinVersion):
        '''
This bValidateMinVersion validates the current version with required minimun version.

**Arguments:**

* ``tCurrentVersion``

  / *Condition*: required / *Type*: tuple /

  Current package version.

* ``tMinVersion``

  / *Condition*: required / *Type*: tuple /

  The minimum version of package.

**Returns:**

* ``True`` or ``False``
        '''
        return tCurrentVersion >= tMinVersion

    @staticmethod
    def bValidateMaxVersion(tCurrentVersion, tMaxVersion):
        '''
This bValidateMaxVersion validates the current version with required minimun version.

**Arguments:**

* ``tCurrentVersion``

  / *Condition*: required / *Type*: tuple /

  Current package version.

* ``tMinVersion``

  / *Condition*: required / *Type*: tuple /

  The minimum version of package.

**Returns:**

* ``True or False``
        '''
        return tCurrentVersion <= tMaxVersion

    @staticmethod
    def bValidateSubVersion(sVersion):
        '''
This bValidateSubVersion validates the format of provided sub version and parse 
it into sub tuple for version comparision.

**Arguments:**

* ``sVersion``

  / *Condition*: required / *Type*: string /

  The version of package.

**Returns:**

* ``lSubVersion``

  / *Type*: tuple /
        '''
        lSubVersion = [0,0,0]
        oMatch = re.match(r"^(\d+)(?:-?(a|b|rc)(\d*))?$", sVersion)
        if oMatch:
            lSubVersion[0] = int(oMatch.group(1))
            # a < b < rc < released (without any character)
            if oMatch.group(2):
                if oMatch.group(2) == 'a':
                    lSubVersion[1] = 0
                elif oMatch.group(2) == 'b':
                    lSubVersion[1] = 1
                elif oMatch.group(2) == 'rc':
                    lSubVersion[1] = 2
            else:
                lSubVersion[1] = 3
            
            if oMatch.group(3):
                lSubVersion[2] = int(oMatch.group(3))
            else:
                lSubVersion[2] = 0
            
            return tuple(lSubVersion)
        else:
            raise Exception("Wrong format in version info")
            
    @staticmethod
    def tupleVersion(sVersion):
        '''
This tupleVersion returns a tuple which contains the (major, minor, patch) version.

In case minor/patch version is missing, it is set to 0.
E.g: "1" is transformed to "1.0.0" and "1.1" is transformed to "1.1.0"
            
This tupleVersion also support version which contains Alpha (a), Beta (b) or 
Release candidate (rc): E.g: "1.2rc3", "1.2.1b1", ...

**Arguments:**

* ``sVersion``

  / *Condition*: required / *Type*: string /

  The version of package.

**Returns:**

* ``lVersion``

  / *Type*: tuple /

  A tuple which contains the (major, minor, patch) version.


        '''
        lVersion = sVersion.split(".")
        if len(lVersion) == 1:
            lVersion.extend(["0", "0"])
        elif len(lVersion) == 2:
            lVersion.append("0")
        elif len(lVersion) >= 3:
            # Just ignore and remove the remaining 
            lVersion = lVersion[:3]
        try:
            # verify the version info is a number
            return tuple(map(lambda x: CConfig.bValidateSubVersion(x), lVersion))
        except Exception:
            BuiltIn().fatal_error(f"Provided version '{sVersion}' is not a correct version format.")

    def versioncontrol_error(self, reason, version1, version2):
        '''
Wrapper version control error log:

Log error message of version control due to reason and set to unknown state.

**Arguments:**

* ``reason``

  / *Condition*: required / *Type*: string /

  ``reason`` can only be ``conflict_min``, ``conflict_max`` and ``wrong_minmax``.

* ``version1``

  / *Condition*: required / *Type*: string /

* ``version2``

  / *Condition*: required / *Type*: string /

**Returns:**

* No return variable
        '''

        header = ""
        detail = ""
        if reason=="conflict_min":
            header = "Version conflict."
            detail = f"\nThe test execution requires minimum {BUNDLE_NAME} version '{version1}'"
            detail +=f"\nbut the installed {BUNDLE_NAME} version is older          '{version2}'"
        elif reason=="conflict_max":
            header = "Version conflict."
            detail = f"\nThe test execution requires maximum {BUNDLE_NAME} version '{version1}'"
            detail +=f"\nbut the installed {BUNDLE_NAME} version is younger        '{version2}'"
        elif reason=="wrong_minmax":
            header = "Wrong use of max/min version control in configuration."
            detail = f"\nThe configured minimum {BUNDLE_NAME} version                 '{version1}'"
            detail +=f"\nis younger than the configured maximum {BUNDLE_NAME} version '{version2}'"
            detail +="\nPlease correct the values of 'Maximum_version', 'Minimum_version' in config file"
        else:
            return
        
        BuiltIn().log(f"{header}" +
        f"\nTestsuite : {BuiltIn().get_variable_value('${SUITE SOURCE}')}" +
        f"\nconfig    : {self.sTestCfgFile}" +
        f"\n{detail}\n"
        f"\nPlease install the required {BUNDLE_NAME} version." +
        f"\nYou can find an installer here: {INSTALLER_LOCATION}\n", "ERROR")
        BuiltIn().unknown('Version control error!!!')

if __name__ == "__main__":
    bundle_version()
