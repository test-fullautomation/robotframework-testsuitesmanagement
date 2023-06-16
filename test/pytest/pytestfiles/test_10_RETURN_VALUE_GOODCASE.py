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
# test_10_RETURN_VALUE_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 16.06.2023 - 16:46:18
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_RETURN_VALUE_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Return value of Robot Framework indicates number of FAILED together with number of UNKNOWN tests
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Robot file containing several tests, some PASSED (2), some FAILED (3), some UNKNOWN (4)",]
   )
   def test_TSM_0600(self, Description):
      nReturn = CExecute.Execute("TSM_0600")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Return value of Robot Framework indicates number of FAILED together with number of UNKNOWN tests
   # (Folder execution)
   @pytest.mark.parametrize(
      "Description", ["Folder with several robot files (6) containing several tests, some PASSED (6), some FAILED (6), some UNKNOWN (6)",]
   )
   def test_TSM_0700(self, Description):
      nReturn = CExecute.Execute("TSM_0700")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
