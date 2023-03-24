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
# CExecute.py
#
# XC-CT/ECA3-Queckenstedt
#
# 24.03.2023
#
# **************************************************************************************************************

# -- import standard Python modules
import os, sys, shlex, subprocess

from PythonExtensionsCollection.String.CString import CString

# --------------------------------------------------------------------------------------------------------------
# TM***

class CExecute(object):
   """
   """

   def Execute(sTestID=None):
      """
      """
      sThisFilePath = os.path.dirname(CString.NormalizePath(__file__))
      sPython         = CString.NormalizePath(sys.executable)
      sTestScript   = CString.NormalizePath("../../../component_test.py", sReferencePathAbs=sThisFilePath)
      print(f"(debug) sTestScript: {sTestScript}")
      listCmdLineParts = []
      listCmdLineParts.append(f"\"{sPython}\"")
      listCmdLineParts.append(f"\"{sTestScript}\"")
      listCmdLineParts.append(f"--testid=\"{sTestID}\"")
      listCmdLineParts.append(f"--silent")
      sCmdLine = " ".join(listCmdLineParts)
      print(f"(debug) sCmdLine: {sCmdLine}")
      listCmdLineParts = shlex.split(sCmdLine)
      nReturn = subprocess.call(listCmdLineParts)
      return nReturn
   # eof def Execute(sTestID=None):

   Execute = staticmethod(Execute)

# eof class CExecute():

# **************************************************************************************************************

