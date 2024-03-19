# **************************************************************************************************************
#
#  Copyright 2020-2024 Robert Bosch GmbH
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
# GenSnippetsTSM.py
#
# XC-HWP/ESW3-Queckenstedt
#
# **************************************************************************************************************
#
VERSION      = "0.1.0"
VERSION_DATE = "18.03.2024"
#
# **************************************************************************************************************

# History

# **************************************************************************************************************
# TM***
#
# -- TOC
#[DEFCONFIG]
#[DEFCOUNTER]
#[DEFCLISTVALUES]
#[DEFLOGGER]
#[DEFEXECUTOR]
#[HTMLPATTERN]
#[CSNIPPETS]
#[INITCONFIG]
#[INITLOGGER]
#[INITCOUNTER]
#[INITJPP]
#[INITEXECUTOR]
#[STARTOFEXECUTION]
#[ENDOFEXECUTION]
#
# TM***
# **************************************************************************************************************


# -- import standard Python modules
import os, sys, shlex, subprocess, ctypes, time, platform, json, pprint, itertools
import colorama as col

# -- import own Python modules
from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Folder.CFolder import CFolder
from PythonExtensionsCollection.File.CFile import CFile
from PythonExtensionsCollection.Utils.CUtils import *

col.init(autoreset=True)

COLBR = col.Style.BRIGHT + col.Fore.RED
COLBY = col.Style.BRIGHT + col.Fore.YELLOW
COLBG = col.Style.BRIGHT + col.Fore.GREEN
COLBB = col.Style.BRIGHT + col.Fore.BLUE

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printfailure(sMsg, prefix=None):
   if prefix is None:
      sMsg = COLBR + f"{sMsg}!\n\n"
   else:
      sMsg = COLBR + f"{prefix}:\n{sMsg}!\n\n"
   sys.stderr.write(sMsg)


# --------------------------------------------------------------------------------------------------------------
#[DEFCONFIG]
# --------------------------------------------------------------------------------------------------------------
#TM***

class CConfig():

   def __init__(self, sCalledBy=None):

      sMethod = "CConfig.__init__"

      # -- configuration init
      self.__dictConfig = {}

      if sCalledBy is None:
         raise Exception(CString.FormatResult(sMethod, None, "sCalledBy is None"))

      THISAPP                                 = CString.NormalizePath(sCalledBy)
      self.__dictConfig['THISAPP']            = THISAPP
      self.__dictConfig['THISAPPNAME']        = os.path.basename(THISAPP)
      REFERENCEPATH                           = os.path.dirname(THISAPP) # position of main() app is reference for all relative paths
      self.__dictConfig['REFERENCEPATH']      = REFERENCEPATH
      self.__dictConfig['OUTPUTPATH']         = f"{REFERENCEPATH}" # /output
      self.__dictConfig['LOGFILE']            = f"{self.__dictConfig['OUTPUTPATH']}/GenSnippetLogTSM.log"
      self.__dictConfig['REPORTFILE']         = f"{self.__dictConfig['OUTPUTPATH']}/GenSnippetReportTSM.html"
      self.__dictConfig['TMPFILESPATH']       = f"{REFERENCEPATH}/tmp_files"
      self.__dictConfig['CONFIGPATH']         = f"{self.__dictConfig['TMPFILESPATH']}/config"
      self.__dictConfig['ROBOTTESTFILE']      = f"{self.__dictConfig['TMPFILESPATH']}/testfile.robot" # dynamically created
      self.__dictConfig['VARIANTSCONFIGFILE'] = f"{self.__dictConfig['CONFIGPATH']}/variants_config.json" # fix
      self.__dictConfig['TESTCONFIGFILE']     = f"{self.__dictConfig['CONFIGPATH']}/testconfig.json" # dynamically created
      self.__dictConfig['TESTLOGFILESFOLDER'] = f"{self.__dictConfig['TMPFILESPATH']}/logfiles"
      self.__dictConfig['TESTLOGFILENAME']    = "testlogfile_debug.log"
      OSNAME                                  = os.name
      self.__dictConfig['OSNAME']             = OSNAME
      self.__dictConfig['PLATFORMSYSTEM']     = platform.system()
      PYTHON                                  = CString.NormalizePath(sys.executable)
      self.__dictConfig['PYTHON']             = PYTHON
      self.__dictConfig['PYTHONPATH']         = os.path.dirname(PYTHON)
      self.__dictConfig['PYTHONVERSION']      = sys.version
      self.__dictConfig['NOW']                = time.strftime('%d.%m.%Y - %H:%M:%S')

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def __del__(self):
      del self.__dictConfig

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def DumpConfig(self):
      """Prints all configuration values to console."""
      listFormattedOutputLines = []
      # -- printing configuration to console
      print()
      # PrettyPrint(self.__dictConfig, sPrefix="Config")
      nJust = 32
      for key, value in self.__dictConfig.items():
         if isinstance(value, list):
            nCnt = 0
            for element in value:
               nCnt = nCnt + 1
               element_cnt = f"{key} ({nCnt})"
               sLine = element_cnt.rjust(nJust, ' ') + " : " + str(element)
               print(sLine)
               listFormattedOutputLines.append(sLine)
         else:
            sLine = key.rjust(nJust, ' ') + " : " + str(value)
            print(sLine)
            listFormattedOutputLines.append(sLine)
      print()
      return listFormattedOutputLines
   # eof def DumpConfig(self):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def Get(self, sName=None):
      """Returns the configuration value belonging to a key name."""
      if ( (sName is None) or (sName not in self.__dictConfig) ):
         print()
         printfailure(f"Configuration parameter '{sName}' not existing")
         return None # returning 'None' in case of key is not existing !!!
      else:
         return self.__dictConfig[sName]
   # eof def Get(self, sName=None):

   # --------------------------------------------------------------------------------------------------------------
   #TM***

   def Set(self, sName=None, sValue=None):
      """Sets a new configuration parameter."""
      sName = f"{sName}"
      self.__dictConfig[sName] = sValue
   # eof def Set(self, sName=None, sValue=None):

# eof class CConfig():


# --------------------------------------------------------------------------------------------------------------
#[DEFCOUNTER]
# --------------------------------------------------------------------------------------------------------------
#TM***

class CCounter():

   def __init__(self, nCntSection=0,nCntSubSection=0,nCntGlobal=0):
      self.__nCntSection    = nCntSection
      self.__nCntSubSection = nCntSubSection
      self.__nCntGlobal     = nCntGlobal

   def IncSection(self):
      self.__nCntSection = self.__nCntSection + 1
      self.__nCntSubSection = 0 # => 'IncSection' requires a separate 'IncSubSection'; advantage: 'IncSubSection' can run separately in loop
      return f"[ {self.__nCntSection}.{self.__nCntSubSection} ]"

   def IncSubSection(self):
      self.__nCntSubSection = self.__nCntSubSection + 1
      self.__nCntGlobal = self.__nCntGlobal + 1
      return f"( {self.__nCntGlobal} ) - [ {self.__nCntSection}.{self.__nCntSubSection} ]"

   def GetCntString(self):
      return f"( {self.__nCntGlobal} ) - [ {self.__nCntSection}.{self.__nCntSubSection} ]"

   def GetCntSection(self):
      return self.__nCntSection

   def GetCntClobal(self):
      return self.__nCntGlobal

# eof class CCounter():


# --------------------------------------------------------------------------------------------------------------
#[DEFCLISTVALUES]
# --------------------------------------------------------------------------------------------------------------
#TM***

class CListElements():

   def __init__(self, listElements=[]):
      self.listElements  = listElements
      self.nNrOfElements = len(self.listElements)
      self.nCurrentIndex = 0

   def GetElement(self):
      oElement = self.listElements[self.nCurrentIndex]
      self.nCurrentIndex = self.nCurrentIndex + 1
      if self.nCurrentIndex >= self.nNrOfElements:
         self.nCurrentIndex = 0
      return oElement

