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
# Base on TML Framework automation concept
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

from RobotFramework_Testsuites.Utils.CStruct import CStruct

from JsonPreprocessor import CJsonPreprocessor
from robot.api import logger
from robot.version import get_full_version, get_version
from robot.libraries.BuiltIn import BuiltIn
import pathlib

# This is version information represents for the whole AIO bundle
# It contains the core robotframework and relative resources such as:
# testsuitesmanagement, testresultwebapptool, Eclipse for RobotFramework, ...
# This information is used for Robotframework AIO version control 
AIO_BUNDLE_NAME = "RobotFramework AIO"
VERSION         = "0.5.2"
VERSION_DATE    = "09.2022"

class dotdict(dict):
    '''
**Subclass: dotdict**
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
**Class: CConfig**

   Defines the properties of configuration

   Holds the identified config files.

   Level1 is highest priority, Level4 is lowest priority.

   **Level1:** Handed over by command line argument.
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

      According to the ``ConfigName``, Testsuites-Management package will choose the corresponding config file. 
``".../config/"`` indicats the relative path to json config file, Testsuites-Management will recursively 
find the ``config`` folder.

   **Level3:** Read in testsuite folder ``/config/robot_config.json``
   **Level4:** Read from RobotFramework AIO install folder ``/RobotFramework/defaultconfig/robot_config.json``
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
    rConfigFiles   = CStruct(
                                sLevel1 = False,
                                sLevel2 = False,
                                sLevel3 = False,
                                sLevel4 = True   #'.../RobotFramework_Testsuites/Config/robot_config.json'
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
**Class: CJsonDotDict**
   The CJsonDotDict class converts json configuration object to dotdict
        '''
        def __init__(self):
            self.lTmpParam = ['CConfig.ddictJson']
            
        def __del__(self):
            CConfig.ddictJson = dotdict()
            del self.lTmpParam

        def dotdictConvert(self, oJson):
            '''
**Method: dotdictConvert**
   This dotdictConvert method converts json object to dotdict.

**Arguments:**

* ``oJson``

   / *Condition*: required / *Type*: dict

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
                        logger.info("Could not convert: %s to dotdict" %(sExec))
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
                                logger.info("Could not convert: %s to dotdict" %(sExec))
                                pass
                            
                            self.dotdictConvert(item)
                        n = n+1
            self.lTmpParam = self.lTmpParam[:-1]
            return CConfig.ddictJson
     
    def __new__(classtype, *args, **kwargs):
        '''
**Method: __new__**
   Makes the CConfig class to singleton.
   
   Checks to see if a __single exists already for this class. 
Compare class types instead of just looking for None so that subclasses will create 
their own __single objects. 
        '''
        if classtype != type(classtype.__single):
            classtype.__single = object.__new__(classtype)
        return classtype.__single

    def __init__(self):
        pass
        

    @staticmethod
    def loadCfg(self):
        '''
