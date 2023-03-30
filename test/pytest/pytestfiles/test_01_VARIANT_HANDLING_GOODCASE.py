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
# test_01_VARIANT_HANDLING_GOODCASE.py
#
# XC-CT/ECA3-Queckenstedt
#
# 30.03.2023 - 13:46:50
#
# --------------------------------------------------------------------------------------------------------------

import pytest
from pytestlibs.CExecute import CExecute

# --------------------------------------------------------------------------------------------------------------

class Test_VARIANT_HANDLING_GOODCASE:

# --------------------------------------------------------------------------------------------------------------
   # Expected: Execution with config level 4
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["Without variant configuration file in suite setup of robot file; default config level 4",]
   )
   def test_TSM_0001(self, Description):
      nReturn = CExecute.Execute("TSM_0001")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Execution with default variant
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With variant configuration file in suite setup of robot file; default variant",]
   )
   def test_TSM_0002(self, Description):
      nReturn = CExecute.Execute("TSM_0002")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Execution with selected variant 1
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With variant name in command line / (variant1)",]
   )
   def test_TSM_0003(self, Description):
      nReturn = CExecute.Execute("TSM_0003")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Execution with selected variant
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With variant name in command line / with 4 byte UTF-8 characters inside name",]
   )
   def test_TSM_0004(self, Description):
      nReturn = CExecute.Execute("TSM_0004")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Execution with selected variant 2
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With parameter configuration file in command line / (tsm-test_config_variant2.json)",]
   )
   def test_TSM_0005(self, Description):
      nReturn = CExecute.Execute("TSM_0005")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Execution with selected config file for variant
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With parameter configuration file in command line / with 4 byte UTF-8 characters inside name",]
   )
   def test_TSM_0006(self, Description):
      nReturn = CExecute.Execute("TSM_0006")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Single command line parameter value overwrites variant 1 configuration value
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With variant name and single parameter in command line / (variant1; teststring_variant)",]
   )
   def test_TSM_0007(self, Description):
      nReturn = CExecute.Execute("TSM_0007")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Single command line parameter value overwrites variant 2 configuration value
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With parameter configuration file and single parameter in command line / (variant2; teststring_variant)",]
   )
   def test_TSM_0008(self, Description):
      nReturn = CExecute.Execute("TSM_0008")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Configuration parameters taken from configuration file with same name as the robot file
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With parameter configuration file taken from local config folder; robot file has same name as configuration file",]
   )
   def test_TSM_0009(self, Description):
      nReturn = CExecute.Execute("TSM_0009")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
   # Expected: Configuration parameters taken from configuration file with predefined default name (robot_config.json)
   # (Single file execution)
   @pytest.mark.parametrize(
      "Description", ["With parameter configuration file taken from local config folder; robot file has another name as configuration file",]
   )
   def test_TSM_0010(self, Description):
      nReturn = CExecute.Execute("TSM_0010")
      assert nReturn == 0
# --------------------------------------------------------------------------------------------------------------
