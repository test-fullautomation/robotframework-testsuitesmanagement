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
# test_14_IMPLICIT_CREATION_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 14.09.2023 - 13:10:37
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_IMPLICIT_CREATION_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Missing subkeys are created (implicit creation of data structures)
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Assignment of known parameter to unknown dictionary subkeys in imported JSON configuration file",]
   )
   def test_TSM_1100(self, Description):
      nReturn = CExecute.Execute("TSM_1100")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
