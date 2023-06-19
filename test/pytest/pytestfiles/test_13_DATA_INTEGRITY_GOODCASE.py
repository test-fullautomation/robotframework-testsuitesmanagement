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
# test_13_DATA_INTEGRITY_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 16.06.2023 - 16:46:18
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_DATA_INTEGRITY_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test string is handed over to Robot Framework and printed to log file unchanged
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Test with test string containing several separator characters and blanks",]
   )
   def test_TSM_1000(self, Description):
      nReturn = CExecute.Execute("TSM_1000")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test string is handed over to Robot Framework and printed to log file unchanged (but with masked special characters and escape sequences resolved)
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Test with test string containing more special characters, masked special characters and escape sequences",]
   )
   def test_TSM_1001(self, Description):
      nReturn = CExecute.Execute("TSM_1001")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
