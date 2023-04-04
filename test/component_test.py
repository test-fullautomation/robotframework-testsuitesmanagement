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
# component_test.py
#
# XC-CT/ECA3-Queckenstedt
#
# --------------------------------------------------------------------------------------------------------------
#
# 04.04.2023 / v. 0.1.0
# initial prototype
#
# --------------------------------------------------------------------------------------------------------------
#TM***
# TOC:
# [TESTCONFIG]
# [CODEDUMP]
# [ADDITIONALSTEPS]
# [EXECUTION]
# --------------------------------------------------------------------------------------------------------------

import os, sys, shlex, subprocess, ctypes, time

import colorama as col

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Folder.CFolder import CFolder
from PythonExtensionsCollection.File.CFile import CFile
from PythonExtensionsCollection.Utils.CUtils import *
from PythonExtensionsCollection.Comparison.CComparison import CComparison

from libs.CConfig import CConfig
from libs.CCodePatterns import CCodePatterns
from libs.CAdditionalSteps import CAdditionalSteps
from libs.CGenCode import CGenCode
from libs.CTextCheck import CTextCheck

from testconfig.TestConfig import *

col.init(autoreset=True)

COLBR = col.Style.BRIGHT + col.Fore.RED
COLBY = col.Style.BRIGHT + col.Fore.YELLOW
COLBG = col.Style.BRIGHT + col.Fore.GREEN

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg):
   sys.stderr.write(COLBR + f"Error: {sMsg}!\n\n")

# --------------------------------------------------------------------------------------------------------------
# [TESTCONFIG]

# -- initialize configuration

oConfig = None
try:
   oConfig = CConfig(os.path.abspath(__file__))
except Exception as ex:
   print()
   printerror(CString.FormatResult("(main)", None, str(ex)))
   print()
   sys.exit(ERROR)

# --------------------------------------------------------------------------------------------------------------
# some special functions
# (with premature end of execution = no test execution)
# --------------------------------------------------------------------------------------------------------------

CONFIGDUMP = oConfig.Get('CONFIGDUMP')
if CONFIGDUMP is True:
   # currently config is already dumped in constructor of CConfig; => nothing more to do here
   sys.exit(SUCCESS)

# --------------------------------------------------------------------------------------------------------------
# [CODEDUMP]

CODEDUMP = oConfig.Get('CODEDUMP')
if CODEDUMP is True:
   oCodeGenerator = None
   try:
      oCodeGenerator = CGenCode(oConfig)
   except Exception as ex:
      print()
      printerror(CString.FormatResult("(main)", None, str(ex)))
      print()
      sys.exit(ERROR)

   bSuccess, sResult = oCodeGenerator.GenCode()
   if bSuccess is not True:
      print()
      printerror(CString.FormatResult("(main)", bSuccess, sResult))
      print()
      sys.exit(ERROR)

   print(COLBG + f"{sResult}\n")

   # after code dump nothing more to do here
   sys.exit(SUCCESS)

# --------------------------------------------------------------------------------------------------------------
# [ADDITIONALSTEPS]

oAdditionalSteps = None
try:
   oAdditionalSteps = CAdditionalSteps(oConfig)
except Exception as ex:
   print()
   printerror(CString.FormatResult("(main)", None, str(ex)))
   print()
   sys.exit(ERROR)


# **************************************************************************************************************
# [EXECUTION]
# **************************************************************************************************************
#TM***

# -- get some configuration values required for execution

THISSCRIPT     = oConfig.Get('THISSCRIPT')
THISSCRIPTNAME = oConfig.Get('THISSCRIPTNAME')
REFERENCEPATH  = oConfig.Get('REFERENCEPATH')
OSNAME         = oConfig.Get('OSNAME')
PLATFORMSYSTEM = oConfig.Get('PLATFORMSYSTEM')
PYTHON         = oConfig.Get('PYTHON')
PYTHONVERSION  = oConfig.Get('PYTHONVERSION')

