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

from JsonPreprocessor import CJsonPreprocessor
from robot.api import logger
from robot.version import get_full_version, get_version
from robot.libraries.BuiltIn import BuiltIn
import pathlib

# This is version information represents for the whole AIO bundle
# It contains the core Robot Framework and relative resources such as:
# RobotFramework_TestsuitesManagement, RobotLog2DB, VSCodium for Robot Framework, ...
# This information is used for RobotFramework AIO version control 
AIO_BUNDLE_NAME = "RobotFramework AIO"
VERSION         = "0.6.0"
VERSION_DATE    = "01.2023"

class dotdict(dict):
    '''
Subclass of dict, with "dot" (attribute) access to keys.
    '''
    __setattr__ = dict.__setitem__
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as error:
            raise AttributeError from error
    __delattr__ = dict.__delitem__


class CConfig():
    '''
Defines the properties of configuration and holds the identified config files.

The loading configuration method is divided into 4 levels, level1 has the highest priority, Level4 has the lowest priority.

**Level1:** Handed over by command line argument

**Level2:** Read from content of json config file

   .. code:: json

      {
         "default": {
            "name": "robot_config.json",
            "path": ".../config/"
         },
         "variant_0": {
            "name": "robot_config.json",
            "path": ".../config/"
         },
         "variant_1": {
            "name": "robot_config_variant_1.json",
            "path": ".../config/"
         },
            ...
            ...
      }

   According to the ``ConfigName``, RobotFramework_TestsuitesManagement will choose the corresponding config file.
   ``".../config/"`` indicats the relative path to json config file, RobotFramework_TestsuitesManagement will recursively
   find the ``config`` folder.

**Level3:** Read in testsuite folder: ``/config/robot_config.json``

**Level4:** Read from RobotFramework AIO installation folder:

    ``/RobotFramework/defaultconfig/robot_config.json``
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
                                bLevel4 = True   #'.../RobotFramework_TestsuitesManagement/Config/robot_config.json'
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
    ddictJson = dotdict()
    
    class CJsonDotDict():
        '''
