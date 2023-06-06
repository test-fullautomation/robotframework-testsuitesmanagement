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
# test_05_NESTED_CONFIG_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 06.06.2023 - 15:28:29
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_NESTED_CONFIG_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN; reason: cyclic import
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Variant with multiple nested configuration files; cyclic import of JSON file",]
   )
   def test_TSM_0250(self, Description):
      nReturn = CExecute.Execute("TSM_0250")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Assignment of unknown dictionary key in imported JSON configuration file",]
   )
   def test_TSM_0251(self, Description):
      nReturn = CExecute.Execute("TSM_0251")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Assignment of known parameter to unknown dictionary subkey in imported JSON configuration file",]
   )
   def test_TSM_0252(self, Description):
      nReturn = CExecute.Execute("TSM_0252")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
