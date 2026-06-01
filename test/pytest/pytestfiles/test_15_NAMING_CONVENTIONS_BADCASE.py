# **************************************************************************************************************
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
# --------------------------------------------------------------------------------------------------------------
#
# test_15_NAMING_CONVENTIONS_BADCASE.py
#
# 27.02.2026 - 11:47:03
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_NAMING_CONVENTIONS_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is FAIL or UNKNOWN (depending on the Robot Framework core)
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["JSON file containing an invalid parameter name",]
   )
   def test_TSM_1350(self, Description):
      nReturn = CExecute.Execute("TSM_1350")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is FAIL or UNKNOWN (depending on the Robot Framework core)
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["JSON file containing an invalid parameter name",]
   )
   def test_TSM_1351(self, Description):
      nReturn = CExecute.Execute("TSM_1351")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is FAIL or UNKNOWN (depending on the Robot Framework core)
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["JSON file containing an invalid parameter name",]
   )
   def test_TSM_1352(self, Description):
      nReturn = CExecute.Execute("TSM_1352")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
