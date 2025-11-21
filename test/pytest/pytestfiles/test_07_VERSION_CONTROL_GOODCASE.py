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
# test_07_VERSION_CONTROL_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 21.11.2025 - 14:11:43
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_VERSION_CONTROL_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'Maximum_version' and 'Minimum_version' not defined",]
   )
   def test_TSM_0400(self, Description):
      nReturn = CExecute.Execute("TSM_0400")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'Maximum_version' initialized with 'None'; 'Minimum_version' initialized with 'null'",]
   )
   def test_TSM_0401(self, Description):
      nReturn = CExecute.Execute("TSM_0401")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Only 'Maximum_version' is defined",]
   )
   def test_TSM_0402(self, Description):
      nReturn = CExecute.Execute("TSM_0402")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Only 'Minimum_version' is defined",]
   )
   def test_TSM_0403(self, Description):
      nReturn = CExecute.Execute("TSM_0403")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'max_version', 'min_version' and 'reference_version' not defined",]
   )
   def test_TSM_0404(self, Description):
      nReturn = CExecute.Execute("TSM_0404")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed, because of the version control is optional
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["'max_version' initialized with 'None'; 'min_version' initialized with 'null'; 'reference_version' not defined",]
   )
   def test_TSM_0405(self, Description):
      nReturn = CExecute.Execute("TSM_0405")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Only 'max_version' is defined",]
   )
   def test_TSM_0406(self, Description):
      nReturn = CExecute.Execute("TSM_0406")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Only 'min_version' is defined",]
   )
   def test_TSM_0407(self, Description):
      nReturn = CExecute.Execute("TSM_0407")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Only 'reference_version' is defined",]
   )
   def test_TSM_0408(self, Description):
      nReturn = CExecute.Execute("TSM_0408")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["All defined: 'min_version', 'max_version' and 'reference_version' (major.minor.patch)",]
   )
   def test_TSM_0409(self, Description):
      nReturn = CExecute.Execute("TSM_0409")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["All defined: 'min_version', 'max_version' and 'reference_version' (major.minor)",]
   )
   def test_TSM_0410(self, Description):
      nReturn = CExecute.Execute("TSM_0410")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["All defined: 'min_version', 'max_version' and 'reference_version' (major)",]
   )
   def test_TSM_0411(self, Description):
      nReturn = CExecute.Execute("TSM_0411")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Both 'min_version' and 'max_version' are defined. Reference is the TestsuitesManagement.",]
   )
   def test_TSM_0412(self, Description):
      nReturn = CExecute.Execute("TSM_0412")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is executed
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Version check with user defined error message",]
   )
   def test_TSM_0413(self, Description):
      nReturn = CExecute.Execute("TSM_0413")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
