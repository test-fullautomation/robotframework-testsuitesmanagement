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
# test_08_VERSION_CONTROL_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 24.03.2023 - 16:32:46
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_VERSION_CONTROL_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'Maximum_version' and 'Minimum_version' not defined",]
   )
   def test_TSM_0400(self, Description):
      nReturn = CExecute.Execute("TSM_0400")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'Maximum_version' initialized with 'None', 'Minimum_version' initialized with 'null'",]
   )
   def test_TSM_0401(self, Description):
      nReturn = CExecute.Execute("TSM_0401")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Only 'Maximum_version' is defined",]
   )
   def test_TSM_0402(self, Description):
      nReturn = CExecute.Execute("TSM_0402")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Only 'Minimum_version' is defined",]
   )
   def test_TSM_0403(self, Description):
      nReturn = CExecute.Execute("TSM_0403")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
