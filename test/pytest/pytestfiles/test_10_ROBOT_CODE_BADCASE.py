# **************************************************************************************************************
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
# --------------------------------------------------------------------------------------------------------------
#
# test_10_ROBOT_CODE_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 11.04.2023 - 12:17:32
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_ROBOT_CODE_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed up to position of keyword FAIL; error message; test result is FAIL
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Robot file contains keyword FAIL",]
   )
   def test_TSM_0551(self, Description):
      nReturn = CExecute.Execute("TSM_0551")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed up to position of keyword UNKNOWN; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Robot file contains keyword UNKNOWN",]
   )
   def test_TSM_0552(self, Description):
      nReturn = CExecute.Execute("TSM_0552")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed up to position of keyword call; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Call of not existing keyword in test code of robot file",]
   )
   def test_TSM_0553(self, Description):
      nReturn = CExecute.Execute("TSM_0553")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed up to position of incomplete keyword call; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Incomplete keyword 'FOR' in test code of robot file",]
   )
   def test_TSM_0554(self, Description):
      nReturn = CExecute.Execute("TSM_0554")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed up to position of incomplete keyword call; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Incomplete keyword 'IF/ELSE' in test code of robot file",]
   )
   def test_TSM_0555(self, Description):
      nReturn = CExecute.Execute("TSM_0555")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Import of not existing library in robot file",]
   )
   def test_TSM_0556(self, Description):
      nReturn = CExecute.Execute("TSM_0556")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed up to position of invalid assignment; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Assignment of unknown dictionary key in test code of robot file",]
   )
   def test_TSM_0557(self, Description):
      nReturn = CExecute.Execute("TSM_0557")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed up to position of invalid assignment; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Assignment of known parameter to unknown dictionary subkey in test code of robot file",]
   )
   def test_TSM_0558(self, Description):
      nReturn = CExecute.Execute("TSM_0558")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
