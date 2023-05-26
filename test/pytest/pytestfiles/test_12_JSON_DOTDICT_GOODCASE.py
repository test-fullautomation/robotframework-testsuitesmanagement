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
# test_12_JSON_DOTDICT_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 23.05.2023 - 15:45:58
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_JSON_DOTDICT_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: dotdict syntax in JSON files is possible
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Nested imports of JSON files with dotdict syntax",]
   )
   def test_TSM_0800(self, Description):
      nReturn = CExecute.Execute("TSM_0800")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
