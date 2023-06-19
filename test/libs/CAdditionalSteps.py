# **************************************************************************************************************
#
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
#
# **************************************************************************************************************
#
# CAdditionalSteps.py
#
# XC-CT/ECA3-Queckenstedt
#
# 15.05.2023
#
# --------------------------------------------------------------------------------------------------------------

"""
All test steps to be executed additionally to what is defined in TestConfig.py.
Purpose: pre- and post actions
"""

# --------------------------------------------------------------------------------------------------------------

import os, sys, time
import colorama as col

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.File.CFile import CFile
from PythonExtensionsCollection.Folder.CFolder import CFolder
from PythonExtensionsCollection.Utils.CUtils import *

## ? from testconfig.TestConfig import *

col.init(autoreset=True)
COLBR = col.Style.BRIGHT + col.Fore.RED
COLBG = col.Style.BRIGHT + col.Fore.GREEN
COLBY = col.Style.BRIGHT + col.Fore.YELLOW
COLNY = col.Style.NORMAL + col.Fore.YELLOW
COLBW = col.Style.BRIGHT + col.Fore.WHITE

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg):
   sys.stderr.write(COLBR + f"Error: {sMsg}!\n")

# --------------------------------------------------------------------------------------------------------------

## TODO: enstepnames



# --------------------------------------------------------------------------------------------------------------

class CAdditionalSteps():
   """
   """

   def __init__(self, oConfig=None):
      """
      """

      sMethod = "CAdditionalSteps.__init__"

      if oConfig is None:
         raise Exception(CString.FormatResult(sMethod, None, "oConfig is None"))

      self.__oConfig = oConfig

      self.__CONFIGSCHEMAFILE = self.__oConfig.Get('CONFIGSCHEMAFILE')
      self.__CONFIGSCHEMAFILE_backup = f"{self.__CONFIGSCHEMAFILE}_backup"

   # --------------------------------------------------------------------------------------------------------------

   def Execute(self, sStepName=None):
      """
      """

      sMethod = "Execute"

      REFERENCEPATH = self.__oConfig.Get('REFERENCEPATH')

      if sStepName == "ConfigSchemaFile_Remove":
         bSuccess, sResult = self.__ConfigSchemaFile_Remove()
         if bSuccess is not True:
            sResult = CString.FormatResult(sMethod, bSuccess, sResult)
      elif sStepName == "ConfigSchemaFile_MakeInvalid":
         bSuccess, sResult = self.__ConfigSchemaFile_MakeInvalid()
         if bSuccess is not True:
            sResult = CString.FormatResult(sMethod, bSuccess, sResult)
      elif sStepName == "ConfigSchemaFile_Restore":
         bSuccess, sResult = self.__ConfigSchemaFile_Restore()
         if bSuccess is not True:
            sResult = CString.FormatResult(sMethod, bSuccess, sResult)

      elif sStepName == "LocalConfigEnvVar_Create":
         bSuccess, sResult = self.__LocalConfigEnvVar_Create()
         if bSuccess is not True:
            sResult = CString.FormatResult(sMethod, bSuccess, sResult)
      elif sStepName == "LocalConfigEnvVar_Delete":
         bSuccess, sResult = self.__LocalConfigEnvVar_Delete()
         if bSuccess is not True:
            sResult = CString.FormatResult(sMethod, bSuccess, sResult)


      else:
         bSuccess = False
         sResult  = f"Step name '{sStepName}' is not defined"
         return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

      print()

      return bSuccess, sResult

   # eof def Execute(self, sStepName=None):

   # --------------------------------------------------------------------------------------------------------------

   # -- config schema

   def __ConfigSchemaFile_Remove(self):
      oFile = CFile(self.__CONFIGSCHEMAFILE)
      bSuccess, sResult = oFile.MoveTo(self.__CONFIGSCHEMAFILE_backup, bOverwrite=True)
      del oFile
      return bSuccess, sResult

   def __ConfigSchemaFile_MakeInvalid(self):
      oFile = CFile(self.__CONFIGSCHEMAFILE)
      bSuccess, sResult = oFile.CopyTo(self.__CONFIGSCHEMAFILE_backup, bOverwrite=True)
      if bSuccess is not True:
         del oFile
         return bSuccess, sResult
      bSuccess, sResult = oFile.Append("}}}:{{{ I am syntax error!")
      del oFile
      return bSuccess, sResult

   def __ConfigSchemaFile_Restore(self):
      oFile = CFile(self.__CONFIGSCHEMAFILE_backup)
      bSuccess, sResult = oFile.MoveTo(self.__CONFIGSCHEMAFILE, bOverwrite=True)
      del oFile
      return bSuccess, sResult

   # -- local config

   def __LocalConfigEnvVar_Create(self):
      TESTFILESFOLDER = self.__oConfig.Get('TESTFILESFOLDER')
      sLocalConfigFile = f"{TESTFILESFOLDER}/localconfig/tsm-test_localconfig_bench2.jsonp"
      if not os.path.isfile(sLocalConfigFile):
         bSuccess = None
         sResult  = "Missing file '{sLocalConfigFile}'"
         return bSuccess, sResult
      os.environ['ROBOT_LOCAL_CONFIG'] = f"{sLocalConfigFile}"
      bSuccess = True
      sResult  = "'ROBOT_LOCAL_CONFIG' set to '{sLocalConfigFile}'"
      return bSuccess, sResult

   def __LocalConfigEnvVar_Delete(self):
      if 'ROBOT_LOCAL_CONFIG' in os.environ:
         del os.environ['ROBOT_LOCAL_CONFIG']
      bSuccess = True
      sResult  = "'ROBOT_LOCAL_CONFIG' removed"
      return bSuccess, sResult

   # --------------------------------------------------------------------------------------------------------------
   # --------------------------------------------------------------------------------------------------------------
   # --------------------------------------------------------------------------------------------------------------

# eof class CAdditionalSteps():

# **************************************************************************************************************

