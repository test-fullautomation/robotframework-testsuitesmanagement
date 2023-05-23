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
# test_13_PARAMETER_PRIORITY_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 23.05.2023 - 15:45:58
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_PARAMETER_PRIORITY_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Accordingly to the priority of the enlisted sources all parameters have proper values finally
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Test with several sources of parameters: config file (selected by variant name), local config and variable file",]
   )
   def test_TSM_0900(self, Description):
      nReturn = CExecute.Execute("TSM_0900")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Accordingly to the priority of the enlisted sources all parameters have proper values finally
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Test with several sources of parameters: config file, local config, variable file",]
   )
   def test_TSM_0901(self, Description):
      nReturn = CExecute.Execute("TSM_0901")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Accordingly to the priority of the enlisted sources all parameters have proper values finally
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Test with several sources of parameters: config file (selected by variant name), local config, variable file and single variable in command line",]
   )
   def test_TSM_0902(self, Description):
      nReturn = CExecute.Execute("TSM_0902")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Accordingly to the priority of the enlisted sources all parameters have proper values finally
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Test with several sources of parameters: config file, local config, variable file and single variable in command line",]
   )
   def test_TSM_0903(self, Description):
      nReturn = CExecute.Execute("TSM_0903")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
