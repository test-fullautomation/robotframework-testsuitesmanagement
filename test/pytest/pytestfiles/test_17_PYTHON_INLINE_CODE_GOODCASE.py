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
# test_17_PYTHON_INLINE_CODE_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 18.08.2025 - 14:49:11
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_PYTHON_INLINE_CODE_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Python inline code is resolved and the results are logged correctly
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["JSON file containing Python inline code",]
   )
   def test_TSM_1500(self, Description):
      nReturn = CExecute.Execute("TSM_1500")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
