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
# CCodePatterns.py
#
# XC-CT/ECA3-Queckenstedt
#
# 24.03.2023
#
# --------------------------------------------------------------------------------------------------------------

"""
Python module containing the code patterns
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

class CCodePatterns():

   # --------------------------------------------------------------------------------------------------------------

   def GetPyTestFileHeader(self, PYTESTFILENAME="", CLASSNAME=""):
      """
      """

      sPyTestFileHeaderPattern = """# **************************************************************************************************************
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
# --------------------------------------------------------------------------------------------------------------
#
# ####PYTESTFILENAME####
#
# XC-CT/ECA3-Queckenstedt
#
# ####DATEOFCREATION####
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class ####CLASSNAME####:

# --------------------------------------------------------------------------------------------------------------"""

      sPyTestFileHeader = sPyTestFileHeaderPattern.replace("####PYTESTFILENAME####", PYTESTFILENAME)
      sPyTestFileHeader = sPyTestFileHeader.replace("####DATEOFCREATION####", time.strftime('%d.%m.%Y - %H:%M:%S'))
      sPyTestFileHeader = sPyTestFileHeader.replace("####CLASSNAME####", CLASSNAME)
      return sPyTestFileHeader

   # eof def GetPyTestFileHeader(self, PYTESTFILENAME="", CLASSNAME=""):

   # --------------------------------------------------------------------------------------------------------------

   def GetPyTestCase(self, DESCRIPTION="", TESTNAME="", TESTID=""):
      """
      """

      sPyTestCasePattern = """   @pytest.mark.parametrize(
      "Description", ["####DESCRIPTION####",]
   )
   def ####TESTNAME####(self, Description):
      nReturn = CExecute.Execute("####TESTID####")
      assert nReturn == 0"""

      sPyTestCase = sPyTestCasePattern.replace("####DESCRIPTION####", DESCRIPTION)
      sPyTestCase = sPyTestCase.replace("####TESTNAME####", TESTNAME)
      sPyTestCase = sPyTestCase.replace("####TESTID####", TESTID)

      return sPyTestCase

   # eof def GetPyTestCase(self, DESCRIPTION="", TESTNAME="", TESTID=""):

   # --------------------------------------------------------------------------------------------------------------

   def GetCopyRightRST(self):
      """
      """

      sCopyRightRST = """.. Copyright 2020-2023 Robert Bosch GmbH

.. Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

.. http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License."""

      return sCopyRightRST

   # eof def GetCopyRightRST(self):

   # --------------------------------------------------------------------------------------------------------------

   def GetCopyRightTXT(self):
      """
      """

      sCopyRightTXT = """Copyright 2020-2023 Robert Bosch GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

      return sCopyRightTXT

   # eof def GetCopyRightTXT(self):

   # --------------------------------------------------------------------------------------------------------------

# eof class CCodePatterns():

# **************************************************************************************************************