# eof class CListElements():


# --------------------------------------------------------------------------------------------------------------
#[DEFLOGGER]
# --------------------------------------------------------------------------------------------------------------
#TM***

class CLogger():

   def __init__(self, oConfig=None):

      sMethod = "CLogger.__init__"

      self.__oLogfile    = None
      self.__oReportfile = None
      self.__oConfig     = None

      if oConfig is None:
         raise Exception(CString.FormatResult(sMethod, None, "oConfig is None"))
      self.__oConfig = oConfig

      LOGFILE    = self.__oConfig.Get('LOGFILE')
      REPORTFILE = self.__oConfig.Get('REPORTFILE')

      self.__oLogfile    = CFile(LOGFILE)
      self.__oReportfile = CFile(REPORTFILE)

   def __del__(self):
      del self.__oConfig
      del self.__oLogfile
      del self.__oReportfile

   def WriteLog(self, content=None):
      if type(content) == list:
         for element in content:
            self.__oLogfile.Write(element)
      else:
         self.__oLogfile.Write(f"{content}")

   def WriteReport(self, content=None):
      if type(content) == list:
         for element in content:
            self.__oReportfile.Write(element)
      else:
         self.__oReportfile.Write(f"{content}")

# eof class CLogger(oConfig):


# --------------------------------------------------------------------------------------------------------------
#[DEFEXECUTOR]
# --------------------------------------------------------------------------------------------------------------
#TM***

