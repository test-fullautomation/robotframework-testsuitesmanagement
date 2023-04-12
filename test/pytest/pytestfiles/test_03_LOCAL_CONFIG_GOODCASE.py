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
# test_03_LOCAL_CONFIG_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 12.04.2023 - 11:05:17
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_LOCAL_CONFIG_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Local config value overwrites initial value for parameter 'teststring_bench'
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With variant1 name and local config file for bench2 given in command line",]
   )
   def test_TSM_0100(self, Description):
      nReturn = CExecute.Execute("TSM_0100")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Local config value overwrites initial value for parameter 'teststring_bench'
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With variant2 configuration file and local config file for bench1 given in command line",]
   )
   def test_TSM_0101(self, Description):
      nReturn = CExecute.Execute("TSM_0101")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Command line value of 'teststring_bench' overwrites all other definitions (the initial one and the local config one)
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With variant2 configuration file, local config file for bench1 and single parameter given in command line",]
   )
   def test_TSM_0102(self, Description):
      nReturn = CExecute.Execute("TSM_0102")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Local config value overwrites initial value for parameter 'teststring_bench'
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With variant1 name given in command line and and local config file for bench2 given by environment variable",]
   )
   def test_TSM_0103(self, Description):
      nReturn = CExecute.Execute("TSM_0103")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
