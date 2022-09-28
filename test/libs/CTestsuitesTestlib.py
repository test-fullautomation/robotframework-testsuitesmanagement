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

# -- import standard Python modules
import pickle, os, time, re

# -- import Robotframework API
from robot.api.deco import keyword, library # required when using @keyword, @library decorators
from robot.libraries.BuiltIn import BuiltIn

# -- import own Python modules
from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.File.CFile import CFile
from PythonExtensionsCollection.Utils.CUtils import *

# --------------------------------------------------------------------------------------------------------------

sThisModuleName    = "CTestsuitesTestlib.py"
sThisModuleVersion = "0.1.0"
sThisModuleDate    = "28.09.2022"
sThisModule        = f"{sThisModuleName} v. {sThisModuleVersion} / {sThisModuleDate}"

# --------------------------------------------------------------------------------------------------------------
# 
@library
class CTestsuitesTestlib():
   """Test library to support the self test of the testsuites management
   """

   ROBOT_AUTO_KEYWORDS   = False # only decorated methods are keywords
   ROBOT_LIBRARY_VERSION = sThisModuleVersion
   ROBOT_LIBRARY_SCOPE   = 'GLOBAL'

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def __init__(self, sThisModule=sThisModule):

      self.__sThisModule = sThisModule
      self.__sConfigFile = None

   def __del__(self):
      pass

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def set_config_file_as_reference(self, sConfigFile=None):
      """Sets the configuration file that is used by the test suite.
(In other keywords of this library we read in the content and we use this content to check,
if the same information is available at robot level also.)
      """

      if sConfigFile is None:
         bSuccess = False
         sResult  = "Error: sConfigFile is None"
         return bSuccess, sResult

      # In case of sConfigFile contains a relative path, we need to define exactly that shall be the reference path.
      # We do not know exactly at which level the Robot Framework execution starts; therefore we do not use ${SUITE SOURCE}
      # for this purpose.
      # Instead of this we use the knowledge about the file system structure of the test folder - and we start with the
      # position of this library file.

      sReferencePathAbs = os.path.dirname(os.path.dirname(CString.NormalizePath(__file__)))
      sConfigFile = CString.NormalizePath(sConfigFile, sReferencePathAbs=sReferencePathAbs)

      if os.path.isfile(sConfigFile) is False:
         bSuccess = False
         sResult  = f"Error: Configuration file '{sConfigFile}' not found"
         return bSuccess, sResult

      BuiltIn().log(f"Reference configuration file: '{sConfigFile}'", "INFO")

      self.__sConfigFile = sConfigFile

      bSuccess = True
      sResult  = "Config file is set"
      return bSuccess, sResult

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   @keyword
   def get_maximum_version(self):
      """Reads the Maximum_version from configuration file.
      """

      sMaximumVersion = None

      if self.__sConfigFile is None:
         bSuccess = False
         sResult  = "Error: Configuration file not yet defined. Use 'set_config_file_as_reference' to define."
         return sMaximumVersion, bSuccess, sResult

      oFile = CFile(self.__sConfigFile)
      listLines, bSuccess, sResult = oFile.ReadLines(
                                                      bCaseSensitive  = True,
                                                      bSkipBlankLines = True,
                                                      sContains       = "Maximum_version",
                                                      bLStrip         = True,
                                                      bRStrip         = True,
                                                      bToScreen       = False
                                                     )
      del oFile
      if bSuccess is not True:
         return sMaximumVersion, bSuccess, sResult

      sPattern_maximum_version = r"\"Maximum_version\"\s*:\s*\"(.+?)\""
      regex_maximum_version    = re.compile(sPattern_maximum_version)

      # We do not expect several positions, but to be on the save side we compute a list of versions.
      # And we go another way as the testsuites management does: We read in the file in text format; we do not use any json interfaces.
      # Therefore we also hit lines, that are commented out.
      listMaximumVersions = []
      for sLine in listLines:
         for sMaximumVersion in regex_maximum_version.findall(sLine):
            listMaximumVersions.append(sMaximumVersion)
      sMaximumVersion = "; ".join(listMaximumVersions)
      if sMaximumVersion == "":
         bSuccess = False
         sResult  = "Error: Not able to parse the maximum version from selected config file"
         return sMaximumVersion, bSuccess, sResult

      bSuccess = True
      sResult  = "Got maximum version"
      return sMaximumVersion, bSuccess, sResult

   # eof def get_maximum_version(self):


   # --------------------------------------------------------------------------------------------------------------
   #TM***
   # --------------------------------------------------------------------------------------------------------------
   #TM***

# eof class CTestsuitesTestlib():