class CExecutor():

   def __init__(self, oConfig=None, oCounter=None, oLogger=None):

      sMethod = "CExecutor.__init__"

      self.__oConfig      = None
      self.__oCounter     = None
      self.__oLogger      = None
      self.__oSnippets    = None
      self.__oHTMLPattern = None

      if oConfig is None:
         raise Exception(CString.FormatResult(sMethod, None, "oConfig is None"))
      self.__oConfig = oConfig

      if oCounter is None:
         raise Exception(CString.FormatResult(sMethod, None, "oCounter is None"))
      self.__oCounter = oCounter

      if oLogger is None:
         raise Exception(CString.FormatResult(sMethod, None, "oLogger is None"))
      self.__oLogger = oLogger

      # access to code snippets (required for HTML report file)
      self.__oSnippets = CSnippets()

      # access to HTML pattern (required for HTML report file)
      self.__oHTMLPattern = CHTMLPattern()

      # info indicators, used while parsing relevant content from Robot Framework debug log file and used to define the text color
      self.__listInfoIndicators = ["[TSM-SNIPPET-TEST]", "configuration level"]

      # error indicators, used while parsing relevant content from Robot Framework debug log file and used to define the text color
      self.__listErrorIndicators = ["ERROR", "Error", "error", "UNKNOWN", "unknown", "FAIL", "failed", "AssertionError",
                                    "Expecting", "expected", "Unexpected", "unexpected", "Invalid", "invalid", "Reason",
                                    "not found", "have to be", "does not support"]

      # filter strings, used while parsing relevant content from Robot Framework debug log file
      self.__sInfoIndicators  = ";".join(self.__listInfoIndicators)
      self.__sErrorIndicators = ";".join(self.__listErrorIndicators)
      self.__sFilterStrings   = f"{self.__sInfoIndicators};{self.__sErrorIndicators}"

   #eof def __init__(self, oConfig=None, oCounter=None, oLogger=None):


   def __del__(self):
      del self.__oConfig
      del self.__oCounter
      del self.__oLogger
      del self.__oSnippets
      del self.__oHTMLPattern

   # --------------------------------------------------------------------------------------------------------------

   def GenInfrastructure(self):

      sMethod = "GenInfrastructure"

      bSuccess = None
      sResult  = "UNKNOWN"

      TMPFILESPATH       = self.__oConfig.Get('TMPFILESPATH')
      CONFIGPATH         = self.__oConfig.Get('CONFIGPATH')
      VARIANTSCONFIGFILE = self.__oConfig.Get('VARIANTSCONFIGFILE')

      oTmpFilesPath = CFolder(TMPFILESPATH)
      bSuccess, sResult = oTmpFilesPath.Create(bOverwrite=False, bRecursive=True)
      del oTmpFilesPath
      if bSuccess is not True:
         return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

      oConfigPath = CFolder(CONFIGPATH)
      bSuccess, sResult = oConfigPath.Create(bOverwrite=False, bRecursive=True)
      del oConfigPath
      if bSuccess is not True:
         return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

      # this is a fix pattern:
      sTestConfigContent = """{
  "default": {
    "name": "testconfig.json",
    "path": ".../config/"
  }
}
"""
      oVariantsConfigFile = CFile(VARIANTSCONFIGFILE)
      bSuccess, sResult = oVariantsConfigFile.Write(sTestConfigContent)
      del oVariantsConfigFile
      if bSuccess is not True:
         return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

      bSuccess = True
      sResult  = "Infrastructure created"

      return bSuccess, sResult

   # eof def GenInfrastructure(self):

   # --------------------------------------------------------------------------------------------------------------

   def Execute(self, sHeadline=None, listoftuplesCodeSnippets=None, sType="TSM"):

      sMethod = "Execute"

      bSuccess = None
      sResult  = "UNKNOWN"

      if sHeadline is None:
         bSuccess = None
         sResult  = "sHeadline is None"
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      if listoftuplesCodeSnippets is None:
         bSuccess = None
         sResult  = "listoftuplesCodeSnippets is None"
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      if len(listoftuplesCodeSnippets) == 0:
         bSuccess = None
         sResult  = "List of code snippets is empty"
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      tupleSupportedTypes = ("TSM")
      if sType not in tupleSupportedTypes:
         bSuccess = None
         sResult  = f"Unexpected application type '{sType}'. Expected is one of '{tupleSupportedTypes}'"
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      if sType == "TSM":
         bSuccess, sResult = self.__ExecuteTSMSnippets(sHeadline, listoftuplesCodeSnippets)
         if bSuccess is not True:
            sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
      else:
         bSuccess = False
         sResult  = f"Types other than 'TSM' are currently not supported"
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)

      return bSuccess, sResult

   # eof def Execute(self, listoftuplesCodeSnippets=None, sType="TSM"):

   # --------------------------------------------------------------------------------------------------------------

   def __ExecuteTSMSnippets(self, sHeadline="UNKNOWN", listoftuplesCodeSnippets=[]):

      sMethod = "__ExecuteTSMSnippets"

      bSuccess = None
      sResult  = "UNKNOWN"

      # increment section counter and write headline to log file and to report file
      self.__oCounter.IncSection()
      nSectionNumber = self.__oCounter.GetCntSection()
      print(COLBY + f"{nSectionNumber}. {sHeadline}\n")
      self.__oLogger.WriteLog(120*"-")
      self.__oLogger.WriteLog(f"{nSectionNumber}. {sHeadline}")
      self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLHeadline1(f"{nSectionNumber}. {sHeadline}"))
      self.__oLogger.WriteLog(120*"-" + "\n")
      self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLHLine())

      for tupleCodeSnippets in listoftuplesCodeSnippets:

         # -- prepare files

         TESTCONFIGFILE      = self.__oConfig.Get('TESTCONFIGFILE')
         oTestConfigFile     = CFile(TESTCONFIGFILE)
         sTestConfigFileCode = tupleCodeSnippets[0]
         bSuccess, sResult   = oTestConfigFile.Write(sTestConfigFileCode)
         del oTestConfigFile
         if bSuccess is not True:
            print()
            printfailure(sResult)
            self.__oLogger.WriteLog(sResult)
            self.__oLogger.WriteLog("")
            self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLException(self.__oHTMLPattern.Txt2HTML(sResult)))
            self.__oLogger.WriteReport("<br/>")
            print()
            bSuccess = None
            return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

         ROBOTTESTFILE      = self.__oConfig.Get('ROBOTTESTFILE')
         oRobotTestFile     = CFile(ROBOTTESTFILE)
         sRobotTestFileCode = tupleCodeSnippets[1]
         bSuccess, sResult  = oRobotTestFile.Write(sRobotTestFileCode)
         del oRobotTestFile
         if bSuccess is not True:
            print()
            printfailure(sResult)
            self.__oLogger.WriteLog(sResult)
            self.__oLogger.WriteLog("")
            self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLException(self.__oHTMLPattern.Txt2HTML(sResult)))
            self.__oLogger.WriteReport("<br/>")
            print()
            bSuccess = None
            return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

         # we only write the JSON code under test to screen and to logfiles, and not the entire sTestConfigFileCode
         # (this would be too much redundancy)
         sParamsGlobalDefinitions = tupleCodeSnippets[2]
         # remove leading and trailing blank lines
         listParamsGlobalDefinitions = sParamsGlobalDefinitions.splitlines()
         listParamsGlobalDefinitionsReduced = []
         for sParamsGlobalDefinition in listParamsGlobalDefinitions:
            sParamsGlobalDefinition = sParamsGlobalDefinition.rstrip()
            if sParamsGlobalDefinition != "":
               listParamsGlobalDefinitionsReduced.append(sParamsGlobalDefinition)
         sParamsGlobalDefinitions = "\n".join(listParamsGlobalDefinitionsReduced)
         del listParamsGlobalDefinitions
         del listParamsGlobalDefinitionsReduced

         # for every code snippet increment subsection counter and write current counter string to log file and to report file
         self.__oCounter.IncSubSection()
         print(COLBY + self.__oCounter.GetCntString() + "\n")
         self.__oLogger.WriteLog(self.__oCounter.GetCntString() + "\n")
         self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLCounter(self.__oCounter.GetCntString()))
         # write code snippet to log file and to report file
         print(COLBB + sParamsGlobalDefinitions + "\n")
         self.__oLogger.WriteLog(sParamsGlobalDefinitions)
         self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLSnippetCode(self.__oHTMLPattern.Txt2HTML(sParamsGlobalDefinitions)))
         self.__oLogger.WriteReport("<br/>")

         # --------------------------------------------------------------------------------------------------------------

         # -- prepare Robot Framework command line

         PYTHON             = self.__oConfig.Get('PYTHON')
         TESTLOGFILESFOLDER = self.__oConfig.Get('TESTLOGFILESFOLDER')
         TESTLOGFILENAME    = self.__oConfig.Get('TESTLOGFILENAME')
         ROBOTTESTFILE      = self.__oConfig.Get('ROBOTTESTFILE')

         listCmdLineParts = []
         listCmdLineParts.append(f"\"{PYTHON}\"")
         listCmdLineParts.append("-m robot")
         # currently not used # listCmdLineParts.append("--loglevel USER")
         listCmdLineParts.append("-d")
         listCmdLineParts.append(f"\"{TESTLOGFILESFOLDER}\"")
         # currently not used # listCmdLineParts.append("-o")
         # currently not used # listCmdLineParts.append(f"\"testlogfile.xml\"")
         # currently not used # listCmdLineParts.append("-l")
         # currently not used # listCmdLineParts.append(f"\"testlogfile_log.html\"")
         # currently not used # listCmdLineParts.append("-r")
         # currently not used # listCmdLineParts.append(f"\"testlogfile_report.html\"")
         listCmdLineParts.append("-b")
         TESTLOGFILENAME = self.__oCounter.GetCntString() + f" - {TESTLOGFILENAME}"
         listCmdLineParts.append(f"\"{TESTLOGFILENAME}\"")
         listCmdLineParts.append(f"\"{ROBOTTESTFILE}\"")
         self.__oConfig.Set('TESTLOGFILE', f"{TESTLOGFILESFOLDER}/{TESTLOGFILENAME}")

         # -- execution of autogenerated test code

         sCmdLine = " ".join(listCmdLineParts)
         del listCmdLineParts
         print(f"Now executing command line:\n{sCmdLine}")
         listCmdLineParts = shlex.split(sCmdLine)
         nReturn = ERROR
         try:
            nReturn = subprocess.call(listCmdLineParts)
            sResult = f"Robot Framework returned {nReturn}"
            print()
            if nReturn == 0:
               print(COLBG + sResult + "\n")
            else:
               print(COLBR + sResult + "\n")
            self.__oLogger.WriteLog("")
            self.__oLogger.WriteLog(sResult)
            self.__oLogger.WriteLog("")
            if nReturn == 0:
               self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLValuesReturned(self.__oHTMLPattern.Txt2HTML(sResult)))
            else:
               self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLException(self.__oHTMLPattern.Txt2HTML(sResult)))
            self.__oLogger.WriteReport("<br/>")
         except Exception as ex:
            sException=str(ex)
            print()
            printfailure(sException)
            self.__oLogger.WriteLog(sException)
            self.__oLogger.WriteLog("")
            self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLException(self.__oHTMLPattern.Txt2HTML(sException)))
            self.__oLogger.WriteReport("<br/>")
            print()

         # -- get relevant content from debug log file

         TESTLOGFILE = self.__oConfig.Get('TESTLOGFILE')
         if not os.path.isfile(TESTLOGFILE):
            sResult  = f"Missing test log file '{TESTLOGFILE}'"
            print()
            printfailure(sResult)
            self.__oLogger.WriteLog(sResult)
            self.__oLogger.WriteLog("")
            self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLException(self.__oHTMLPattern.Txt2HTML(sResult)))
            self.__oLogger.WriteReport("<br/>")
            print()
            bSuccess = None
            return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

         oTestLogFile = CFile(TESTLOGFILE)
         listLogLines, bSuccess, sResult = oTestLogFile.ReadLines(bSkipBlankLines=True,
                                                                  sContains=self.__sFilterStrings,
                                                                  sContainsNot="START KEYWORD;END KEYWORD",
                                                                  bLStrip=True,
                                                                  bRStrip=True,
                                                                  bToScreen=False)
         del oTestLogFile
         if bSuccess is not True:
            # print()
            printfailure(sResult)
            self.__oLogger.WriteLog(sResult)
            self.__oLogger.WriteLog("")
            self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLException(self.__oHTMLPattern.Txt2HTML(sResult)))
            self.__oLogger.WriteReport("<br/>")
            print()
            bSuccess = None
            return bSuccess, CString.FormatResult(sMethod, bSuccess, sResult)

         # remove timestamp and blank lines (mostly leading and trailing blank lines)
         listLogLinesReduced = []
         for sLogLine in listLogLines:
            sLogLine = sLogLine.strip()
            if sLogLine != "":
               if sLogLine[0:5].isdigit() is True:
                  sLogLine = sLogLine[24:]
               listLogLinesReduced.append(sLogLine)

         for sLogLine in listLogLinesReduced:
            bError = False
            for sErrorIndicator in self.__listErrorIndicators:
               if sErrorIndicator in sLogLine:
                  bError = True
                  print(COLBR + sLogLine)
                  break
            if bError is False:
               print(COLBG + sLogLine)
         # eof for sLogLine in listLogLinesReduced:
         print()

         self.__oLogger.WriteLog(listLogLinesReduced)
         self.__oLogger.WriteLog("")

         for sLogLine in listLogLinesReduced:
            bError = False
            for sErrorIndicator in self.__listErrorIndicators:
               if sErrorIndicator in sLogLine:
                  bError = True
                  self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLException(self.__oHTMLPattern.Txt2HTML(sLogLine)))
                  break
            if bError is False:
               self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLValuesReturned(self.__oHTMLPattern.Txt2HTML(sLogLine)))
         # eof for sLogLine in listLogLinesReduced:

         self.__oLogger.WriteReport("<br/>")

         self.__oLogger.WriteLog(120*"-" + "\n")
         self.__oLogger.WriteReport(self.__oHTMLPattern.GetHTMLHLine())

         del listLogLines
         del listLogLinesReduced

      # eof for tupleCodeSnippets in listoftuplesCodeSnippets:

      bSuccess = True
      sResult  = "done"

      return bSuccess, sResult

   # eof def __ExecuteTSMSnippets(self, sHeadline="UNKNOWN", listoftuplesCodeSnippets=[]):

   # --------------------------------------------------------------------------------------------------------------