The CJsonDotDict class converts json configuration object to dotdict
        '''
        def __init__(self):
            self.lTmpParam = ['CConfig.ddictJson']
            
        def __del__(self):
            CConfig.ddictJson = dotdict()
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
                    sExec = sExec + " = dotdict(" + str(v) + ")"
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
                            sExec = sExec + " = dotdict(" + str(item) + ")"
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
        if not self.rConfigFiles.bLevel1:
            if self.rConfigFiles.bLevel2:
                self.rConfigFiles.bLevel4 = False
                self.__loadConfigFileLevel2()
            else:
                bLevel3Check = False
                if os.path.isdir(self.sTestcasePath + 'config'):
                    sSuiteFileName = BuiltIn().get_variable_value('${SUITE_SOURCE}').split(os.path.sep)[-1:][0]
                    for file in os.listdir(self.sTestcasePath + 'config'):
                        if file.split('.')[0] == sSuiteFileName.split('.')[0]:
                            self.sTestCfgFile = self.sTestcasePath + 'config' + os.path.sep + file
                            self.rConfigFiles.bLevel4 = False
                            bLevel3Check = True
                            break
                    if not bLevel3Check:
                        if os.path.isfile(self.sTestcasePath + 'config' + os.path.sep + 'robot_config.json'):
                            self.sTestCfgFile = self.sTestcasePath + 'config' + os.path.sep + 'robot_config.json'
                            self.rConfigFiles.bLevel4 = False
                        else:
                            self.rConfigFiles.bLevel3 = False
                            if not self.bConfigLoaded:
                                #self.rConfigFiles.bLevel4 = True
                                sDefaultConfig=str(pathlib.Path(__file__).parent.absolute() / "robot_config.json")
                                self.sTestCfgFile = sDefaultConfig
                else:
                    self.rConfigFiles.bLevel3 = False
                    if not self.bConfigLoaded:
                        #self.rConfigFiles.bLevel4 = True
                        sDefaultConfig=str(pathlib.Path(__file__).parent.absolute() / "robot_config.json")
                        self.sTestCfgFile = sDefaultConfig

            if self.sTestCfgFile != '':                      
                self.sTestCfgFile = os.path.abspath(self.sTestCfgFile)

        if self.bConfigLoaded:
            if self.rConfigFiles.bLevel1:
                return
            elif not self.rConfigFiles.bLevel2 and not self.rConfigFiles.bLevel3:
                return
        
        if self.rConfigFiles.bLevel1:
            if self.sConfigName != 'default':
                errorMessage = f"Redundant settings detected in command line: Parameter 'variant' is used together with parameter 'config_file'.\n\
It is not possible to use both together, because they belong to the same feature (the variant selection).\n\
Please remove one of them.\n"
                logger.error(errorMessage)
                BuiltIn().unknown(errorMessage)

            if self.sTestCfgFile == '':
                errorMessage = "The config_file input parameter is empty!!!"
                logger.error(errorMessage)
                BuiltIn().unknown(errorMessage)

        if not os.path.isfile(self.__sNormalizePath(self.sTestCfgFile)):
            errorMessage = f"Did not find configuration file: '{self.sTestCfgFile}'!"
            logger.error(errorMessage)
            BuiltIn().unknown(errorMessage)
        
        robotCoreData = BuiltIn().get_variables()
        ROBFW_AIO_Data = {}
        for k, v in robotCoreData.items():
            key = re.findall("\s*{\s*(.+)\s*}\s*", k)[0]
            if 'CONFIG' == key:
                continue
            ROBFW_AIO_Data.update({key:v})
        oJsonPreprocessor = CJsonPreprocessor(syntax="python", currentCfg=ROBFW_AIO_Data)
        try:
            oJsonCfgData = oJsonPreprocessor.jsonLoad(self.__sNormalizePath(self.sTestCfgFile))
        except Exception as error:
            CConfig.bLoadedCfg = False
            CConfig.sLoadedCfgError = str(error)
            logger.error(f"Loading of JSON configuration file failed! Reason: {CConfig.sLoadedCfgError}")
            raise Exception

        if self.sLocalConfig != '':
            try:
                oLocalConfig = oJsonPreprocessor.jsonLoad(self.__sNormalizePath(self.sLocalConfig))
            except Exception as error:
                CConfig.bLoadedCfg = False
                CConfig.sLoadedCfgError = str(error)
                logger.error(f"Loading local config failed! Reason: {CConfig.sLoadedCfgError}")
                BuiltIn().unknown(CConfig.sLoadedCfgError)
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
            sSchemaFile=str(pathlib.Path(__file__).parent.absolute() / "robot_schema.json")
            with open(sSchemaFile) as f:
                oJsonSchemaCfg = json.load(f)
        except Exception as err:
            bJsonSchema = False
            logger.error(f"Could not parse configuration JSON schema file: '{str(err)}'")
    
        if bJsonSchema:
            try:
                validate(instance=oJsonCfgData, schema=oJsonSchemaCfg)
            except Exception as error:
                if error.validator == 'additionalProperties':
                    logger.error(f"Verification against JSON schema failed: '{error.message}'")
                    logger.error("Additional properties are not allowed! \n \
                    Please put the additional params into 'params': { 'global': {...}")
                    raise Exception(f"Verification against json schema failed: '{error.message}'")
                elif error.validator == 'required':
                    logger.error(f"The parameter {error.message}, but it's not set in JSON configuration file.")
                    raise Exception(f"The parameter {error.message}, but it's missing in JSON configuration file.")
                else:
                    errParam = error.path.pop()
                    logger.error(f"Parameter '{errParam}' with invalid value found in JSON configuration file!\n{error.message}")
                    raise Exception(f"Parameter '{errParam}' with invalid value found in JSON configuration file!\n{error.message}")
            
        self.sProjectName = oJsonCfgData['Project']
        self.sTargetName = oJsonCfgData['TargetName']
        self.sWelcomeString = oJsonCfgData['WelcomeString']
        if ("Maximum_version" in oJsonCfgData) and oJsonCfgData["Maximum_version"] != None:
            self.sMaxVersion = oJsonCfgData["Maximum_version"]
        if ("Minimum_version" in oJsonCfgData) and oJsonCfgData["Minimum_version"] != None:
            self.sMinVersion = oJsonCfgData["Minimum_version"]

        # Set metadata at top level
        BuiltIn().set_suite_metadata("project", self.sProjectName, top=True)
        BuiltIn().set_suite_metadata("version_sw", self.rMetaData.sVersionSW, top=True)
        BuiltIn().set_suite_metadata("version_hw", self.rMetaData.sVersionHW, top=True)
        BuiltIn().set_suite_metadata("version_test", self.rMetaData.sVersionTest, top=True)
        BuiltIn().set_suite_metadata("machine", self.__getMachineName(), top=True)
        BuiltIn().set_suite_metadata("tester", self.__getUserName(), top=True)
        BuiltIn().set_suite_metadata("testtool", self.rMetaData.sROBFWVersion, top=True)
        BuiltIn().set_suite_metadata("version", VERSION, top=True)
        
        CConfig.oConfigParams = copy.deepcopy(oJsonCfgData)
        
        self.__updateGlobalVariable()
        try:    
            del oJsonCfgData['params']['global']
        except:
            pass  
        
        try:
            del oJsonCfgData['preprocessor']['definitions']
        except:
            pass 
        
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
        try:
            for k,v in self.oConfigParams['preprocessor']['definitions'].items():
                if k in self.lBuitInVariables:
                    continue
                try:
                    self.__setGlobalVariable(k, v)
                except:
                    logger.info(f"The parameter {k.strip()} is updated")
                    continue
        except:
            pass
        
        try:
            for k,v in self.oConfigParams['params']['global'].items():
                if k in self.lBuitInVariables:
                    continue
                try:
                    self.__setGlobalVariable(k, v)
                except:
                    logger.info(f"The parameter {k.strip()} is updated")
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
    
    def __loadConfigFileLevel2(self):
        '''
