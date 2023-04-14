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
# CGenCode.py
#
# XC-CT/ECA3-Queckenstedt
#
# 30.03.2023
#
# --------------------------------------------------------------------------------------------------------------

"""
Python module containing the code generator
"""

# --------------------------------------------------------------------------------------------------------------

import os, sys, time
import colorama as col

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.File.CFile import CFile
from PythonExtensionsCollection.Folder.CFolder import CFolder
from PythonExtensionsCollection.Utils.CUtils import *

from libs.CCodePatterns import CCodePatterns

from testconfig.TestConfig import *

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

class CGenCode():
   """
   """

   def __init__(self, oConfig=None):
      """
      """

      sMethod = "CGenCode.__init__"

      if oConfig is None:
         raise Exception(CString.FormatResult(sMethod, None, "oConfig is None"))

      self.__oConfig = oConfig

      # -- initialize code patterns
      self.__oCodePatterns = None
      try:
          self.__oCodePatterns = CCodePatterns()
      except Exception as ex:
         raise Exception(CString.FormatResult(sMethod, None, str(ex)))

   # --------------------------------------------------------------------------------------------------------------

   def GenCode(self):
      """
      """

      sMethod = "GenCode"

      REFERENCEPATH = self.__oConfig.Get('REFERENCEPATH')

      # -- folder containing the generated pytest files

      PYTESTFILESFOLDER = f"{REFERENCEPATH}/pytest/pytestfiles"
      oFolder = CFolder(PYTESTFILESFOLDER)
      bSuccess, sResult = oFolder.Create(bOverwrite=True, bRecursive=True)
      del oFolder
      if bSuccess is not True:
         return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

      # -- copy additional pytest test libraries (that are not created automatically)
      sLibFolderSrc  = f"{REFERENCEPATH}/libs/pytestlibs"
      if not os.path.isdir(sLibFolderSrc):
         bSuccess = None
         sResult  = f"Missing pytest lib folder '{sLibFolderSrc}'"
         return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

      oFolder = CFolder(sLibFolderSrc)
      bSuccess, sResult = oFolder.CopyTo(PYTESTFILESFOLDER, bOverwrite=True)
      del oFolder
      if bSuccess is not True:
         return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

      # -- overview lists in RST, TXT and CSV format

      print(COLBY + f"Writing overview lists to '{REFERENCEPATH}'")
      print()

      PYTESTLISTFILE_RST = f"{REFERENCEPATH}/TSM_TestUsecases.rst"
      oPyTestListFile_RST = CFile(PYTESTLISTFILE_RST)
      print(f"* '{PYTESTLISTFILE_RST}'")

      PYTESTLISTFILE_TXT = f"{REFERENCEPATH}/TSM_TestUsecases.txt"
      oPyTestListFile_TXT = CFile(PYTESTLISTFILE_TXT)
      print(f"* '{PYTESTLISTFILE_TXT}'")

      PYTESTLISTFILE_CSV = f"{REFERENCEPATH}/TSM_TestUsecases.csv"
      oPyTestListFile_CSV = CFile(PYTESTLISTFILE_CSV)
      print(f"* '{PYTESTLISTFILE_CSV}'")

      PYTESTLISTFILE_HTML = f"{REFERENCEPATH}/TSM_TestUsecases.html"
      oPyTestListFile_HTML = CFile(PYTESTLISTFILE_HTML)
      print(f"* '{PYTESTLISTFILE_HTML}'")
      print()

      oPyTestListFile_RST.Write(self.__oCodePatterns.GetCopyRightRST(), 1)
      sHeadline = "Test Use Cases"
      sUnderline = len(sHeadline)*"="
      oPyTestListFile_RST.Write(sHeadline)
      oPyTestListFile_RST.Write(sUnderline, 1)

      oPyTestListFile_TXT.Write(120*"*")
      oPyTestListFile_TXT.Write(self.__oCodePatterns.GetCopyRightTXT())
      oPyTestListFile_TXT.Write(120*"-")
      oPyTestListFile_TXT.Write("Test Use Cases")
      oPyTestListFile_TXT.Write(120*"-")

      sSep = "|"
      oPyTestListFile_CSV.Write(f"sep={sSep}")
      oPyTestListFile_CSV.Write("TESTID|SECTION|SUBSECTION|DESCRIPTION")

      sOut = """<html><head>
<meta http-equiv="content-type" content="text/html; charset=windows-1252">
   <meta name="Testsuites Management" content="Testsuites Management">
   <title>Testsuites Management Test Overview</title>
</head>
<body vlink="#000000" text="#000000" link="#000000" bgcolor="#FFFFFF" alink="#000000">
<hr width="100%" color="#FF8C00" align="center">
<div align="center">
<font size="6" face="Arial" color="#595959">
<b>
RobotFramework_TestsuitesManagement<br>Test Cases
</b></font>
</div>
<hr width="100%" color="#FF8C00" align="center">

<div>&nbsp;</div>

<div align="center">

<table frame="box" rules="all" valign="middle" width="1100" cellspacing="0" cellpadding="6" border="1" align="center">
<colgroup>
   <col width="4%" span="1">
   <col width="8%" span="1">
   <col width="16%" span="1">
   <col width="9%" span="1">
   <col width="63%" span="1">
</colgroup>
<tbody>
"""
      oPyTestListFile_HTML.Write(sOut)

      nCntUsecases = 0
      for dictUsecase in listofdictUsecases:
         nCntUsecases = nCntUsecases + 1
         TESTID           = dictUsecase['TESTID']
         DESCRIPTION      = dictUsecase['DESCRIPTION']
         EXPECTATION      = dictUsecase['EXPECTATION']
         SECTION          = dictUsecase['SECTION']
         SUBSECTION       = dictUsecase['SUBSECTION']
         COMMENT          = dictUsecase['COMMENT']
         # optional ones
         HINT = None
         if "HINT" in dictUsecase:
            HINT = dictUsecase['HINT']

         oPyTestListFile_RST.Write(f"* **Test {TESTID}**", 1)
         oPyTestListFile_RST.Write(f"  [{SECTION} / {SUBSECTION}]", 1)
         oPyTestListFile_RST.Write(f"   **{DESCRIPTION}**", 1)
         oPyTestListFile_RST.Write(f"   Expected: {EXPECTATION}", 1)
         oPyTestListFile_RST.Write(f"   *Comment: {COMMENT}*", 1)
         if HINT is not None:
            oPyTestListFile_RST.Write(f"   *Hint: {HINT}*", 1)
         oPyTestListFile_RST.Write(f"----", 1)

         oPyTestListFile_TXT.Write(f"Test {TESTID} / {SECTION} / {SUBSECTION}")
         oPyTestListFile_TXT.Write(f"Description: {DESCRIPTION}")
         oPyTestListFile_TXT.Write(f"Expectation: {EXPECTATION}")
         oPyTestListFile_TXT.Write(f"Comment....: {COMMENT}")
         if HINT is not None:
            oPyTestListFile_TXT.Write(f"Hint.......: {HINT}")
         oPyTestListFile_TXT.Write(120*"-")

         oPyTestListFile_CSV.Write(f"{TESTID}|{SECTION}|{SUBSECTION}|{DESCRIPTION}")

         sOut = """<tr valign="middle" align="left">"""
         oPyTestListFile_HTML.Write(sOut)

         sHTMLPattern = """<td colspan="1" valign="center" bgcolor="#F5F5F5" align="right">
<font size="2" face="Arial" color="#FF0000">
<b>
####CNTUSECASES####
</b></font></td>

<td colspan="1" valign="center" bgcolor="#F5F5F5" align="middle">
<font size="2" face="Arial" color="#595959">
<b>
####TESTID####
</b></font></td>

<td colspan="1" valign="center" bgcolor="#F5F5F5" align="middle">
<font size="2" face="Arial" color="#4169E1">
####SECTION####
</font></td>

<td colspan="1" valign="center" bgcolor="#F5F5F5" align="middle">
<font size="2" face="Arial" color="#####TEXTCOLOR####">
####SUBSECTION####
</font></td>

<td colspan="1" valign="center" bgcolor="#F5F5F5" align="left">
<font size="2" face="Arial" color="#595959"><i>
####DESCRIPTION####<br>
Expected: ####EXPECTATION####<br>
Comment: ####COMMENT########HINT####
</i></font></td>

"""
         sOut = sHTMLPattern.replace('####CNTUSECASES####', str(nCntUsecases))
         sOut = sOut.replace('####TESTID####', TESTID)
         sOut = sOut.replace('####SECTION####', SECTION)
         sOut = sOut.replace('####SUBSECTION####', SUBSECTION)
         if SUBSECTION == "GOODCASE":
            TEXTCOLOR = "008000"
         else:
            TEXTCOLOR = "FF0000"
         sOut = sOut.replace('####TEXTCOLOR####', TEXTCOLOR)
         sOut = sOut.replace('####DESCRIPTION####', DESCRIPTION)
         sOut = sOut.replace('####EXPECTATION####', EXPECTATION)
         sOut = sOut.replace('####COMMENT####', COMMENT)
         if HINT is None:
            sOut = sOut.replace('####HINT####', "")
         else:
            sReplace = f"<br>\nHint: {HINT}"
            sOut = sOut.replace('####HINT####', sReplace)
         oPyTestListFile_HTML.Write(sOut)

         oPyTestListFile_HTML.Write("</tr>")

      # eof for dictUsecase in listofdictUsecases:

      sGenerated = "Generated: " + time.strftime('%d.%m.%Y - %H:%M:%S')
      oPyTestListFile_RST.Write(sGenerated, 1)
      oPyTestListFile_TXT.Write(sGenerated, 1)

      sEndOfFilePattern = """
</tbody></table></div>
<div>&nbsp;</div>
<hr width="100%" color="#FF8C00" align="center">
<div align="center"><font size="2" color="#27408B">####GENERATED####</font></div>
<div>&nbsp;</div>
</body></html>
"""
      sEndOfFile = sEndOfFilePattern.replace('####GENERATED####', sGenerated)
      oPyTestListFile_HTML.Write(sEndOfFile)

      del oPyTestListFile_RST
      del oPyTestListFile_TXT
      del oPyTestListFile_CSV
      del oPyTestListFile_HTML

      # --------------------------------------------------------------------------------------------------------------

      print(COLBY + f"Dumping pytest code to '{PYTESTFILESFOLDER}'")
      print()

      # -- use cases sorted by '{SECTION}_{SUBSECTION}'
      dictPyTestFiles = {}
      for dictUsecase in listofdictUsecases:
         SECTION    = dictUsecase['SECTION']
         SUBSECTION = dictUsecase['SUBSECTION']
         sKey = f"{SECTION}_{SUBSECTION}"
         if sKey not in dictPyTestFiles:
            dictPyTestFiles[sKey] = []
         listofdictUsecasesInFile = dictPyTestFiles[sKey]
         listofdictUsecasesInFile.append(dictUsecase)
         dictPyTestFiles[sKey] = listofdictUsecasesInFile
      # eof for dictUsecase in listofdictUsecases:

      # debug
      # PrettyPrint(dictPyTestFiles)

      nCntPyTestFiles = 0

      for sKey in dictPyTestFiles:
         nCntPyTestFiles = nCntPyTestFiles + 1
         sCnt = str(nCntPyTestFiles).rjust(2, "0")
         PYTESTFILENAME = f"test_{sCnt}_{sKey}.py"
         sPyTestFile = f"{PYTESTFILESFOLDER}/{PYTESTFILENAME}"
         print(f"* '{sPyTestFile}'")
         CLASSNAME = f"Test_{sKey}"
         oPyTestFile = CFile(sPyTestFile)
         oPyTestFile.Write(self.__oCodePatterns.GetPyTestFileHeader(PYTESTFILENAME, CLASSNAME))

         listofdictUsecasesInFile = dictPyTestFiles[sKey]
         for dictUsecase in listofdictUsecasesInFile:
            TESTID      = dictUsecase['TESTID']
            DESCRIPTION = dictUsecase['DESCRIPTION']
            EXPECTATION = dictUsecase['EXPECTATION']
            COMMENT     = dictUsecase['COMMENT']
            TESTNAME    = f"test_{TESTID}"
            oPyTestFile.Write(f"   # Expected: {EXPECTATION}")
            oPyTestFile.Write(f"   # ({COMMENT})")
            oPyTestFile.Write(self.__oCodePatterns.GetPyTestCase(DESCRIPTION, TESTNAME, TESTID))
            oPyTestFile.Write("# --------------------------------------------------------------------------------------------------------------")
         # eof for dictUsecase in listofdictUsecasesInFile:

         del oPyTestFile

      # eof for sKey in dictPyTestFiles:

      print()

      bSuccess = True
      sResult  = "Code and overview lists generated."

      return bSuccess, sResult

   # --------------------------------------------------------------------------------------------------------------

# eof class CGenCode():

# **************************************************************************************************************