# eof class CExecutor():


# --------------------------------------------------------------------------------------------------------------
#[HTMLPATTERN]
# --------------------------------------------------------------------------------------------------------------
#TM***

class CHTMLPattern():

   sHTMLHeader = """
<html>
<head>
   <meta name="Code Snippets" content="Release">
   <title>Code Snippets</title>
</head>
<body bgcolor="#FFFFFF" text="#000000" link="#0000FF" vlink="#0000FF" alink="#0000FF">

   <hr width="100%" align="center" color="#d0d0d0"/>
"""

   sHTMLFooter = """
   <div align="center"><font size="2" color="#27408B">###NOW###</font></div>
</body>
</html>
"""

   sHTMLHLine = """
<hr width="100%" align="center" color="#d0d0d0"/>
"""

   sHTMLHeadline1 = """
<h1>###HTMLHEADLINE1###</h1>
"""

   sHTMLHeadline2 = """
<h2>###HTMLHEADLINE2###</h2>
"""

   sHTMLText = """
<p><font face="Arial" color="black" size="-1">###HTMLTEXT###</font></p>
"""

   sHTMLCounter = """
<p><font face="Arial" color="black" size="-1">###HTMLCOUNTER###</font></p>
"""

   sHTMLSnippetCode = """
<code><font font-family="courier new" color="mediumblue" size="">###HTMLSNIPPETCODE###</font></code><br/>
"""

   sHTMLValuesReturned = """
<code><font font-family="courier new" color="green" size="">###HTMLVALUESRETURNED###</font></code><br/>
"""

   sHTMLException = """
<font face="Arial" color="red" size="-1">###HTMLEXCEPTION###</font><br/>
"""


   def Txt2HTML(self, sText=None):
      listHTML = sText.splitlines()
      listLinesHTMLindent = []
      for sLine in listHTML:
         sLine = sLine.rstrip() # remove unnecessary trailing blanks
         sLine = sLine.replace("<", "&lt;")   # replace HTML special characters
         sLine = sLine.replace(">", "&gt;")   # replace HTML special characters
         sLine = sLine.replace(" ", "&nbsp;") # replace spaces by non breaking HTML spaces
         listLinesHTMLindent.append(sLine)
      # eof for sLine in listHTML:
      sHTML = "</br>\n".join(listLinesHTMLindent)
      return sHTML

   def GetHTMLHeader(self):
      return CHTMLPattern.sHTMLHeader

   def GetHTMLFooter(self, NOW=None):
      sHTML = CHTMLPattern.sHTMLFooter.replace("###NOW###", f"{NOW}")
      return sHTML

   def GetHTMLHLine(self):
      return CHTMLPattern.sHTMLHLine

   def GetHTMLHeadline1(self, sHTML=None):
      sHTML = CHTMLPattern.sHTMLHeadline1.replace("###HTMLHEADLINE1###", f"{sHTML}")
      return sHTML

   def GetHTMLHeadline2(self, sHTML=None):
      sHTML = CHTMLPattern.sHTMLHeadline2.replace("###HTMLHEADLINE2###", f"{sHTML}")
      return sHTML

   def GetHTMLText(self, sHTML=None):
      sHTML = CHTMLPattern.sHTMLText.replace("###HTMLTEXT###", f"{sHTML}")
      return sHTML

   def GetHTMLCounter(self, sHTML=None):
      sHTML = CHTMLPattern.sHTMLCounter.replace("###HTMLCOUNTER###", f"{sHTML}")
      return sHTML

   def GetHTMLSnippetCode(self, sHTML=None):
      sHTML = CHTMLPattern.sHTMLSnippetCode.replace("###HTMLSNIPPETCODE###", f"{sHTML}")
      return sHTML

   def GetHTMLValuesReturned(self, sHTML=None):
      sHTML = CHTMLPattern.sHTMLValuesReturned.replace("###HTMLVALUESRETURNED###", f"{sHTML}")
      return sHTML

   def GetHTMLException(self, sHTML=None):
      sHTML = CHTMLPattern.sHTMLException.replace("###HTMLEXCEPTION###", f"{sHTML}")
      return sHTML

# eof class CHTMLPattern():


# --------------------------------------------------------------------------------------------------------------
#[CSNIPPETS]
# --------------------------------------------------------------------------------------------------------------
#TM***

class CSnippets():

   def __GetTestConfigFileCode(self, sParamsGlobalDefinitions=None):
      """Returns a test config file code in JSONP format
      """

      sTestConfigFilePattern = """{
  "WelcomeString": "Hello... TSM self test is running now!",

  "Maximum_version" : "1.0.0",
  "Minimum_version" : "0.6.0",

  "Project"    : "test",
  "TargetName" : "test",

  "params" : {
              "global": {
####PARAMSGLOBALDEFINITIONS####
                        }
             }
}
"""
      sTestConfigFileCode = sTestConfigFilePattern.replace("####PARAMSGLOBALDEFINITIONS####", f"{sParamsGlobalDefinitions}")
      return sTestConfigFileCode

   # --------------------------------------------------------------------------------------------------------------

   def __GetRobotTestFileCode(self, sRobotTestCode=None):
      """Returns a robot test file code
      """

      sRobotTestFilePattern = """*** Settings ***

Library    Collections
Library    BuiltIn
Library    RobotFramework_TestsuitesManagement    WITH NAME    tm
Library    RobotframeworkExtensions.Collection    WITH NAME    rf.extensions

Suite Setup    tm.testsuite_setup    ./config/variants_config.json

Documentation    TSM code snippet test suite

*** Test Cases ***

TSM Code Snippet Test

####ROBOTTESTCODE####
"""

      sRobotTestFileCode = sRobotTestFilePattern.replace("####ROBOTTESTCODE####", f"{sRobotTestCode}")
      return sRobotTestFileCode

   # --------------------------------------------------------------------------------------------------------------

   def GetSeveralParticularSnippets(self):
      """Several particular snippets covering different topics
      """

      # '[TSM-SNIPPET-TEST]' is a constant log line identifier!

      sHeadline = "Several particular snippets covering different topics"

      listoftuplesCodeSnippets = []

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"testparam_1" : "value_1",
"testparam_2" : {"A" : 1},
"testparam_3" : ["A","B","C"]
"""
      sRobotTestCode = """
    rf.extensions.pretty_print    ${testparam_1}    [TSM-SNIPPET-TEST] {testparam_1}
    rf.extensions.pretty_print    ${testparam_2}    [TSM-SNIPPET-TEST] {testparam_2}
    rf.extensions.pretty_print    ${testparam_3}    [TSM-SNIPPET-TEST] {testparam_3}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