PATTERNFILE_TXT         = oConfig.Get('PATTERNFILE_TXT')
PATTERNFILE_XML         = oConfig.Get('PATTERNFILE_XML')
IGNOREPATTERNFILE_TXT   = oConfig.Get('IGNOREPATTERNFILE_TXT')
TESTFILESFOLDER         = oConfig.Get('TESTFILESFOLDER')
TESTLOGFILESFOLDER      = oConfig.Get('TESTLOGFILESFOLDER')
SELFTESTLOGFILE         = oConfig.Get('SELFTESTLOGFILE')
REFERENCELOGFILESFOLDER = oConfig.Get('REFERENCELOGFILESFOLDER')

TESTID   = oConfig.Get('TESTID')
SILENT   = oConfig.Get('SILENT')

# -- start logging
oSelfTestLogFile = CFile(SELFTESTLOGFILE)

print("Executing test cases")
print()

nNrOfUsecases = 0

if TESTID is not None:
   listofdictUsecasesSubset = []
   for dictUsecase in listofdictUsecases:
      if TESTID == dictUsecase['TESTID']:
         listofdictUsecasesSubset.append(dictUsecase)
         break # currently assumed that there is only one TESTID provided (maybe later more than one)
   if len(listofdictUsecasesSubset) == 0:
      bSuccess = False
      sResult  = f"Test ID '{TESTID}' not defined"
      printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult))
      sys.exit(ERROR)
   del listofdictUsecases
   listofdictUsecases = listofdictUsecasesSubset
# eof if TESTID is not None:

# --------------------------------------------------------------------------------------------------------------

# -- check for duplicate test IDs
# Test IDs are used to identify and select test cases. They have to be unique.

listIDs = []
listDuplicates = []
for dictUsecase in listofdictUsecases:
   TESTID = dictUsecase['TESTID']
   if TESTID in listIDs:
      listDuplicates.append(TESTID)
   else:
      listIDs.append(TESTID)
# eof for dictUsecase in listofdictUsecases:
if len(listDuplicates) > 0:
   sDuplicates = "[" + ", ".join(listDuplicates) + "]"
   bSuccess = False
   sResult  = f"Duplicate test IDs found: {sDuplicates}\nTest IDs are used to identify and select test cases. They have to be unique"
   printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult))
   sys.exit(ERROR)

# --------------------------------------------------------------------------------------------------------------

nNrOfUsecases = len(listofdictUsecases)

# -- initialize test conter
nCntUsecases        = 0
nCntPassedUsecases  = 0
nCntFailedUsecases  = 0
nCntUnknownUsecases = 0

# -- initialize the text check module
oTextCheck = None
try:
   oTextCheck = CTextCheck(oConfig)
except Exception as ex:
   printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess=None, sResult=str(ex)))
   sys.exit(ERROR)

# -- initialize the comparison module
# Maybe within the following loop we detect that LOGCOMPARE is False. But even so we want to create this class object only once,
# and not in every iteration again and again.
oComparison = CComparison()

listTestsNotPassed = []