**Method: loadCfg**
   This loadCfg method uses to load configuration's parameters from json files.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        if not self.rConfigFiles.sLevel1:
            if self.rConfigFiles.sLevel2:
                self.rConfigFiles.sLevel4 = False
                self.__loadConfigFileLevel2()
            else:
                bLevel3Check = False
                if os.path.isdir(self.sTestcasePath + 'config'):
                    sSuiteFileName = BuiltIn().get_variable_value('${SUITE_SOURCE}').split(os.path.sep)[-1:][0]
                    for file in os.listdir(self.sTestcasePath + 'config'):
                        if file.split('.')[0] == sSuiteFileName.split('.')[0]:
                            self.sTestCfgFile = self.sTestcasePath + 'config' + os.path.sep + file
                            self.rConfigFiles.sLevel4 = False
                            bLevel3Check = True
                            break
                    if not bLevel3Check:
                        if os.path.isfile(self.sTestcasePath + 'config' + os.path.sep + 'robot_config.json'):
                            self.sTestCfgFile = self.sTestcasePath + 'config' + os.path.sep + 'robot_config.json'
                            self.rConfigFiles.sLevel4 = False
                        else:
                            self.rConfigFiles.sLevel3 = False
                            if not self.bConfigLoaded:
                                #self.rConfigFiles.sLevel4 = True
                                sDefaultConfig=str(pathlib.Path(__file__).parent.absolute() / "robot_config.json")
                                self.sTestCfgFile = sDefaultConfig
                else:
                    self.rConfigFiles.sLevel3 = False
                    if not self.bConfigLoaded:
                        #self.rConfigFiles.sLevel4 = True
                        sDefaultConfig=str(pathlib.Path(__file__).parent.absolute() / "robot_config.json")
                        self.sTestCfgFile = sDefaultConfig

        if self.bConfigLoaded:
            if self.rConfigFiles.sLevel1:
                return
            elif not self.rConfigFiles.sLevel2 and not self.rConfigFiles.sLevel3:
                return
        
        if self.rConfigFiles.sLevel1 and self.sTestCfgFile == '':
            logger.error("The config_file input parameter is empty!!!")
            raise Exception("The config_file input parameter is empty!!!")
        elif not (os.path.isfile(self.sTestCfgFile)):
           raise Exception("Did not find configuration file: '%s'!" % self.sTestCfgFile)
        
        robotCoreData = BuiltIn().get_variables()
        ROBFW_AIO_Data = {}
        for k, v in robotCoreData.items():
            key = re.findall("\s*{\s*(.+)\s*}\s*", k)[0]
            if 'CONFIG' == key:
                continue
            ROBFW_AIO_Data.update({key:v})
        oJsonPreprocessor = CJsonPreprocessor(syntax="python", currentCfg=ROBFW_AIO_Data)
        try:
            oJsonCfgData = oJsonPreprocessor.jsonLoad(self.__sNormalizePath(os.path.abspath(self.sTestCfgFile)))
        except Exception as error:
            CConfig.bLoadedCfg = False
            CConfig.sLoadedCfgError = str(error)
            logger.error("Loading of JSON configuration file failed! Reason: %s" %(CConfig.sLoadedCfgError))
            raise Exception

        bJsonSchema = True    
        try:
            sSchemaFile=str(pathlib.Path(__file__).parent.absolute() / "robot_schema.json")
            with open(sSchemaFile) as f:
                oJsonSchemaCfg = json.load(f)
        except Exception as err:
            bJsonSchema = False
            logger.error("Could not parse configuration json schema file: '%s'" % str(err))
    
        if bJsonSchema:
            try:
                validate(instance=oJsonCfgData, schema=oJsonSchemaCfg)
            except Exception as error:
                if error.validator == 'additionalProperties':
                    logger.error("Verification against json schema failed: '%s'" %(error.message))
                    logger.error("Additional properties are not allowed! \n \
                    Please put the additional params to 'preprocessor': { 'definitions' : {...} or 'params': { 'global': {...}")
                    raise Exception("Verification against json schema failed: '%s'" %(error.message))
                elif error.validator == 'required':
                    logger.error("The parameter %s, but it's not set in JSON configuration file." % (error.message))
                    raise Exception("The parameter %s, but it's missing in JSON configuration file." % (error.message))
                else:
                    errParam = error.path.pop()
                    logger.error("Parameter '%s' in JSON configuration file is not allowed due to: %s" % (errParam, error.message))
                    raise Exception("Parameter '%s' in JSON configuration file is not allowed due to: %s" % (errParam, error.message))
            
        self.sProjectName = oJsonCfgData['Project']
        self.sTargetName = oJsonCfgData['TargetName']
        self.sWelcomeString = oJsonCfgData['WelcomeString']
        if ("Maximum_version" in oJsonCfgData):
            self.sMaxVersion = oJsonCfgData["Maximum_version"]
        if ("Minimum_version" in oJsonCfgData):
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
            logger.info("Could not convert json config to dotdict!!!")
            pass
        del dotdictObj
        
        if bDotdict:
            BuiltIn().set_global_variable("${CONFIG}", jsonDotdict)
        else:
            BuiltIn().set_global_variable("${CONFIG}",oJsonCfgData)
        self.bConfigLoaded = True
        
    def updateCfg(sUpdateCfgFile):
        '''
**Method: updateCfg**
   This updateCfg method updates preprocessor, global or local params base on RobotFramework AIO local 
config or any json config file according to purpose of specific testsuite.

**Arguments:**

* ``sUpdateCfgFile``

   / *Condition*: required / *Type*: string

   The path of json file which wants to update configuration parameters.

**Returns:**

* No return variable       
        '''
        oJsonPreprocessor = CJsonPreprocessor(syntax="python", currentCfg=CConfig.oConfigParams)
        try:
            oUpdateParams = oJsonPreprocessor.jsonLoad(CConfig.__sNormalizePath(os.path.abspath(sUpdateCfgFile)))
        except Exception as error:
            CConfig.bLoadedCfg = False
            CConfig.sLoadedCfgError = str(error)
            logger.error("Loading of JSON configuration file failed! Reason: %s" %(CConfig.sLoadedCfgError))
            raise Exception
            
        if bool(oUpdateParams):
            CConfig.oConfigParams.update(oUpdateParams)
        oTmpJsonCfgData = copy.deepcopy(CConfig.oConfigParams)
        try:    
            del oTmpJsonCfgData['params']['global']
        except:
            pass  
        
        try:
            del oTmpJsonCfgData['preprocessor']['definitions']
        except:
            pass
        
        BuiltIn().set_global_variable("${CONFIG}", oTmpJsonCfgData)
        del oTmpJsonCfgData
        CConfig.__updateGlobalVariable(CConfig)
        
    def __setGlobalVariable(self, key, value):
        '''
**Method: __setGlobalVariable**
   This method set RobotFramework AIO global variable from config object.

**Arguments:**

* ``key``

   / *Condition*: required / *Type*: string

   key is set as global variable of RobotFramework AIO, user can call ${<key>} in test script.

* ``value``

   / *Condition*: required / *Type*: <variant datatypes>

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
                logger.info("Could not convert json config to dotdict!!!")
                pass
            del dotdictObj
            if bDotdict:
                BuiltIn().set_global_variable("${%s}" % k.strip(), jsonDotdict)
            else:
                BuiltIn().set_global_variable("${%s}" % k.strip(), v)
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
                        logger.info("Could not convert json config to dotdict!!!")
                        pass
                    if bDotdict:
                        tmpList.append(jsonDotdict)
                    else:
                        tmpList.append(item)
                else:
                    tmpList.append(item)
            BuiltIn().set_global_variable("${%s}" % k.strip(), tmpList)
        else:         
            BuiltIn().set_global_variable("${%s}" % k.strip(), v)
            
    def __updateGlobalVariable(self):
        '''
