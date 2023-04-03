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
# test_04_LOCAL_CONFIG_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 03.04.2023 - 13:58:56
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_LOCAL_CONFIG_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["A parameter config file is passed to command line parameter local_config; a variant configuration file is not involved",]
   )
   def test_TSM_0150(self, Description):
      nReturn = CExecute.Execute("TSM_0150")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN; reason: 'variant' and 'local_config' belog to the same feature, therefore only one of them is allowed in command line
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["A parameter config file for variant1 is passed to command line parameter local_config; also variant2 configuration is requested",]
   )
   def test_TSM_0151(self, Description):
      nReturn = CExecute.Execute("TSM_0151")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
