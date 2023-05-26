# **************************************************************************************************************
#
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
#
# **************************************************************************************************************
#
# CConfig.py
#
# XC-CT/ECA3-Queckenstedt
#
# 03.04.2023
#
# --------------------------------------------------------------------------------------------------------------

"""
Python module containing the configuration for **component_test.py**.
"""

# --------------------------------------------------------------------------------------------------------------

import os, sys, time, platform, json, argparse
import colorama as col

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.File.CFile import CFile
from PythonExtensionsCollection.Folder.CFolder import CFolder
from PythonExtensionsCollection.Utils.CUtils import *

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

class CConfig():

   def __init__(self, sCalledBy=None):
      """
      """

      sMethod = "CConfig.__init__"

      if sCalledBy is None:
         raise Exception(CString.FormatResult(sMethod, None, "sCalledBy is None"))

      # -- configuration init
      self.__dictConfig = {}

      # -- configuration: basic environment

      THISSCRIPT = CString.NormalizePath(sCalledBy)
      self.__dictConfig['THISSCRIPT']     = THISSCRIPT
      self.__dictConfig['THISSCRIPTNAME'] = os.path.basename(THISSCRIPT)
      REFERENCEPATH = os.path.dirname(THISSCRIPT) # position of main() script is reference for all relative paths
      self.__dictConfig['REFERENCEPATH']  = REFERENCEPATH
      OSNAME = os.name
      self.__dictConfig['OSNAME']         = OSNAME
      PLATFORMSYSTEM = platform.system()
      self.__dictConfig['PLATFORMSYSTEM'] = PLATFORMSYSTEM
      PYTHON = CString.NormalizePath(sys.executable)
      self.__dictConfig['PYTHON']         = PYTHON
      PYTHONPATH = os.path.dirname(PYTHON)
      self.__dictConfig['PYTHONPATH']     = PYTHONPATH
      self.__dictConfig['PYTHONVERSION']  = sys.version

      # -- configuration: test environment
      # TODO maybe later: get this from external JSON config file

      NOTPATTERNFILE_TXT = f"{REFERENCEPATH}/testconfig/tsm_test_not_pattern_TXT.txt"
      if os.path.isfile(NOTPATTERNFILE_TXT) is False:
         raise Exception(CString.FormatResult(sMethod, False, f"'Not' pattern file not found: '{NOTPATTERNFILE_TXT}'"))
      self.__dictConfig['NOTPATTERNFILE_TXT'] = NOTPATTERNFILE_TXT # needed for log file pre check

      IGNOREPATTERNFILE_TXT = f"{REFERENCEPATH}/testconfig/tsm_test_ignore_pattern_TXT.txt"
      if os.path.isfile(IGNOREPATTERNFILE_TXT) is False:
         raise Exception(CString.FormatResult(sMethod, False, f"'Ignore' pattern file not found: '{IGNOREPATTERNFILE_TXT}'"))
      self.__dictConfig['IGNOREPATTERNFILE_TXT'] = IGNOREPATTERNFILE_TXT

      PATTERNFILE_TXT = f"{REFERENCEPATH}/testconfig/tsm_test_pattern_TXT.txt"
      if os.path.isfile(PATTERNFILE_TXT) is False:
         raise Exception(CString.FormatResult(sMethod, False, f"Pattern file not found: '{PATTERNFILE_TXT}'"))
      self.__dictConfig['PATTERNFILE_TXT'] = PATTERNFILE_TXT # needed for log file comparison

      PATTERNFILE_XML = f"{REFERENCEPATH}/testconfig/tsm_test_pattern_XML.txt"
      if os.path.isfile(PATTERNFILE_XML) is False:
         raise Exception(CString.FormatResult(sMethod, False, f"Pattern file not found: '{PATTERNFILE_XML}'"))
      self.__dictConfig['PATTERNFILE_XML'] = PATTERNFILE_XML # needed for log file comparison

      TESTFILESFOLDER = f"{REFERENCEPATH}/testfiles"
      if os.path.isdir(TESTFILESFOLDER) is False:
         raise Exception(CString.FormatResult(sMethod, False, f"Testfiles folder not found: '{TESTFILESFOLDER}'"))
      self.__dictConfig['TESTFILESFOLDER'] = TESTFILESFOLDER

      TESTLOGFILESFOLDER = f"{REFERENCEPATH}/testlogfiles"
      oFolder = CFolder(TESTLOGFILESFOLDER)
      bSuccess, sResult = oFolder.Create(bOverwrite=True, bRecursive=True)
      del oFolder
      if bSuccess is not True:
         raise Exception(CString.FormatResult(sMethod, bSuccess, sResult))
      self.__dictConfig['TESTLOGFILESFOLDER'] = TESTLOGFILESFOLDER

      self.__dictConfig['SELFTESTLOGFILE'] = f"{TESTLOGFILESFOLDER}/TSM_SelfTest.log"

      REFERENCELOGFILESFOLDER = f"{REFERENCEPATH}/referencelogfiles"
      if os.path.isdir(REFERENCELOGFILESFOLDER) is False:
         raise Exception(CString.FormatResult(sMethod, False, f"Reference log files folder not found: '{REFERENCELOGFILESFOLDER}'"))
      self.__dictConfig['REFERENCELOGFILESFOLDER'] = REFERENCELOGFILESFOLDER

      # -- installed sources

      SITEPACKAGES = None
      if PLATFORMSYSTEM == "Windows":
          SITEPACKAGES = CString.NormalizePath(f"{PYTHONPATH}/Lib/site-packages")
      elif PLATFORMSYSTEM == "Linux":
          SITEPACKAGES = CString.NormalizePath(f"{PYTHONPATH}/../lib/python3.9/site-packages")
      else:
         bSuccess = None
         sResult  = f"Operating system {PLATFORMSYSTEM} ({OSNAME}) not supported"
         raise Exception(CString.FormatResult(sMethod, bSuccess, sResult))
      self.__dictConfig['SITEPACKAGES'] = SITEPACKAGES

      self.__dictConfig['CONFIGSCHEMAFILE'] = f"{SITEPACKAGES}/RobotFramework_TestsuitesManagement/Config/configuration_schema.json"

      # -- configuration: command line

      oCmdLineParser = argparse.ArgumentParser()
      oCmdLineParser.add_argument('--testid', type=str, help='The ID of the test to be executed')
      oCmdLineParser.add_argument('--silent', action='store_true', help='If True, parts of console output are suppressed; default: False')
      oCmdLineParser.add_argument('--codedump', action='store_true', help='If True, creates pytest code and test lists; default: False')
      oCmdLineParser.add_argument('--configdump', action='store_true', help='If True, basic configuration values are dumped to console; default: False')
      oCmdLineParser.add_argument('--skiplogcompare', action='store_true', help='If True, the log file comparison is skipped; default: False') # e.g. in case of reference log files are not yet existing

      oCmdLineArgs = oCmdLineParser.parse_args()

      TESTID = None
      if oCmdLineArgs.testid != None:
         TESTID = str(oCmdLineArgs.testid).strip()
      self.__dictConfig['TESTID'] = TESTID

      bSilent = False
      if oCmdLineArgs.silent != None:
         bSilent = oCmdLineArgs.silent
      self.__dictConfig['SILENT'] = bSilent

      bCodeDump = False
      if oCmdLineArgs.codedump != None:
         bCodeDump = oCmdLineArgs.codedump
      self.__dictConfig['CODEDUMP'] = bCodeDump
      # if True: script quits after config dump

      bConfigDump = False
      if oCmdLineArgs.configdump != None:
         bConfigDump = oCmdLineArgs.configdump
      self.__dictConfig['CONFIGDUMP'] = bConfigDump
      # if True: script quits after config dump

      LOGCOMPARE = True
      if oCmdLineArgs.skiplogcompare != None:
         bSkipLogCompare = oCmdLineArgs.skiplogcompare
         if bSkipLogCompare is True:
            LOGCOMPARE = False
         else:
            LOGCOMPARE = True
      self.__dictConfig['LOGCOMPARE'] = LOGCOMPARE

      # dump of basic configuration parameters to console
      self.DumpConfig()

   # eof def __init__(self, sCalledBy=None):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def DumpConfig(self):
      """Prints all configuration values to console."""
      # -- printing configuration to console
      print()
      # PrettyPrint(self.__dictConfig, sPrefix="Config")
      for key, value in self.__dictConfig.items():
         print(key.rjust(30, ' ') + " : " + str(value))
      print()
   # eof def DumpConfig(self):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def PrintConfigKeys(self):
      """Prints all configuration key names to console."""
      # -- printing configuration keys to console
      print()
      listKeys = self.__dictConfig.keys()
      sKeys = "[" + ", ".join(listKeys) + "]"
      print(sKeys)
      print()
   # eof def PrintConfigKeys(self):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def Get(self, sName=None):
      """Returns the configuration value belonging to a key name."""
      if ( (sName is None) or (sName not in self.__dictConfig) ):
         print()
         printerror(f"Configuration parameter '{sName}' not existing")
         # from here it's standard output:
         print()
         print("Use instead one of:")
         self.PrintConfigKeys()
         return None # returning 'None' in case of key is not existing !!!
      else:
         return self.__dictConfig[sName]
   # eof def Get(self, sName=None):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

# eof class CConfig():

# **************************************************************************************************************


