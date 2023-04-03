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
# CTextCheck.py
#
# XC-CT/ECA3-Queckenstedt
#
# 03.04.2023
#
# --------------------------------------------------------------------------------------------------------------

"""
Python module containing log file check functions
"""

# --------------------------------------------------------------------------------------------------------------

import os, sys, time
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

class CTextCheck():
   """
   """

   def __init__(self, oConfig=None):
      """
      """

      sMethod = "CTextCheck.__init__"

      if oConfig is None:
         raise Exception(CString.FormatResult(sMethod, None, "oConfig is None"))

      self.__oConfig = oConfig

   # --------------------------------------------------------------------------------------------------------------

   def TextCheck(self, sTextFile=None):
      """
      """

      sMethod = "TextCheck"

      if os.path.isfile(sTextFile) is False:
         bCheckResult = None
         bSuccess     = None
         sResult      = f"File not found: '{sTextFile}'"
         return bCheckResult, bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

      listNotPatterns = []
      NOTPATTERNFILE_TXT = self.__oConfig.Get('NOTPATTERNFILE_TXT')
      oNotPatternFile_TXT = CFile(NOTPATTERNFILE_TXT)
      listNotPatterns, bSuccess, sResult = oNotPatternFile_TXT.ReadLines()
      del oNotPatternFile_TXT
      if bSuccess is not True:
         bCheckResult = None
         return bCheckResult, bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

      listIgnorePatterns = []
      IGNOREPATTERNFILE_TXT = self.__oConfig.Get('IGNOREPATTERNFILE_TXT')
      oIgnorePatternFile_TXT = CFile(IGNOREPATTERNFILE_TXT)
      listIgnorePatterns, bSuccess, sResult = oIgnorePatternFile_TXT.ReadLines()
      del oIgnorePatternFile_TXT
      if bSuccess is not True:
         bCheckResult = None
         return bCheckResult, bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)
      sIgnorePatterns = None
      if listIgnorePatterns is not None:
         sIgnorePatterns = ";".join(listIgnorePatterns)

      # initial assumptions
      bCheckResult = None # None is to indicate that no check has been executed (because no pattern are defined)
      bSuccess     = True
      sResult      = "Done."

      if len(listNotPatterns) > 0:
         # check only makes sense in case of patterns are available
         oTextFile = CFile(sTextFile)
         listTextLines, bSuccess, sResult = oTextFile.ReadLines(bSkipBlankLines=True, sContainsNot=sIgnorePatterns)
         # Currently we assume that it is possible to read the entire log file. In case of the size of the log file
         # exceeds the computer ressources we have to introduce a 'read line by line' mechanism.
         del oTextFile
         if bSuccess is not True:
            bCheckResult = None
            return bCheckResult, bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)
         listForbiddenPositions = []
         for sTextLine in listTextLines:
            for sNotPattern in listNotPatterns:
               if sNotPattern in sTextLine:
                  if sTextLine not in listForbiddenPositions:
                     listForbiddenPositions.append(sTextLine)
         # eof for sTextLine in listTextLines:
         if len(listForbiddenPositions) > 0:
            # text check failed because of forbidden patterns found
            bCheckResult = False
            bSuccess     = True
            sForbiddenPatternFeedback = "\n".join(listForbiddenPositions)
            sResult      = f"Text check for forbidden patterns failed.\n\nFile: '{sTextFile}'\nForbidden pattern found in line:\n{sForbiddenPatternFeedback}"
         else:
            bCheckResult = True
            bSuccess     = True
            sResult      = "Text check passed"
      # eof if len(listNotPatterns) > 0:

      return bCheckResult, bSuccess, sResult

   # eof def TextCheck(self, sTextFile=None):

   # --------------------------------------------------------------------------------------------------------------

# eof class CTextCheck():

# **************************************************************************************************************