**Method: __updateGlobalVariable**
   This method updates preprocessor and global params to global variable of RobotFramework AIO.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        try:
            for k,v in self.oConfigParams['preprocessor']['definitions'].items():
                try:
                    self.__setGlobalVariable(k, v)
                except:
                    logger.info("The parameter %s is updated" %k.strip())
                    continue
        except:
            pass
        
        try:
            for k,v in self.oConfigParams['params']['global'].items():
                try:
                    self.__setGlobalVariable(k, v)
                except:
                    logger.info("The parameter %s is updated" %k.strip())
                    continue
        except:
            pass  
        
    def __del__(self):
        '''
**Method: __del__**
   This destructor method.

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        pass
    
    def __loadConfigFileLevel2(self):
        '''
**Method: __loadConfigFileLevel2**
   This __loadConfigFileLevel2 method loads configuration in case rConfigFiles.sLevel2 == True.

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
            logger.error("Loading of JSON configuration file failed! Reason: %s" %(CConfig.sLoadedCfgError))
            raise Exception
        
        try:
            defualtCfg = oSuiteConfig['default']['name']
        except:
            logger.error("Testsuite management is in configuration level2.")
            logger.error("The file '%s' has no default config or wrong testsuite config format for level 2" %(self.sTestSuiteCfg))
            logger.error("Testsuite will run with default config file: %s " %(self.sTestCfgFile))
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
                    raise Exception('Could not find out config directory: %s' %(sTestCfgDirStart))
                
        self.sTestCfgFile = sTestCfgDir + self.sTestCfgFile

    def __sNormalizePath(self, sPath : str) -> str:
        '''
**Method: __sNormalizePath**
   Python struggles with

      - UNC paths

         e.g. ``\\hi-z4939\ccstg\....``


      - escape sequences in windows paths

         e.g. ``c:\autotest\tuner   \t`` will be interpreted as tab, the result 
after processing it with an regexp would be ``c:\autotest   uner``
    
      In order to solve this problems any slash will be replaced from backslash 
to slash, only the two UNC backslashes must be kept if contained.

**Arguments:**

* ``sPath``

   / *Condition*: required / *Type*: string

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
**Method: __getMachineName**
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
**Method: __getUserName**
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
**Method: verifyRbfwVersion**

   This verifyRbfwVersion validates the current RobotFramework AIO version with maximum and minimum
version (if provided in the configuration file).

   In case the current version is not between min and max version, then the execution of 
testsuite is terminated with "unknown" state

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
**Method: bValidateMinVersion**
   This bValidateMinVersion validates the current version with required minimun version.

**Arguments:**

* ``tCurrentVersion``

   / *Condition*: required / *Type*: tuple

   Current RobotFramework AIO version.

* ``tMinVersion``

   / *Condition*: required / *Type*: tuple

   The minimum version of RobotFramework AIO.

**Returns:**

* ``True or False``
        '''
        return tCurrentVersion >= tMinVersion

    @staticmethod
    def bValidateMaxVersion(tCurrentVersion, tMaxVersion):
        '''
**Method: bValidateMaxVersion**
   This bValidateMaxVersion validates the current version with required minimun version.

**Arguments:**

* ``tCurrentVersion``

   / *Condition*: required / *Type*: tuple

   Current RobotFramework AIO version.

* ``tMinVersion``

   / *Condition*: required / *Type*: tuple

   The minimum version of RobotFramework AIO.

**Returns:**

* ``True or False``
        '''
        return tCurrentVersion <= tMaxVersion

    @staticmethod
    def bValidateSubVersion(sVersion):
        '''
**Method: bValidateSubVersion**
   This bValidateSubVersion validates the format of provided sub version and parse it into sub tuple 
for version comparision.

**Arguments:**

* ``sVersion``

   / *Condition*: required / *Type*: string

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
**Method: tupleVersion**

   This tupleVersion returns a tuple which contains the (major, minor, patch) version. 

   (remaining content needs to be fixed and restored)

**Arguments:**

* ``sVersion``

   / *Condition*: required / *Type*: string

   The version of RobotFramework AIO.

**Returns:**

* ``lVersion``

   / *Type*: tuple /
        '''
        # '''
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
            BuiltIn().fatal_error("Provided version '%s' is not a correct version format."%sVersion)

    def versioncontrol_error(self, reason, version1, version2):
        '''
**Method: versioncontrol_error**

   Wrapper version control error log:

      Log error message of version control due to reason and set to unknown state.

      `reason` can only be "conflict_min", "conflict_max" and "wrong_minmax".

**Arguments:**

* ``reason``

   / *Condition*: required / *Type*: string

* ``version1``

   / *Condition*: required / *Type*: string

* ``version2``

   / *Condition*: required / *Type*: string

**Returns:**

* No return variable
        '''
        sLocation = "\\\\bosch.com\\dfsrb\\DfsDE\\DIV\\CM\\DI\\Projects\\Common\\RobotFramework\\Releases"
        header = ""
        detail = ""
        if reason=="conflict_min":
            header = "Version conflict."
            detail = f"\nThe configuration requires minimum Robotframework AIO version '{version1}'"
            detail +=f"\nbut the installed Robotframework AIO version is older         '{version2}'"
        elif reason=="conflict_max":
            header = "Version conflict."
            detail = f"\nThe configuration requires maximum Robotframework AIO version '{version1}'"
            detail +=f"\nbut the installed Robotframework AIO version is younger       '{version2}'"
        elif reason=="wrong_minmax":
            header = "Wrong use of max/min version control in configuration."
            detail = f"\nThe configured minimum Robotframework AIO version                 '{version1}'"
            detail +=f"\nis younger than the configured maximum Robotframework AIO version '{version2}'"
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