${testdict1.subKey1.subKey2.subKey3} : {"subKey4" : 1},
${testdict2.subKey1.subKey2} : {"subKey3" : {"subKey4" : 2}},
${testdict3.subKey1} : {"subKey2" : {"subKey3" : {"subKey4" : 3}}},
${testdict4} : {"subKey1" : {"subKey2" : {"subKey3" : {"subKey4" : 4}}}}
"""
      sRobotTestCode = """
    rf.extensions.pretty_print    ${testdict1}    [TSM-SNIPPET-TEST] {testdict1}
    rf.extensions.pretty_print    ${testdict2}    [TSM-SNIPPET-TEST] {testdict2}
    rf.extensions.pretty_print    ${testdict3}    [TSM-SNIPPET-TEST] {testdict3}
    rf.extensions.pretty_print    ${testdict4}    [TSM-SNIPPET-TEST] {testdict4}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"par${...}am2" : "123"
"""
      sRobotTestCode = """
    rf.extensions.pretty_print    output not expected    [TSM-SNIPPET-TEST]
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
I_AM_SYNTAX_ERROR }}}:{{{
"""
      sRobotTestCode = """
    rf.extensions.pretty_print    output not expected    [TSM-SNIPPET-TEST]
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"teststring_data_integrity" : "a.1,b.2;c.3,d.4  ;  e.5  ,  f.6"
"""
      sRobotTestCode = """
    rf.extensions.pretty_print    ${teststring_data_integrity}    [TSM-SNIPPET-TEST] {teststring_data_integrity}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"dTestDict" : {"ddKeyA" : "ddKeyA_value", "ddKeyB" : "ddKeyB_value"},
${params}['global']['dTestDict']['ddKeyA'] : {"ddKeyA_2" : "ddKeyA_2_value"},
//
"ddKeyA_2_param_1" : ${params.global.dTestDict.ddKeyA.ddKeyA_2},
"ddKeyA_2_param_2" : ${params.global.dTestDict.ddKeyA}['ddKeyA_2'],
"ddKeyA_2_param_3" : ${params.global.dTestDict}['ddKeyA']['ddKeyA_2'],
"ddKeyA_2_param_4" : ${params.global}['dTestDict']['ddKeyA']['ddKeyA_2'],
//
${params}['global']['dTestDict']['ddKeyB'] : {"ddKeyB_2" : "ddKeyB_2_value"},
//
"ddKeyB_2_param_1" : ${params.global.dTestDict.ddKeyB.ddKeyB_2},
"ddKeyB_2_param_2" : ${params.global.dTestDict.ddKeyB}['ddKeyB_2'],
"ddKeyB_2_param_3" : ${params.global.dTestDict}['ddKeyB']['ddKeyB_2'],
"ddKeyB_2_param_4" : ${params.global}['dTestDict']['ddKeyB']['ddKeyB_2'],
//
${params}['global']['dTestDict']['ddKeyC'] : {"ddKeyC_2" : {"ddKeyC_3" : "ddKeyC_3_value"}}
"""
      sRobotTestCode = """
    rf.extensions.pretty_print    ${dTestDict}    [TSM-SNIPPET-TEST] {dTestDict}

    rf.extensions.pretty_print    ${ddKeyA_2_param_1}    [TSM-SNIPPET-TEST] {ddKeyA_2_param_1}
    rf.extensions.pretty_print    ${ddKeyA_2_param_2}    [TSM-SNIPPET-TEST] {ddKeyA_2_param_2}
    rf.extensions.pretty_print    ${ddKeyA_2_param_3}    [TSM-SNIPPET-TEST] {ddKeyA_2_param_3}
    rf.extensions.pretty_print    ${ddKeyA_2_param_4}    [TSM-SNIPPET-TEST] {ddKeyA_2_param_4}

    rf.extensions.pretty_print    ${ddKeyB_2_param_1}    [TSM-SNIPPET-TEST] {ddKeyB_2_param_1}
    rf.extensions.pretty_print    ${ddKeyB_2_param_2}    [TSM-SNIPPET-TEST] {ddKeyB_2_param_2}
    rf.extensions.pretty_print    ${ddKeyB_2_param_3}    [TSM-SNIPPET-TEST] {ddKeyB_2_param_3}
    rf.extensions.pretty_print    ${ddKeyB_2_param_4}    [TSM-SNIPPET-TEST] {ddKeyB_2_param_4}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"Hint" : "Robot code contains keyword 'Fail'"
"""
      sRobotTestCode = """
    Fail
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"Hint" : "Robot code contains keyword 'Unknown'"
"""
      sRobotTestCode = """
    Unknown
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"dTestDict" : {"kVal_1" : "Val_1"},
${params}['global']['dTestDict']['kVal_2']['I_am_not_existing_1']['I_am_not_existing_2'] : ${params}['global']['dTestDict']['kVal_1'],
//
// use what has been created implicitly before
${params.global.dTestDict.kVal_3.I_am_not_existing_3.I_am_not_existing_4}    : ${params}['global']['dTestDict']['kVal_2']['I_am_not_existing_1']['I_am_not_existing_2'],
${params.global.dTestDict.kVal_3b.I_am_not_existing_3b.I_am_not_existing_4b} : ${params.global.dTestDict.kVal_2.I_am_not_existing_1.I_am_not_existing_2},
//
// overwrite what has been created implicitly before:
${params}['global']['dTestDict']['kVal_3']['I_am_not_existing_3']['I_am_not_existing_4'] : "${params}['global']['dTestDict']['kVal_1']_extended",
//
// use inside quotes the expression belonging to the data structure that has been created implicitly before:
"${params.global.dTestDict.kVal_3.I_am_not_existing_3.I_am_not_existing_4}" : "${params.global.dTestDict}['kVal_2']['I_am_not_existing_1']['I_am_not_existing_2']",
//
// mixture of dotdict and standard notation:
${params.global.dTestDict.kVal_4}['kVal_4B']['kVal_4C'] : {"A" : 1, "B" : [1,2]},
${params.global.dTestDict.kVal_4.kVal_4B.kVal_4C.kVal_4D.kVal_4E}['kVal_4F']['kVal_4G'] : {"C" : 2, "D" : [3,4]}
"""
      sRobotTestCode = """
    rf.extensions.pretty_print    ${dTestDict}    [TSM-SNIPPET-TEST] {dTestDict}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"teststring" : "eins",
${params.global.teststring} : "${params.global.teststring}.zwei"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${teststring}    [TSM-SNIPPET-TEST] {teststring}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"testdict" : {"A" : 1},
"name" : "C",
${params.global.testdict.${params.global.name}}['${params.global.name}'] : 5
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${testdict}    [TSM-SNIPPET-TEST] {testdict}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"teststring-1"  : "teststring-1 value",
${params.global.teststring-1} : "${params.global.teststring-1} extended"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${teststring-1}    [TSM-SNIPPET-TEST] {teststring-1}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"teststring*1"  : "teststring*1 value",
${params.global.teststring*1} : "${params.global.teststring*1} extended"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${teststring*1}    [TSM-SNIPPET-TEST] {teststring*1}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"teststring/1"  : "teststring/1 value",
${params.global.teststring/1} : "${params.global.teststring/1} extended"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${teststring/1}    [TSM-SNIPPET-TEST] {teststring/1}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
${params.global.level_1.level_2.level_3.level_4} : "levelvalue"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${level_1}    [TSM-SNIPPET-TEST] {level_1}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
// some parameters with subkey name values
"param1" : "subKey1",
"param2" : "subKey2",
"param3" : "subKey3",
"param4" : "subKey4",
//
// implicitly created dictionary
${testdict1.subKey1.subKey2.subKey3.subKey4} : 1,
//
// several ways to access subKey4 at left hand side of the colon
${testdict1}[${param1}]['${param2}']['subKey3'][${param4}] : 2,
${testdict1.${param1}.subKey2.${param3}.subKey4} : 3,
//
// the same on the right hand side of the colon
"param5" : ${testdict1}[${param1}]['${param2}']['subKey3'][${param4}],
"param6" : ${testdict1.${param1}.subKey2.${param3}.subKey4},
"param7" : "${testdict1.${param1}.subKey2.${param3}.subKey4}"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${testdict1}    [TSM-SNIPPET-TEST] {testdict1}
    rf.extensions.pretty_print    ${param1}    [TSM-SNIPPET-TEST] {param1}
    rf.extensions.pretty_print    ${param2}    [TSM-SNIPPET-TEST] {param2}
    rf.extensions.pretty_print    ${param3}    [TSM-SNIPPET-TEST] {param3}
    rf.extensions.pretty_print    ${param4}    [TSM-SNIPPET-TEST] {param4}
    rf.extensions.pretty_print    ${param5}    [TSM-SNIPPET-TEST] {param5}
    rf.extensions.pretty_print    ${param6}    [TSM-SNIPPET-TEST] {param6}
    rf.extensions.pretty_print    ${param7}    [TSM-SNIPPET-TEST] {param7}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param1" : "value",
"param2" : ${params.global.param1}[-1]
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param2}    [TSM-SNIPPET-TEST] {param2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param1" : "value",
"param2" : "${params.global.param1}[-1]"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param2}    [TSM-SNIPPET-TEST] {param2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"testlist" : [1,2,3],
"param2"   : ${params.global.testlist}[-1]
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param2}    [TSM-SNIPPET-TEST] {param2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"testlist" : [1,2,3],
"param2"   : "${params.global.testlist}[-1]"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param2}    [TSM-SNIPPET-TEST] {param2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"testdict" : {"A" : "B"},
"param2"   : ${params.global.testdict}[-1]
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param2}    [TSM-SNIPPET-TEST] {param2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"testdict" : {"A" : "B"},
"param2"   : "${params.global.testdict}[-1]"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param2}    [TSM-SNIPPET-TEST] {param2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"${IAMNOTEXISTING.${dictparam}}['${listparam}']" : 3
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    output not expected    [TSM-SNIPPET-TEST]
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"dict_param" : {"A" : 1 , "B" : 2}
"list_param" : ["A", "B", "C"]
"val2"       : "${params.global.list_param[1]}"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${val2}    [TSM-SNIPPET-TEST] {val2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"dict_param" : {"A" : 1 , "B" : 2},
"list_param" : ["A", "B", "C"],
"val3"       : "${params.global.list_param[${params.global.dict_param}['A']]}"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${val3}    [TSM-SNIPPET-TEST] {val3}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"dict_param" : {"A" : 1 , "B" : 2},
"list_param" : ["A", "B", "C"],
"val4"       : "${params.global.list_param[${params.global.dict_param}[${params.global.list_param}[0]]]}"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${val4}    [TSM-SNIPPET-TEST] {val4}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"dict_param" : {"A" : 1 , "B" : 2},
"list_param" : ["A", "B", "C"],
"val5"       : "${params.global.list_param[${params.global.dict_param}['${params.global.list_param}[0]']]}"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${val5}    [TSM-SNIPPET-TEST] {val5}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"intval"   : 1,
"testlist" : ["B", 2],
"param_${params.global.testlist}['${params.global.intval}']}" : 3
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    output not expected    [TSM-SNIPPET-TEST]
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"intval"   : 1,
"testlist" : ["B", 2],
${params.global.testlist}[${params.global.intval}] : 4
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${testlist}    [TSM-SNIPPET-TEST] {testlist}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"intval" : 1,
"testlist" : ["B", 2],
${params.global.testlist}['${params.global.intval}'] : 4
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${testlist}    [TSM-SNIPPET-TEST] {testlist}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param1" : True,
"param2" : False,
"param3" : None,
"param4" : ${True},
"param5" : ${False},
"param6" : ${None}
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param1}    [TSM-SNIPPET-TEST] {param1}
    rf.extensions.pretty_print    ${param2}    [TSM-SNIPPET-TEST] {param2}
    rf.extensions.pretty_print    ${param3}    [TSM-SNIPPET-TEST] {param3}
    rf.extensions.pretty_print    ${param4}    [TSM-SNIPPET-TEST] {param4}
    rf.extensions.pretty_print    ${param5}    [TSM-SNIPPET-TEST] {param5}
    rf.extensions.pretty_print    ${param6}    [TSM-SNIPPET-TEST] {param6}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param7" : {"A" : ${True}, "B" : 2},
"param8" : {C" : ${True}, "D" : [${False}, 3],
"param9" : {"E" : ${True}, "F" : [${False}, {"G" : ${None}}]}
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param7}    [TSM-SNIPPET-TEST] {param7}
    rf.extensions.pretty_print    ${param8}    [TSM-SNIPPET-TEST] {param8}
    rf.extensions.pretty_print    ${param9}    [TSM-SNIPPET-TEST] {param9}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"testdict1" : {"subKey1" : {"subKey2" : {"subKey3" : {"subKey4" : 0}}}},
${params.global.testdict1.subKey1} : {"subKey2" : {"subKey3" : {"subKey4" : 1}}},
${params.global.testdict1.subKey1.subKey2} : {"subKey3" : {"subKey4" : 2}},
${params.global.testdict1.subKey1.subKey2.subKey3} : {"subKey4" : 3},
${params.global.testdict1.subKey1.subKey2.subKey3.subKey4} : 4,
//
${testdict2.subKey1.subKey2.subKey3.subKey4} : 5,
${params.global.testdict2.subKey1.subKey2.subKey3} : {"subKey4" : 6},
${params.global.testdict2.subKey1.subKey2} : {"subKey3" : {"subKey4" : 7}},
${params.global.testdict2.subKey1} : {"subKey2" : {"subKey3" : {"subKey4" : 8}}},
${params.global.testdict2} : {"subKey1" : {"subKey2" : {"subKey3" : {"subKey4" : 9}}}},
//
${params.global.testdict3} : {"subKey1" : {"subKey2" : {"subKey3" : {"subKey4" : 10}}}},
//
${params.global.testdict4.subKey1.subKey2} : {"subKey3" : {"subKey4" : 20}}
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${testdict1}    [TSM-SNIPPET-TEST] {testdict1}
    rf.extensions.pretty_print    ${testdict2}    [TSM-SNIPPET-TEST] {testdict2}
    rf.extensions.pretty_print    ${testdict3}    [TSM-SNIPPET-TEST] {testdict3}
    rf.extensions.pretty_print    ${testdict4}    [TSM-SNIPPET-TEST] {testdict4}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"listparam" : ["A","B","C"],
"param" : ${params.global.listparam}0]
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    output not expected    [TSM-SNIPPET-TEST]
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"listparam" : ["A","B","C"],
"param" : "${params.global.listparam}0]"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    output not expected    [TSM-SNIPPET-TEST]
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"keyP"  : "A",
"dictP" : {"A" : 1, "B" : 2},
"param" : "${params.global.dictP['${params.global.keyP}']}"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param}    [TSM-SNIPPET-TEST] {param}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
${params.global.testdict1.subKey1.subKey2} : 1,
"testdict2" : ${params.global.testdict1},
${params.global.testdict2.subKey1.subKey2} : 2,
${params.global.testdict1.subKey1.subKey2} : 3
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${testdict1}    [TSM-SNIPPET-TEST] {testdict1}
    rf.extensions.pretty_print    ${testdict2}    [TSM-SNIPPET-TEST] {testdict2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
${params.global.testdict3.subKey1.subKey2} : 4,
"testdict4" : ${params.global.testdict3},
${params.global.testdict3.subKey1.subKey2} : 5,
${params.global.testdict4.subKey1.subKey2} : 6
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${testdict3}    [TSM-SNIPPET-TEST] {testdict1}
    rf.extensions.pretty_print    ${testdict4}    [TSM-SNIPPET-TEST] {testdict2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"testlist1" : [1,2],
"testlist2" : ${params.global.testlist1},
${params.global.testlist1}[0] : 3,
${params.global.testlist2}[1] : 4
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${testlist1}    [TSM-SNIPPET-TEST] {testlist1}
    rf.extensions.pretty_print    ${testlist2}    [TSM-SNIPPET-TEST] {testlist2}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"testlist3" : [5,6],
"testlist4" : ${params.global.testlist3},
${params.global.testlist4}[0] : 7,
${params.global.testlist3}[1] : 8
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${testlist3}    [TSM-SNIPPET-TEST] {testlist3}
    rf.extensions.pretty_print    ${testlist4}    [TSM-SNIPPET-TEST] {testlist4}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param" : "value",
${params.global.param} : ${params.global.param}
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param}    [TSM-SNIPPET-TEST] {param}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param" : {"A" : 1},
${params.global.param} : ${params.global.param}
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param}    [TSM-SNIPPET-TEST] {param}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param" : ["A" , 1],
${params.global.param} : ${params.global.param}
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param}    [TSM-SNIPPET-TEST] {param}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"keyP"       : "A",
"B"          : "params.global.keyP",
"dictP"      : {"A" : "params.global.B"},
//
"newparam_1" : "${params.global.dictP}['${params.global.keyP}']",                                        // => "${params.global.dictP}['A']" -> 'params.global.B'
"newparam_2" : "${${params.global.dictP}['${params.global.keyP}']}",                                     // => "${params.global.B}"          -> 'params.global.keyP'
"newparam_3" : "${${${params.global.dictP}['${params.global.keyP}']}}",                                  // => "${params.global.keyP}"       -> 'A'
"newparam_4" : "${params.global.dictP}['${${${params.global.dictP}['${params.global.keyP}']}}']",        // => "${params.global.dictP}['A']" -> 'params.global.B'
"newparam_5" : "${${params.global.dictP}['${${${params.global.dictP}['${params.global.keyP}']}}']}",     // => "${params.global.B}"          -> 'params.global.keyP'
"newparam_6" : "${${${params.global.dictP}['${${${params.global.dictP}['${params.global.keyP}']}}']}}",  // => "${params.global.keyP}"       -> 'A'
"newparam_7" : "${params.global.dictP}['${${${params.global.dictP}['${${${params.global.dictP}['${params.global.keyP}']}}']}}']",      // => "${params.global.dictP}['A']" -> 'params.global.B'
"newparam_8" : "${${params.global.dictP}['${${${params.global.dictP}['${${${params.global.dictP}['${params.global.keyP}']}}']}}']}",   // => "${params.global.B}"          -> 'params.global.keyP'
"newparam_9" : "${${${params.global.dictP}['${${${params.global.dictP}['${${${params.global.dictP}['${params.global.keyP}']}}']}}']}}" // => "${params.global.keyP}"       -> 'A'
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${newparam_1}    [TSM-SNIPPET-TEST] {newparam_1}
    rf.extensions.pretty_print    ${newparam_2}    [TSM-SNIPPET-TEST] {newparam_2}
    rf.extensions.pretty_print    ${newparam_3}    [TSM-SNIPPET-TEST] {newparam_3}
    rf.extensions.pretty_print    ${newparam_4}    [TSM-SNIPPET-TEST] {newparam_4}
    rf.extensions.pretty_print    ${newparam_5}    [TSM-SNIPPET-TEST] {newparam_5}
    rf.extensions.pretty_print    ${newparam_6}    [TSM-SNIPPET-TEST] {newparam_6}
    rf.extensions.pretty_print    ${newparam_7}    [TSM-SNIPPET-TEST] {newparam_7}
    rf.extensions.pretty_print    ${newparam_8}    [TSM-SNIPPET-TEST] {newparam_8}
    rf.extensions.pretty_print    ${newparam_9}    [TSM-SNIPPET-TEST] {newparam_9}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param1" : "A",
