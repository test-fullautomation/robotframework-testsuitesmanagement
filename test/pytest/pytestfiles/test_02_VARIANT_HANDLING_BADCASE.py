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
# test_02_VARIANT_HANDLING_BADCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 23.05.2023 - 15:45:58
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_VARIANT_HANDLING_BADCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With missing parameter in parameter configuration file",]
   )
   def test_TSM_0050(self, Description):
      nReturn = CExecute.Execute("TSM_0050")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With syntax error in parameter configuration file",]
   )
   def test_TSM_0051(self, Description):
      nReturn = CExecute.Execute("TSM_0051")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With syntax error within imported parameter configuration file",]
   )
   def test_TSM_0052(self, Description):
      nReturn = CExecute.Execute("TSM_0052")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With not existing imported parameter configuration file",]
   )
   def test_TSM_0053(self, Description):
      nReturn = CExecute.Execute("TSM_0053")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With not existing imported parameter configuration file",]
   )
   def test_TSM_0054(self, Description):
      nReturn = CExecute.Execute("TSM_0054")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Both together is not accepted; test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Command line contains both: variant name and config file",]
   )
   def test_TSM_0055(self, Description):
      nReturn = CExecute.Execute("TSM_0055")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Command line contains variant name, but no variant configuration file is given to suite setup",]
   )
   def test_TSM_0056(self, Description):
      nReturn = CExecute.Execute("TSM_0056")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Command line contains invalid variant name (not allowed characters in variant name)",]
   )
   def test_TSM_0057(self, Description):
      nReturn = CExecute.Execute("TSM_0057")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Command line contains unknown variant name (a variant with this name is not defined in variant configuration file)",]
   )
   def test_TSM_0058(self, Description):
      nReturn = CExecute.Execute("TSM_0058")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Command line contains unknown variant configuration file (a file with this name does not exist)",]
   )
   def test_TSM_0059(self, Description):
      nReturn = CExecute.Execute("TSM_0059")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Robot file refers to a variant configuration file with syntax errors",]
   )
   def test_TSM_0060(self, Description):
      nReturn = CExecute.Execute("TSM_0060")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Robot file refers to a variant configuration file with not existing parameter file for default variant",]
   )
   def test_TSM_0061(self, Description):
      nReturn = CExecute.Execute("TSM_0061")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Robot file refers to a variant configuration file with not existing path for variant1",]
   )
   def test_TSM_0062(self, Description):
      nReturn = CExecute.Execute("TSM_0062")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Robot file refers to a variant configuration file with with missing 'default' variant; a variant name is not given in command line",]
   )
   def test_TSM_0063(self, Description):
      nReturn = CExecute.Execute("TSM_0063")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN; reason: a local config file is not a full configuration file
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["A local config file is passed to command line parameter config_file",]
   )
   def test_TSM_0064(self, Description):
      nReturn = CExecute.Execute("TSM_0064")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With parameter configuration file taken from config folder (placed beside the executed robot file); robot file has same name as configuration file, but configuration file exists twice: json/jsonp",]
   )
   def test_TSM_0065(self, Description):
      nReturn = CExecute.Execute("TSM_0065")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Test is not executed; error message; test result is UNKNOWN
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With parameter configuration file taken from config folder (placed beside the executed robot file); robot file has another name as configuration file, but configuration file with default name exists twice: json/jsonp",]
   )
   def test_TSM_0066(self, Description):
      nReturn = CExecute.Execute("TSM_0066")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
