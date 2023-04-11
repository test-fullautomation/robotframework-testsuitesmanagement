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
# test_09_VERSION_CONTROL_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 11.04.2023 - 12:17:32
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_VERSION_CONTROL_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'Maximum_version' is invalid (value is not a version number)",]
   )
   def test_TSM_0450(self, Description):
      nReturn = CExecute.Execute("TSM_0450")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'Minimum_version' is invalid (value contains blanks only)",]
   )
   def test_TSM_0451(self, Description):
      nReturn = CExecute.Execute("TSM_0451")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'Minimum_version' is bigger than 'Maximum_version'",]
   )
   def test_TSM_0452(self, Description):
      nReturn = CExecute.Execute("TSM_0452")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'Maximum_version' is smaller than current version",]
   )
   def test_TSM_0453(self, Description):
      nReturn = CExecute.Execute("TSM_0453")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'Minimum_version' is bigger than current version",]
   )
   def test_TSM_0454(self, Description):
      nReturn = CExecute.Execute("TSM_0454")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
