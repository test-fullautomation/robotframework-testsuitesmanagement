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
# test_05_NESTED_CONFIG_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 11.04.2023 - 12:17:32
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_NESTED_CONFIG_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Nested configuration files create new parameters and also overwrite already existing ones. Accordingly to the order of definitions the last definition sets the parameter value.
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Variant with multiple nested configuration files",]
   )
   def test_TSM_0200(self, Description):
      nReturn = CExecute.Execute("TSM_0200")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Inside robot files all configuration parameters have proper value and are of proper data type
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Variant with multiple nested configuration files and extended parameter definitions (new and overwritten values; all relevant data types)",]
   )
   def test_TSM_0201(self, Description):
      nReturn = CExecute.Execute("TSM_0201")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