"params" : {  "${params.global.param1}" : "A",
            "param2" : "B"
           }
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${params}    [TSM-SNIPPET-TEST] {params}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"listparam" : ["A","B","C"],
"param_1"   : "}${params.global.listparam}[0]{",
"param_2"   : "{${params.global.listparam}[0]}",
"param_3"   : "$}${params.global.listparam}[0]$}",
"param_4"   : "{$}${params.global.listparam}[0]{$}",
"param_5"   : "}{$}${params.global.listparam}[0]{$}{",
"param_6"   : "{}{$}${params.global.listparam}[0]{$}{}",
"param_7"   : "{}${params.global.listparam}[0]{$}${params.global.listparam}[1]{$}${params.global.listparam}[2]{}",
"param_8"   : "{}$${params.global.listparam}[0]{$$}$${params.global.listparam}[1]{$$}$${params.global.listparam}[2]{}",
"param_9"   : "{[}$${params.global.listparam}[0]]{$[$}$${params.global.listparam}[1]}{$$}$${params.global.listparam}[2]{}()"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param_1}    [TSM-SNIPPET-TEST] {param_1}
    rf.extensions.pretty_print    ${param_2}    [TSM-SNIPPET-TEST] {param_2}
    rf.extensions.pretty_print    ${param_3}    [TSM-SNIPPET-TEST] {param_3}
    rf.extensions.pretty_print    ${param_4}    [TSM-SNIPPET-TEST] {param_4}
    rf.extensions.pretty_print    ${param_5}    [TSM-SNIPPET-TEST] {param_5}
    rf.extensions.pretty_print    ${param_6}    [TSM-SNIPPET-TEST] {param_6}
    rf.extensions.pretty_print    ${param_7}    [TSM-SNIPPET-TEST] {param_7}
    rf.extensions.pretty_print    ${param_8}    [TSM-SNIPPET-TEST] {param_8}
    rf.extensions.pretty_print    ${param_9}    [TSM-SNIPPET-TEST] {param_9}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param" : "Hello empty bracket []"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param}    [TSM-SNIPPET-TEST] {param}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param" : "Hello spaced bracket [    ]"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param}    [TSM-SNIPPET-TEST] {param}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param" : "Hello filled bracket [selftest]"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param}    [TSM-SNIPPET-TEST] {param}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param" : "{Hello filled bracket after string}[selftest]"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param}    [TSM-SNIPPET-TEST] {param}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      sParamsGlobalDefinitions = """
"param" : "Hello filled bracket with spaces [self  test]"
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${param}    [TSM-SNIPPET-TEST] {param}
"""

      sTestConfigFileCode = self.__GetTestConfigFileCode(sParamsGlobalDefinitions)
      sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
      listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sParamsGlobalDefinitions))

      # --------------------------------------------------------------------------------------------------------------

      return sHeadline, listoftuplesCodeSnippets

   # eof def GetSeveralParticularSnippets(self):

   # --------------------------------------------------------------------------------------------------------------

   def GetExpressions(self):
      """Several expressions at several positions within a complex data structure
      """

      sHeadline = "Several expressions at several positions within a complex data structure"

      sParamsGlobalDefinitions = """
"indexP" : 0,
"keyP"   : "A",
"dictP"  : {"A" : 0, "B" : 1},
"listP"  : ["A", "B"],
"params" : {*01* : *02*,
            *03* : [*04*, {*05* : *06*,
                           *07* : [*08*, [*09*, *10*]],
                           *11* : [*12*, {*13* : *14*}],
                           *15* : {*16* : [*17*, *18*]},
                           *19* : {*20* : {*21* : *22*}}
                          }
                    ]
           }
"""

      sRobotTestCode = """
    rf.extensions.pretty_print    ${indexP}    [TSM-SNIPPET-TEST] {indexP}
    rf.extensions.pretty_print    ${keyP}    [TSM-SNIPPET-TEST] {keyP}
    rf.extensions.pretty_print    ${dictP}    [TSM-SNIPPET-TEST] {dictP}
    rf.extensions.pretty_print    ${listP}    [TSM-SNIPPET-TEST] {listP}
    rf.extensions.pretty_print    ${params}    [TSM-SNIPPET-TEST] {params}
"""

      # We have a list of expressions and we have a list of placeholders like used in sParamsGlobalDefinitions.
      # The followig code runs in a nested loop: Every expression is placed at every placeholder position. Only one single
      # expression and placeholder per iteration. All remaining placeholders in current iteration are replaced by elements
      # from a list of filler expressions (simple letters) that are only used to complete the code snippet, but are not in focus.

      listExpressions = ["None", "${True}", "${None}", "\"${False}\"", "\"${None}\"",
                         "${params.global.indexP}", "${params.global.keyP}", "${params.global.dictP}", "${params.global.listP}",
                         "\"${params.global.indexP}\"", "\"${params.global.keyP}\"", "\"${params.global.dictP}\"", "\"${params.global.listP}\"", "123",
                         "${IAMNOTEXISTING}", "${params.global.dictP}[${IAMNOTEXISTING}]", "${params.global.listP}[${IAMNOTEXISTING}]",
                         ".", "..", "[]", "[..]", "[.  .]", "{}", "{..}", "{.  .}", "/", "\\", "|", "*", "+", "-", "$", "\"", "'", "#", "\"#\"", ":"]
                         ### "\"${listPparams.global.}[${params.global.indexP}]\"", "\"${params.global.dictP}[${params.global.keyP}]\"",
                         ### "\"${params.global.listP}[${params.global.dictP}[${params.global.keyP}]]\"",
                         ### "\"${params.global.dictP}[${params.global.listP}[${params.global.indexP}]]\""]

      listPlaceholders = ["*01*", "*02*", "*03*", "*04*", "*05*", "*06*", "*07*", "*08*", "*09*", "*10*", "*11*",
                          "*12*", "*13*", "*14*", "*15*", "*16*", "*17*", "*18*", "*19*", "*20*", "*21*", "*22*"]

      listPositions = listPlaceholders[:] # to support a nested iteration of the same list; better readibility of code because of different names

      listFiller = ["001","002","003","004","005","006","007","008","009","010",
                    "011","012","013","014","015","016","017","018","019","020","021","022"] # as much elements as in listPlaceholders

      # put all things together

      listoftuplesCodeSnippets = []
      for sExpression in listExpressions:
         for sPosition in listPositions:
            sDataStructure = sParamsGlobalDefinitions # init a new data structure from pattern sParamsGlobalDefinitions
            oFiller = CListElements(listFiller)       # init a new filler object (= content for remaining placeholders)
            for sPlaceholder in listPlaceholders:
               sFiller = oFiller.GetElement()
               if sPosition == sPlaceholder:
                  sDataStructure = sDataStructure.replace(sPlaceholder, sExpression)
               else:
                  sDataStructure = sDataStructure.replace(sPlaceholder, f"\"{sFiller}\"")
            # eof for sPlaceholder in listPlaceholders:
            sTestConfigFileCode = self.__GetTestConfigFileCode(sDataStructure)
            sRobotTestFileCode  = self.__GetRobotTestFileCode(sRobotTestCode)
            listoftuplesCodeSnippets.append((sTestConfigFileCode, sRobotTestFileCode, sDataStructure))
         # eof for sPosition in listPositions:
      # eof for sExpression in listExpressions:

      return sHeadline, listoftuplesCodeSnippets

   # eof def GetExpressions(self):

   # --------------------------------------------------------------------------------------------------------------