This __loadConfigFileLevel2 method loads configuration in case rConfigFiles.bLevel2 == True.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        
        oJsonPreprocessor = CJsonPreprocessor(syntax="python")
        try:
            oSuiteConfig = oJsonPreprocessor.jsonLoad(self.__sNormalizePath(os.path.abspath(self.sTestSuiteCfg)))
        except Exception as error:
            CConfig.bLoadedCfg = False
            CConfig.sLoadedCfgError = str(error)
            logger.error(f"Loading of JSON configuration file failed! Reason: {CConfig.sLoadedCfgError}")
            raise Exception
        
        try:
            defualtCfg = oSuiteConfig['default']['name']
        except:
            CConfig.sLoadedCfgError = f"Testsuite management - Loading configuration level 2 failed! \n \
                The variant '{self.sConfigName}' is not defined in '{os.path.abspath(self.sTestSuiteCfg)}'"
            logger.error(CConfig.sLoadedCfgError)
            return
        
        self.sTestCfgFile = oSuiteConfig[self.sConfigName]['name']
        sTestCfgDir = oSuiteConfig[self.sConfigName]['path']
            
        if sTestCfgDir.startswith('.../'):
            sTestCfgDirStart = sTestCfgDir
            sTestCfgDir = sTestCfgDir[4:]
            if os.path.exists(self.__sNormalizePath(os.path.abspath('./' + sTestCfgDir))):
                sTestCfgDir = './' + sTestCfgDir
            else:
                bFoundTestCfgDir = False
                for i in range(0, 30):
                    sTestCfgDir = '../' + sTestCfgDir
                    if os.path.exists(self.__sNormalizePath(os.path.abspath(sTestCfgDir))):
                        bFoundTestCfgDir = True
                        break
                if bFoundTestCfgDir == False:
                    raise Exception(f"Could not find out config directory: {sTestCfgDirStart}")
                
        self.sTestCfgFile = sTestCfgDir + self.sTestCfgFile

    def __sNormalizePath(self, sPath : str) -> str:
        '''
Python struggles with

   - UNC paths

      e.g. ``\\hi-z4939\ccstg\....``


   - escape sequences in windows paths

      e.g. ``c:\autotest\tuner   \t`` will be interpreted as tab, the result after
      processing it with an regexp would be ``c:\autotest   uner``

   In order to solve this problems any slash will be replaced from backslash to slash,
   only the two UNC backslashes must be kept if contained.

**Arguments:**

* ``sPath``

   / *Condition*: required / *Type*: string /

   Absolute or relative path as input.

   Allows environment variables with ``%variable%`` or ``${variable}`` syntax.

**Returns:**

* ``sPath``

   / *Type*: string /

   Normalized path as string
        '''
        # make all backslashes to slash, but mask
        # UNC indicator \\ before and restore after.
        def __mkslash(sPath : str) -> str:
            if sPath.strip()=='':
                return ''
     
            sNPath=re.sub(r"\\\\",r"#!#!#",sPath.strip())
            sNPath=re.sub(r"\\",r"/",sNPath)
            sNPath=re.sub(r"#!#!#",r"\\\\",sNPath)
          
            return sNPath               
            if sPath.strip()=='':
                return ''
      
        # TML Syntax uses %Name%-syntax to reference an system- or framework
        # environment variable. Linux requires ${Name} to do the same.
        # Therefore change on Linux systems to ${Name}-syntax to make
        # expandvars working here, too.
        # This makes same TML code working on both platforms
        if platform.system().lower()!="windows":
            sPath=re.sub("%(.*?)%","${\\1}",sPath)
      
        #in a windows system normpath turns all slashes to backslash
        #this is unwanted. Therefore turn back after normpath execution.
        sNPath=os.path.normpath(os.path.expandvars(sPath.strip()))
        #make all backslashes to slash, but mask
        #UNC indicator \\ before and restore after.
        sNPath=__mkslash(sNPath)
      
        return sNPath
    
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
    
    def verifyRbfwVersion(self):
        '''
This verifyRbfwVersion validates the current RobotFramework AIO version with maximum and minimum version
(if provided in the configuration file).

In case the current version is not between min and max version, then the execution of testsuite is terminated
with "unknown" state

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        sCurrentVersion = VERSION
        tCurrentVersion = CConfig.tupleVersion(sCurrentVersion)
        
        # Verify format of provided min and max versions then parse to tuples
        tMinVersion = None
        tMaxVersion = None
        if self.sMinVersion != '':
            tMinVersion = CConfig.tupleVersion(self.sMinVersion)
        if self.sMaxVersion != '':
            tMaxVersion = CConfig.tupleVersion(self.sMaxVersion)

        if tMinVersion and tMaxVersion and (tMinVersion > tMaxVersion):
            self.versioncontrol_error('wrong_minmax', self.sMinVersion, self.sMaxVersion)

        if tMinVersion and not CConfig.bValidateMinVersion(tCurrentVersion, tMinVersion):
            self.versioncontrol_error('conflict_min', self.sMinVersion, sCurrentVersion)

        if tMaxVersion and not CConfig.bValidateMaxVersion(tCurrentVersion, tMaxVersion):
            self.versioncontrol_error('conflict_max', self.sMaxVersion, sCurrentVersion)

    @staticmethod
    def bValidateMinVersion(tCurrentVersion, tMinVersion):
        '''