for dictUsecase in listofdictUsecases:

   nCntUsecases = nCntUsecases + 1

   TESTID           = dictUsecase['TESTID']
   DESCRIPTION      = dictUsecase['DESCRIPTION']
   EXPECTATION      = dictUsecase['EXPECTATION']
   SECTION          = dictUsecase['SECTION']
   SUBSECTION       = dictUsecase['SUBSECTION']
   COMMENT          = dictUsecase['COMMENT']
   TESTFILENAME     = dictUsecase['TESTFILENAME']
   TESTFOLDERNAME   = dictUsecase['TESTFOLDERNAME']
   ADDITIONALPARAMS = dictUsecase['ADDITIONALPARAMS']
   EXPECTEDRETURN   = dictUsecase['EXPECTEDRETURN']
   # optional ones
   HINT = None
   if "HINT" in dictUsecase:
      HINT = dictUsecase['HINT']
   PRESTEP = None
   if "PRESTEP" in dictUsecase:
      PRESTEP = dictUsecase['PRESTEP']
   POSTSTEP = None
   if "POSTSTEP" in dictUsecase:
      POSTSTEP = dictUsecase['POSTSTEP']
   LOGCOMPARE = oConfig.Get('LOGCOMPARE')
   if "LOGCOMPARE" in dictUsecase:
      # local value of use case overwrites global configuration value
      LOGCOMPARE = dictUsecase['LOGCOMPARE']
   # derived ones
   TESTFULLNAME              = f"{TESTID}-({SECTION})-[{SUBSECTION}]"
   TESTLOGFILE_TXT           = f"{TESTLOGFILESFOLDER}/{TESTFULLNAME}/{TESTFULLNAME}.log"
   REFERENCELOGFILE_TXT      = f"{REFERENCELOGFILESFOLDER}/{TESTFULLNAME}/{TESTFULLNAME}.log"
   TESTLOGFILE_XML           = f"{TESTLOGFILESFOLDER}/{TESTFULLNAME}/{TESTFULLNAME}.xml"
   REFERENCELOGFILE_XML      = f"{REFERENCELOGFILESFOLDER}/{TESTFULLNAME}/{TESTFULLNAME}.xml"
   CURRENTTESTLOGFILESFOLDER = f"{TESTLOGFILESFOLDER}/{TESTFULLNAME}"

   sOut = f"====== [TEST] : '{TESTFULLNAME}' / ({nCntUsecases}/{nNrOfUsecases})"
   if SILENT is False:
      print(COLBY + sOut)
      print()
   oSelfTestLogFile.Write(sOut, 1)
   sOut = f"[DESCRIPTION] : {DESCRIPTION}"
   if SILENT is False:
      print(COLBY + sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"[EXPECTATION] : {EXPECTATION}"
   if SILENT is False:
      print(COLBY + sOut)
   oSelfTestLogFile.Write(sOut)
   if HINT is not None:
      sOut = f"       [HINT] : {HINT}"
      if SILENT is False:
         print(COLBY + sOut)
      oSelfTestLogFile.Write(sOut)
   sOut = f"    [COMMENT] : {COMMENT}"
   if SILENT is False:
      print(COLBY + sOut)
      print()
   oSelfTestLogFile.Write(sOut, 1)

   listCmdLineParts = []
   listCmdLineParts.append(f"\"{PYTHON}\"")
   listCmdLineParts.append("-m robot")
   listCmdLineParts.append("-d")
   listCmdLineParts.append(f"\"{CURRENTTESTLOGFILESFOLDER}\"")
   listCmdLineParts.append("-o")
   listCmdLineParts.append(f"\"{TESTLOGFILE_XML}\"")
   listCmdLineParts.append("-l")
   listCmdLineParts.append(f"\"{TESTLOGFILESFOLDER}/{TESTFULLNAME}/{TESTFULLNAME}_log.html\"")
   listCmdLineParts.append("-r")
   listCmdLineParts.append(f"\"{TESTLOGFILESFOLDER}/{TESTFULLNAME}/{TESTFULLNAME}_report.html\"")
   listCmdLineParts.append("-b")
   listCmdLineParts.append(f"\"{TESTLOGFILE_TXT}\"")
   if ADDITIONALPARAMS is not None:
      listCmdLineParts.append(f"{ADDITIONALPARAMS}")

   if ( (TESTFILENAME is not None) and (TESTFOLDERNAME is not None) ):
      print()
      bSuccess = None
      sResult  = "Both is defined: 'TESTFILENAME' and 'TESTFOLDERNAME', but only one of them is allowed"
      printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult))
      print()
      nCntUnknownUsecases = nCntUnknownUsecases + 1
      printerror(f"Test '{TESTFULLNAME}' result: UNKNOWN\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
      oSelfTestLogFile.Write("Result: UNKNOWN", 1)
      listTestsNotPassed.append(TESTFULLNAME)
      continue # for dictUsecase in listofdictUsecases:
   if TESTFILENAME is not None:
      listCmdLineParts.append(f"\"{TESTFILESFOLDER}/{TESTFILENAME}\"")
   elif TESTFOLDERNAME is not None:
      listCmdLineParts.append(f"\"{TESTFILESFOLDER}/{TESTFOLDERNAME}\"")
   else:
      # invalid
      pass

   # --------------------------------------------------------------------------------------------------------------

   # -- prestep
   if PRESTEP is not None:
      print(COLBY + f"Executing pre step: '{PRESTEP}'")
      bSuccess, sResult = oAdditionalSteps.Execute(PRESTEP)
      if bSuccess is not True:
         print()
         printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult))
         print()
         nCntUnknownUsecases = nCntUnknownUsecases + 1
         printerror(f"Test '{TESTFULLNAME}' result: UNKNOWN\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
         oSelfTestLogFile.Write("Result: UNKNOWN", 1)
         listTestsNotPassed.append(TESTFULLNAME)
         continue # for dictUsecase in listofdictUsecases:

   bContinue = False

   sCmdLine = " ".join(listCmdLineParts)
   del listCmdLineParts
   if SILENT is False:
      print(f"Now executing command line:\n{sCmdLine}")
      print()
   listCmdLineParts = shlex.split(sCmdLine)
   nReturn = ERROR
   bIsAlreadyUnknown = False
   try:
      nReturn = subprocess.call(listCmdLineParts)
      print()
      bSuccess = True
      sResult  = f"Robot Framework returned {nReturn}"
      print(CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult))
   except Exception as ex:
      print()
      printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess=None, sResult=str(ex)))
      print()
      nCntUnknownUsecases = nCntUnknownUsecases + 1
      printerror(f"Test '{TESTFULLNAME}' result: UNKNOWN\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
      oSelfTestLogFile.Write("Result: UNKNOWN", 1)
      listTestsNotPassed.append(TESTFULLNAME)
      bIsAlreadyUnknown = True
      bContinue = True # 'continue' will be done after POSTSTEP
   print()

   # --------------------------------------------------------------------------------------------------------------

   # -- poststep (has to be executed also in case of subprocess.call() failed)
   if POSTSTEP is not None:
      print(COLBY + f"Executing post step: '{POSTSTEP}'")
      bSuccess, sResult = oAdditionalSteps.Execute(POSTSTEP)
      if bSuccess is not True:
         print()
         printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult))
         print()
         if bIsAlreadyUnknown is False:
            nCntUnknownUsecases = nCntUnknownUsecases + 1
            printerror(f"Test '{TESTFULLNAME}' result: UNKNOWN\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
            oSelfTestLogFile.Write("Result: UNKNOWN", 1)
            listTestsNotPassed.append(TESTFULLNAME)
         continue # for dictUsecase in listofdictUsecases:

   # --------------------------------------------------------------------------------------------------------------

   if bContinue is True:
      # if subprocess.call() failed
      continue # for dictUsecase in listofdictUsecases:

   # --------------------------------------------------------------------------------------------------------------

   if nReturn != EXPECTEDRETURN:
      # result from subprocess.call()
      print()
      bSuccess = False
      sResult  = f"Robot Framework returned not expected value {nReturn}"
      sResult  = CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult)
      printerror(sResult)
      oSelfTestLogFile.Write(sResult)
      print()
      nCntFailedUsecases = nCntFailedUsecases + 1
      printerror(f"Test '{TESTFULLNAME}' failed\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
      oSelfTestLogFile.Write("Result: FAILED", 1)
      listTestsNotPassed.append(TESTFULLNAME)
      continue # for dictUsecase in listofdictUsecases:

   # --------------------------------------------------------------------------------------------------------------

   # -- log file pre check (check for forbidden patterns)
   bCheckResult, bSuccess, sResult = oTextCheck.TextCheck(TESTLOGFILE_TXT)
   if bSuccess is not True:
      print()
      sResult = CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult)
      printerror(sResult)
      oSelfTestLogFile.Write(sResult)
      print()
      nCntUnknownUsecases = nCntUnknownUsecases + 1
      printerror(f"Test '{TESTFULLNAME}' result: UNKNOWN\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
      oSelfTestLogFile.Write("Result: UNKNOWN", 1)
      listTestsNotPassed.append(TESTFULLNAME)
      continue # for dictUsecase in listofdictUsecases:
   if bCheckResult is None:
      print(COLBY + "No forbidden patterns defined, log file pre check skipped")
      print()
   elif bCheckResult is True:
      print(COLBY + "Log file pre check for forbidden patterns passed")
      print()
   else:
      print()
      printerror(sResult)
      oSelfTestLogFile.Write(sResult)
      print()
      nCntFailedUsecases = nCntFailedUsecases + 1
      printerror(f"Test '{TESTFULLNAME}' result: FAILED\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
      oSelfTestLogFile.Write("Result: FAILED", 1)
      listTestsNotPassed.append(TESTFULLNAME)
      continue # for dictUsecase in listofdictUsecases:

   # --------------------------------------------------------------------------------------------------------------

   # -- log file comparison

   if LOGCOMPARE is True:

      tupleFilesToCheck = (TESTLOGFILE_TXT, REFERENCELOGFILE_TXT, TESTLOGFILE_XML, REFERENCELOGFILE_XML)
      bFileMissing = False
      for sFileToCheck in tupleFilesToCheck:
         if os.path.isfile(sFileToCheck) is False:
            bFileMissing = True
            bSuccess = False
            sResult  = f"Missing log file of test '{TESTFULLNAME}': '{sFileToCheck}'"
            printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult))
      # eof for sFileToCheck in tupleFilesToCheck:
      if bFileMissing is True:
         nCntUnknownUsecases = nCntUnknownUsecases + 1
         printerror(f"Usecase '{TESTFULLNAME}' result: UNKNOWN\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
         oSelfTestLogFile.Write("Result: UNKNOWN", 1)
         listTestsNotPassed.append(TESTFULLNAME)
         continue # for dictUsecase in listofdictUsecases:

      # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

      print(COLBY + "Log file check 1/2: debug log file in text format")
      print()

      bIdentical, bSuccess, sResult = oComparison.Compare(TESTLOGFILE_TXT, REFERENCELOGFILE_TXT, sPatternFile=PATTERNFILE_TXT, sIgnorePatternFile=IGNOREPATTERNFILE_TXT)

      print(f"(1) Test log file      : {TESTLOGFILE_TXT}")
      print(f"(2) Reference log file : {REFERENCELOGFILE_TXT}")
      print(f"(3) Pattern file       : {PATTERNFILE_TXT}")
      print(f"(3) 'Ignore' pattern   : {IGNOREPATTERNFILE_TXT}")
      print()

      if bSuccess is not True:
         print()
         printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult))
         print()
         nCntUnknownUsecases = nCntUnknownUsecases + 1
         printerror(f"Test '{TESTFULLNAME}' result: UNKNOWN\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
         oSelfTestLogFile.Write("Result: UNKNOWN", 1)
         listTestsNotPassed.append(TESTFULLNAME)
         continue # for dictUsecase in listofdictUsecases:
      else:
         if bIdentical is True:
            print(COLBY + "passed")
            print()
            # now continue with log file check 2/2
         else:
            print()
            printerror(sResult) # without FormatResult!
            nCntFailedUsecases = nCntFailedUsecases + 1
            printerror(f"Test '{TESTFULLNAME}' failed\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
            oSelfTestLogFile.Write("Result: FAILED", 1)
            listTestsNotPassed.append(TESTFULLNAME)
            continue # for dictUsecase in listofdictUsecases:
      # eof else - if bSuccess is not True:

      # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

      print(COLBY + "Log file check 2/2: XML log file")
      print()

      bIdentical, bSuccess, sResult = oComparison.Compare(TESTLOGFILE_XML, REFERENCELOGFILE_XML, sPatternFile=PATTERNFILE_XML)

      print(f"(1) Test log file      : {TESTLOGFILE_XML}")
      print(f"(2) Reference log file : {REFERENCELOGFILE_XML}")
      print(f"(3) Pattern file       : {PATTERNFILE_XML}")

      if bSuccess is True:
         if bIdentical is True:
            print()
            print(COLBY + "passed")
            print()
            print(COLBY + f"    Test '{TESTFULLNAME}': log file checks passed") # related to both: (1/2) and (2/2) !!!
            print()
         else:
            print()
            printerror(sResult) # without FormatResult!
            nCntFailedUsecases = nCntFailedUsecases + 1
            printerror(f"Test '{TESTFULLNAME}' failed\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
            oSelfTestLogFile.Write("Result: FAILED", 1)
            listTestsNotPassed.append(TESTFULLNAME)
            continue # for dictUsecase in listofdictUsecases:
      else:
         print()
         printerror(CString.FormatResult(THISSCRIPTNAME, bSuccess, sResult)) # bSuccess, sResult from oComparison.Compare()
         print()
         nCntUnknownUsecases = nCntUnknownUsecases + 1
         printerror(f"Test '{TESTFULLNAME}' result: UNKNOWN\n[DESCRIPTION]: {DESCRIPTION}\n[EXPECTATION]: {EXPECTATION}\n[COMMENT]: {COMMENT}")
         oSelfTestLogFile.Write("Result: UNKNOWN", 1)
         listTestsNotPassed.append(TESTFULLNAME)
         continue # for dictUsecase in listofdictUsecases:
      # eof else - if bSuccess is True:

   # eof if LOGCOMPARE is True:

   # -- if nothing went wrong up to here, the test is passed:
   nCntPassedUsecases = nCntPassedUsecases + 1
   print(COLBG + f"    Test '{TESTFULLNAME}' passed")
   print()
   oSelfTestLogFile.Write("Result: PASSED", 1)

# eof for dictUsecase in listofdictUsecases:

# --------------------------------------------------------------------------------------------------------------

# paranoia check
if ( (nCntPassedUsecases + nCntFailedUsecases + nCntUnknownUsecases != nCntUsecases) or (nNrOfUsecases != nCntUsecases) ):
   print()
   sOut = CString.FormatResult(THISSCRIPTNAME, bSuccess=False, sResult="Internal counter mismatch")
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"Defined  : {nNrOfUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"Executed : {nCntUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"PASSED   : {nCntPassedUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"FAILED   : {nCntFailedUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   sOut = f"UNKNOWN  : {nCntUnknownUsecases}"
   printerror(sOut)
   oSelfTestLogFile.Write(sOut)
   print()
   del oSelfTestLogFile
   sys.exit(ERROR)

# --------------------------------------------------------------------------------------------------------------

# -- component test result (over all test cases)

if len(listTestsNotPassed) > 0:
   print()
   sOut = "Tests that are not PASSED:"
   oSelfTestLogFile.Write(sOut + "\n")
   print(COLBY + sOut)
   print()
   for sTest in listTestsNotPassed:
      sOut = f"- {sTest}"
      oSelfTestLogFile.Write(sOut)
      print(sOut)
   oSelfTestLogFile.Write()
   print()

nReturn = ERROR

if nCntUsecases == 0:
   sOut = "Nothing executed - but why?" # should not happen
   oSelfTestLogFile.Write(sOut, 1)
   printerror(fsOut)
   nReturn = ERROR
elif ( (nCntFailedUsecases == 0) and (nCntUnknownUsecases == 0) ):
   sOut = f"Component test PASSED"
   oSelfTestLogFile.Write(sOut, 1)
   print(COLBG + sOut)
   print()
   nReturn = SUCCESS
else:
   sOut = f"Component test FAILED"
   oSelfTestLogFile.Write(sOut, 1)
   printerror(sOut)
   nReturn = ERROR

sOut = f"Defined : {nNrOfUsecases}"
print(COLBY + sOut)
oSelfTestLogFile.Write(sOut)
sOut = f"PASSED  : {nCntPassedUsecases}"
print(COLBY + sOut)
oSelfTestLogFile.Write(sOut)
sOut = f"FAILED  : {nCntFailedUsecases}"
print(COLBY + sOut)
oSelfTestLogFile.Write(sOut)
sOut = f"UNKNOWN : {nCntUnknownUsecases}"
print(COLBY + sOut)
oSelfTestLogFile.Write(sOut)

print()

del oSelfTestLogFile

sys.exit(nReturn)

# --------------------------------------------------------------------------------------------------------------