# eof class CSnippets():

# --------------------------------------------------------------------------------------------------------------
# eof class definitions
# --------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------
#[INITCONFIG]
# --------------------------------------------------------------------------------------------------------------
#TM***

# -- configuration setup (relative to the path of this app)
oConfig = None
try:
   oConfig = CConfig(os.path.abspath(sys.argv[0]))
except Exception as reason:
   sResult = CString.FormatResult(sMethod="(main)", bSuccess=None, sResult=str(reason))
   print()
   printfailure(sResult)
   print()
   sys.exit(ERROR)

# update version and date of this app
oConfig.Set("APP_VERSION", VERSION)
oConfig.Set("APP_VERSION_DATE", VERSION_DATE)
THISAPPNAME     = oConfig.Get('THISAPPNAME')
THISAPPFULLNAME = f"{THISAPPNAME} v. {VERSION} / {VERSION_DATE}"
oConfig.Set("THISAPPFULLNAME", THISAPPFULLNAME)


# --------------------------------------------------------------------------------------------------------------
#[INITLOGGER]
# --------------------------------------------------------------------------------------------------------------
#TM***

oLogger = None
try:
   oLogger = CLogger(oConfig)
except Exception as reason:
   sResult = CString.FormatResult(sMethod="(main)", bSuccess=None, sResult=str(reason))
   print()
   printfailure(sResult)
   print()
   sys.exit(ERROR)


