# **************************************************************************************************************
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
# test_15_COMPOSITE_EXPRESSIONS_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 06.10.2023 - 10:11:21
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_COMPOSITE_EXPRESSIONS_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Resulting strings available during test execution
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["JSON file containing several string concatenations in separate lines",]
   )
   def test_TSM_1200(self, Description):
      nReturn = CExecute.Execute("TSM_1200")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
