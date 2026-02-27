# **************************************************************************************************************
#  Copyright 2020-2026 Robert Bosch GmbH
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
# test_14_NAMING_CONVENTIONS_GOODCASE.py
#
# 27.02.2026 - 11:47:03
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_NAMING_CONVENTIONS_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Parameters are accepted and their values are logged correctly
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["JSON file containing several valid parameter names",]
   )
   def test_TSM_1300(self, Description):
      nReturn = CExecute.Execute("TSM_1300")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