This bValidateMinVersion validates the current version with required minimun version.

**Arguments:**

* ``tCurrentVersion``

  / *Condition*: required / *Type*: tuple /

  Current RobotFramework AIO version.

* ``tMinVersion``

  / *Condition*: required / *Type*: tuple /

  The minimum version of RobotFramework AIO.

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

  Current RobotFramework AIO version.

* ``tMinVersion``

  / *Condition*: required / *Type*: tuple /

  The minimum version of RobotFramework AIO.

**Returns:**

* ``True or False``
        '''
        return tCurrentVersion <= tMaxVersion

    @staticmethod
    def bValidateSubVersion(sVersion):
        '''
This bValidateSubVersion validates the format of provided sub version and parse it into sub tuple
for version comparision.

**Arguments:**

* ``sVersion``

  / *Condition*: required / *Type*: string /

  The version of RobotFramework AIO.

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

**Arguments:**

* ``sVersion``

  / *Condition*: required / *Type*: string /

  The version of RobotFramework AIO.

**Returns:**

* ``lVersion``

  / *Type*: tuple /
        '''
        # '''

# TODO: (remaining content needs to be fixed and restored)

        # Return a tuple which contains the (major, minor, patch) version.
          # - In case minor/patch version is missing, it is set to 0.
            # E.g: 1   => 1.0.0
                 # 1.1 => 1.1.0
          # - Support version contains Alpha (a), Beta (b) or Release candidate (rc):
            # E.g: 1.2rc3, 1.2.1b1, ...
        # '''
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
        sLocation = "\\\\bosch.com\\dfsrb\\DfsDE\\DIV\\CM\\DI\\Projects\\Common\\RobotFramework\\Releases"
        header = ""
        detail = ""
        if reason=="conflict_min":
            header = "Version conflict."
            detail = f"\nThe test execution requires minimum RobotFramework AIO version '{version1}'"
            detail +=f"\nbut the installed RobotFramework AIO version is older         '{version2}'"
        elif reason=="conflict_max":
            header = "Version conflict."
            detail = f"\nThe test execution requires maximum RobotFramework AIO version '{version1}'"
            detail +=f"\nbut the installed RobotFramework AIO version is younger       '{version2}'"
        elif reason=="wrong_minmax":
            header = "Wrong use of max/min version control in configuration."
            detail = f"\nThe configured minimum RobotFramework AIO version                 '{version1}'"
            detail +=f"\nis younger than the configured maximum RobotFramework AIO version '{version2}'"
            detail +="\nPlease correct the values of 'Maximum_version', 'Minimum_version' in config file"
        else:
            return
        
        BuiltIn().log(f"{header}" +
        f"\nTestsuite : {BuiltIn().get_variable_value('${SUITE SOURCE}')}" +
        f"\nconfig    : {self.sTestCfgFile}" +
        f"\n{detail}\n"
        "\nPlease install the required RobotFramework AIO version." +
        f"\nYou can find an installer here: {sLocation}\n", "ERROR")
        BuiltIn().unknown()