# --------------------------------------------------------------------------------------------------------------

# ---- prepare initial output

# dump configuration values to log file
listFormattedOutputLines = oConfig.DumpConfig()
oLogger.WriteLog(120*"*")
oLogger.WriteLog(listFormattedOutputLines)
oLogger.WriteLog(120*"*" + "\n")

# write HTML header to report file
oHTMLPattern = CHTMLPattern()
oLogger.WriteReport(oHTMLPattern.GetHTMLHeader())
del oHTMLPattern

# --------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------
#[INITCOUNTER]
# --------------------------------------------------------------------------------------------------------------
#TM***

oCounter = CCounter()


# --------------------------------------------------------------------------------------------------------------
#[INITEXECUTOR]
# --------------------------------------------------------------------------------------------------------------
#TM***

oExecutor = None
try:
   oExecutor = CExecutor(oConfig, oCounter, oLogger)
except Exception as reason:
   sResult = CString.FormatResult(sMethod="(main)", bSuccess=None, sResult=str(reason))
   print()
   printfailure(sResult)
   print()
   sys.exit(ERROR)

bSuccess, sResult = oExecutor.GenInfrastructure()
if bSuccess is not True:
   sResult = CString.FormatResult(sMethod="(main)", bSuccess=bSuccess, sResult=sResult)
   print()
   printfailure(sResult)
   print()
   sys.exit(ERROR)

print(sResult)
print()



# --------------------------------------------------------------------------------------------------------------
#[STARTOFEXECUTION]
# --------------------------------------------------------------------------------------------------------------
#TM***

oSnippets = CSnippets()

sHeadline, listoftuplesCodeSnippets = oSnippets.GetSeveralParticularSnippets()
bSuccess, sResult = oExecutor.Execute(sHeadline, listoftuplesCodeSnippets, "TSM")

sHeadline, listoftuplesCodeSnippets = oSnippets.GetExpressions()
bSuccess, sResult = oExecutor.Execute(sHeadline, listoftuplesCodeSnippets, "TSM")

print()
print(COLBG + "done")
print()


# --------------------------------------------------------------------------------------------------------------

# PrettyPrint(sHeadline, sPrefix="(sHeadline)")
# PrettyPrint(listoftuplesCodeSnippets, sPrefix="(listoftuplesCodeSnippets)")

# --------------------------------------------------------------------------------------------------------------
#[ENDOFEXECUTION]
# --------------------------------------------------------------------------------------------------------------
#TM***

# write HTML footer to report file
oHTMLPattern = CHTMLPattern()
oLogger.WriteReport(oHTMLPattern.GetHTMLFooter(oConfig.Get('NOW')))
del oHTMLPattern

del oConfig
del oLogger
del oCounter
del oExecutor

sys.exit(SUCCESS)

# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

