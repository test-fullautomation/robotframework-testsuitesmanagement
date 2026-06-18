# **************************************************************************************************************
#
#  Copyright 2020-2026 Robert Bosch GmbH
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
# Mai Minh Tri
#
# coverage.py
#
# --------------------------------------------------------------------------------------------------------------
#
# 06.23.2022
#
# --------------------------------------------------------------------------------------------------------------

import os, sys, platform, shlex, subprocess, shutil, argparse, json

import colorama as col

from PythonExtensionsCollection.String.CString import CString
from PythonExtensionsCollection.Folder.CFolder import CFolder

col.init(autoreset=True)

COLBR = col.Style.BRIGHT + col.Fore.RED
COLBY = col.Style.BRIGHT + col.Fore.YELLOW
COLBG = col.Style.BRIGHT + col.Fore.GREEN

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg):
    sys.stderr.write(COLBR + f"Error: {sMsg}!\n")

def printexception(sMsg):
    sys.stderr.write(COLBR + f"Exception: {sMsg}!\n")

# --------------------------------------------------------------------------------------------------------------

# -- some informations about the environment of this script

sThisScript     = sys.argv[0]
sThisScript     = CString.NormalizePath(sThisScript)
sThisScriptPath = os.path.dirname(sThisScript)
sThisScriptName = os.path.basename(sThisScript)
sComponentPath  = CString.NormalizePath(sys.argv[1])

sOSName         = os.name
sPlatformSystem = platform.system()
sPythonPath     = CString.NormalizePath(os.path.dirname(sys.executable))
sPython         = CString.NormalizePath(sys.executable)
sPythonVersion  = sys.version
sCoverage       = shutil.which("coverage")

sFilter = None
if sPlatformSystem == "Windows":
    sFilter = "not _Linux_"
   #  sComponentPath = os.path.normpath(sComponentPath)
elif sPlatformSystem == "Linux":
    sFilter = "not _Windows_"
else:
   bSuccess = False
   sResult  = f"Operating system {sPlatformSystem} ({sOSName}) not supported"
   printerror(CString.FormatResult(sThisScriptName, bSuccess, sResult))
   sys.exit(ERROR)

print()
print(f"{sThisScriptName} is running under {sPlatformSystem} ({sOSName})")
print()

# load static configuration values (name of json file is fix)
sCoverageJsonFile = CString.NormalizePath(f"{sThisScriptPath}/config/coverage_config.json")
hCoverageJsonFile = open(sCoverageJsonFile, encoding="utf-8")
oCoverageConfig = json.load(hCoverageJsonFile)
hCoverageJsonFile.close()

sCoverageJsonFileAbs = CString.NormalizePath(f"{sComponentPath}/test/pytest/coverage/config/.coveragerc")
sCoverageStartupPath = CString.NormalizePath(f"{sComponentPath}/test/pytest/coverage/startup")

if sCoverage is None:
   bSuccess = False
   sResult  = "The 'coverage' executable is not available in PATH"
   printerror(CString.FormatResult(sThisScriptName, bSuccess, sResult))
   sys.exit(ERROR)

listCoverage = oCoverageConfig.get('COVERAGE')
for coverage in listCoverage:
   sState       = coverage['STATE']
   sCommandline = coverage['COMMANDLINE']
   sCWD         = coverage['CURRENT_WORKING_DIR']
   sConfig      = coverage['CONFIG']

   if sState in ["report", "html"]:
      sCombineCmdLine = f'"{sCoverage}" combine --rcfile="{sConfig}"'
      print(f"Now executing command line:\n{sCombineCmdLine}")
      print()
      listCombineCmdLineParts = shlex.split(sCombineCmdLine)
      nCombineReturn = subprocess.call(listCombineCmdLineParts,
                                       cwd=CString.NormalizePath(f"{sComponentPath}/{sCWD}"))
      print()
      print(f"[{sThisScriptName}] : Subprocess COVERAGE COMBINE returned {nCombineReturn}")
      print()

   # -- prepare the command line for run the test coverage
   listCmdLineParts = []
   if sCommandline.strip().startswith("pytest "):
      listCmdLineParts.append(f"{sCommandline}")
   else:
      listCmdLineParts.append(f"\"{sCoverage}\"")
      listCmdLineParts.append(f"{sState}")
      listCmdLineParts.append(f"--rcfile=\"{sConfig}\"")
      listCmdLineParts.append(f"{sCommandline}")

   sCmdLine = " ".join(listCmdLineParts)
   del listCmdLineParts

   # -- execute the test coverage
   print(f"Now executing command line:\n{sCmdLine}")
   print()

   listCmdLineParts = shlex.split(sCmdLine)

   nReturn = ERROR
   try:
      nReturn = subprocess.call(listCmdLineParts,
                                cwd=CString.NormalizePath(f"{sComponentPath}/{sCWD}"))
      print()
      print(f"[{sThisScriptName}] : Subprocess PYTEST returned {nReturn}")
   except Exception as ex:
      print()
      printexception(str(ex))
      print()
      sys.exit(ERROR)
   print()

   if nReturn == SUCCESS:
      print()
      print(COLBG + f"{sThisScriptName} done")
   else:
      printerror(f"[{sThisScriptName}] : Subprocess PYTEST has not returned expected value {SUCCESS}")
      nReturn = -nReturn

   print()
   # nReturn:
   # > 0  : internal error of this script
   # < 0  : return value (!= 0) from subprocess
   # == 0 : no internal error of this script and no error from subprocess

sys.exit(nReturn)

# --------------------------------------------------------------------------------------------------------------

