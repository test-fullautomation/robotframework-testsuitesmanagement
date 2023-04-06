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
# test_07_SCHEMA_VALIDATION_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 06.04.2023 - 14:44:14
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_SCHEMA_VALIDATION_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Schema file for JSON configuration files is not available",]
   )
   def test_TSM_0350(self, Description):
      nReturn = CExecute.Execute("TSM_0350")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Schema file for JSON configuration files is invalid because of a syntax error",]
   )
   def test_TSM_0351(self, Description):
      nReturn = CExecute.Execute("TSM_0351")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
