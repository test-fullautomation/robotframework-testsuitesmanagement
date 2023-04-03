.. Copyright 2020-2022 Robert Bosch GmbH

.. Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

.. http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Test Use Cases
==============

* **Test TSM_0001**

  [VARIANT_HANDLING / GOODCASE]

   **Without variant configuration file in suite setup of robot file; default config level 4**

   Expected: Execution with config level 4

   *Comment: Single file execution*

----

* **Test TSM_0002**

  [VARIANT_HANDLING / GOODCASE]

   **With variant configuration file in suite setup of robot file; default variant**

   Expected: Execution with default variant

   *Comment: Single file execution*

----

* **Test TSM_0003**

  [VARIANT_HANDLING / GOODCASE]

   **With variant name in command line / (variant1)**

   Expected: Execution with selected variant 1

   *Comment: Single file execution*

----

* **Test TSM_0004**

  [VARIANT_HANDLING / GOODCASE]

   **With variant name in command line / with 4 byte UTF-8 characters inside name**

   Expected: Execution with selected variant

   *Comment: Single file execution*

----

* **Test TSM_0005**

  [VARIANT_HANDLING / GOODCASE]

   **With parameter configuration file in command line / (tsm-test_config_variant2.json)**

   Expected: Execution with selected variant 2

   *Comment: Single file execution*

----

* **Test TSM_0006**

  [VARIANT_HANDLING / GOODCASE]

   **With parameter configuration file in command line / with 4 byte UTF-8 characters inside name**

   Expected: Execution with selected config file for variant

   *Comment: Single file execution*

----

* **Test TSM_0007**

  [VARIANT_HANDLING / GOODCASE]

   **With variant name and single parameter in command line / (variant1; teststring_variant)**

   Expected: Single command line parameter value overwrites variant 1 configuration value

   *Comment: Single file execution*

----

* **Test TSM_0008**

  [VARIANT_HANDLING / GOODCASE]

   **With parameter configuration file and single parameter in command line / (variant2; teststring_variant)**

   Expected: Single command line parameter value overwrites variant 2 configuration value

   *Comment: Single file execution*

----

* **Test TSM_0009**

  [VARIANT_HANDLING / GOODCASE]

   **With parameter configuration file taken from config folder (placed beside the executed robot file); robot file has same name as configuration file**

   Expected: Configuration parameters taken from configuration file with same name as the robot file

   *Comment: Single file execution*

----

* **Test TSM_0010**

  [VARIANT_HANDLING / GOODCASE]

   **With parameter configuration file taken from config folder (placed beside the executed robot file); robot file has another name as configuration file**

   Expected: Configuration parameters taken from configuration file with predefined default name (robot_config.json)

   *Comment: Single file execution*

----

* **Test TSM_0011**

  [VARIANT_HANDLING / GOODCASE]

   **With parameter configuration file taken from config folder (placed beside the executed robot file); robot file has another name as configuration file; single parameter in command line (teststring_variant)**

   Expected: Configuration parameters taken from configuration file with predefined default name (robot_config.json); single command line parameter value overwrites variant 'robot_config' configuration value

   *Comment: Single file execution*

----

* **Test TSM_0050**

  [VARIANT_HANDLING / BADCASE]

   **With missing parameter in parameter configuration file**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0051**

  [VARIANT_HANDLING / BADCASE]

   **With syntax error in parameter configuration file**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0052**

  [VARIANT_HANDLING / BADCASE]

   **With syntax error within imported parameter configuration file**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0053**

  [VARIANT_HANDLING / BADCASE]

   **With not existing imported parameter configuration file**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0054**

  [VARIANT_HANDLING / BADCASE]

   **With not existing imported parameter configuration file**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0055**

  [VARIANT_HANDLING / BADCASE]

   **Command line contains both: variant name and config file**

   Expected: Both together is not accepted; test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0056**

  [VARIANT_HANDLING / BADCASE]

   **Command line contains variant name, but no variant configuration file is given to suite setup**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0057**

  [VARIANT_HANDLING / BADCASE]

   **Command line contains invalid variant name (not allowed characters in variant name)**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0058**

  [VARIANT_HANDLING / BADCASE]

   **Command line contains unknown variant name (a variant with this name is not defined in variant configuration file)**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0059**

  [VARIANT_HANDLING / BADCASE]

   **Command line contains unknown variant configuration file (a file with this name does not exist)**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0060**

  [VARIANT_HANDLING / BADCASE]

   **Robot file refers to a variant configuration file with syntax errors**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0061**

  [VARIANT_HANDLING / BADCASE]

   **Robot file refers to a variant configuration file with not existing parameter file for default variant**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0062**

  [VARIANT_HANDLING / BADCASE]

   **Robot file refers to a variant configuration file with not existing path for variant1**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0063**

  [VARIANT_HANDLING / BADCASE]

   **Robot file refers to a variant configuration file with with missing 'default' variant; a variant name is not given in command line**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0064**

  [VARIANT_HANDLING / BADCASE]

   **A local config file is passed to command line parameter config_file**

   Expected: Test is not executed; error message; test result is UNKNOWN; reason: a local config file is not a full configuration file

   *Comment: Single file execution*

----

* **Test TSM_0100**

  [LOCAL_CONFIG / GOODCASE]

   **With variant1 name and local config file for bench2 given in command line**

   Expected: Local config value overwrites initial value for parameter 'teststring_bench'

   *Comment: Single file execution*

----

* **Test TSM_0101**

  [LOCAL_CONFIG / GOODCASE]

   **With variant2 configuration file and local config file for bench1 given in command line**

   Expected: Local config value overwrites initial value for parameter 'teststring_bench'

   *Comment: Single file execution*

----

* **Test TSM_0102**

  [LOCAL_CONFIG / GOODCASE]

   **With variant2 configuration file, local config file for bench1 and single parameter given in command line**

   Expected: Command line value of 'teststring_bench' overwrites all other definitions (the initial one and the local config one)

   *Comment: Single file execution*

----

* **Test TSM_0103**

  [LOCAL_CONFIG / GOODCASE]

   **With variant1 name given in command line and and local config file for bench2 given by environment variable**

   Expected: Local config value overwrites initial value for parameter 'teststring_bench'

   *Comment: Single file execution*

   *Hint: Temporary change of environment (ROBOT_LOCAL_CONFIG)*

----

* **Test TSM_0150**

  [LOCAL_CONFIG / BADCASE]

   **A parameter config file is passed to command line parameter local_config; a variant configuration file is not involved**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0151**

  [LOCAL_CONFIG / BADCASE]

   **A parameter config file for variant1 is passed to command line parameter local_config; also variant2 configuration is requested**

   Expected: Test is not executed; error message; test result is UNKNOWN; reason: 'variant' and 'local_config' belog to the same feature, therefore only one of them is allowed in command line

   *Comment: Single file execution*

----

* **Test TSM_0200**

  [NESTED_CONFIG / GOODCASE]

   **Variant with multiple nested configuration files**

   Expected: Nested configuration files create new parameters and also overwrite already existing ones. Accordingly to the order of definitions the last definition sets the parameter value.

   *Comment: Single file execution*

----

* **Test TSM_0201**

  [NESTED_CONFIG / GOODCASE]

   **Variant with multiple nested configuration files and extended parameter definitions (new and overwritten values; all relevant data types)**

   Expected: Inside robot files all configuration parameters have proper value and are of proper data type

   *Comment: Single file execution*

----

* **Test TSM_0250**

  [NESTED_CONFIG / BADCASE]

   **Variant with multiple nested configuration files; cyclic import of JSON file**

   Expected: Test is not executed; error message; test result is UNKNOWN; reason: cyclic import

   *Comment: Single file execution*

----

* **Test TSM_0251**

  [NESTED_CONFIG / BADCASE]

   **Assignment of unknown dictionary key in imported JSON configuration file**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0252**

  [NESTED_CONFIG / BADCASE]

   **Assignment of known parameter to unknown dictionary subkey in imported JSON configuration file**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0350**

  [SCHEMA_VALIDATION / BADCASE]

   **Schema file for JSON configuration files is not available**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

   *Hint: Temporary modification of installed schema file*

----

* **Test TSM_0351**

  [SCHEMA_VALIDATION / BADCASE]

   **Schema file for JSON configuration files is invalid because of a syntax error**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0400**

  [VERSION_CONTROL / GOODCASE]

   **'Maximum_version' and 'Minimum_version' not defined**

   Expected: Test is executed, because of the version control is optional

   *Comment: Single file execution*

----

* **Test TSM_0401**

  [VERSION_CONTROL / GOODCASE]

   **'Maximum_version' initialized with 'None', 'Minimum_version' initialized with 'null'**

   Expected: Test is executed, because of the version control is optional

   *Comment: Single file execution*

----

* **Test TSM_0402**

  [VERSION_CONTROL / GOODCASE]

   **Only 'Maximum_version' is defined**

   Expected: Test is executed, because of the version control is optional

   *Comment: Single file execution*

----

* **Test TSM_0403**

  [VERSION_CONTROL / GOODCASE]

   **Only 'Minimum_version' is defined**

   Expected: Test is executed, because of the version control is optional

   *Comment: Single file execution*

----

* **Test TSM_0450**

  [VERSION_CONTROL / BADCASE]

   **'Maximum_version' is invalid (value is not a version number)**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0451**

  [VERSION_CONTROL / BADCASE]

   **'Minimum_version' is invalid (value contains blanks only)**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0452**

  [VERSION_CONTROL / BADCASE]

   **'Minimum_version' is bigger than 'Maximum_version'**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0453**

  [VERSION_CONTROL / BADCASE]

   **'Maximum_version' is smaller than current version**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0454**

  [VERSION_CONTROL / BADCASE]

   **'Minimum_version' is bigger than current version**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0551**

  [ROBOT_CODE / BADCASE]

   **Robot file contains keyword FAIL**

   Expected: Test is executed up to position of keyword FAIL; error message; test result is FAIL

   *Comment: Single file execution*

----

* **Test TSM_0552**

  [ROBOT_CODE / BADCASE]

   **Robot file contains keyword UNKNOWN**

   Expected: Test is executed up to position of keyword UNKNOWN; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0553**

  [ROBOT_CODE / BADCASE]

   **Call of not existing keyword in test code of robot file**

   Expected: Test is executed up to position of keyword call; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0554**

  [ROBOT_CODE / BADCASE]

   **Incomplete keyword 'FOR' in test code of robot file**

   Expected: Test is executed up to position of incomplete keyword call; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0555**

  [ROBOT_CODE / BADCASE]

   **Incomplete keyword 'IF/ELSE' in test code of robot file**

   Expected: Test is executed up to position of incomplete keyword call; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0556**

  [ROBOT_CODE / BADCASE]

   **Import of not existing library in robot file**

   Expected: Test is not executed; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0557**

  [ROBOT_CODE / BADCASE]

   **Assignment of unknown dictionary key in test code of robot file**

   Expected: Test is executed up to position of invalid assignment; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0558**

  [ROBOT_CODE / BADCASE]

   **Assignment of known parameter to unknown dictionary subkey in test code of robot file**

   Expected: Test is executed up to position of invalid assignment; error message; test result is UNKNOWN

   *Comment: Single file execution*

----

* **Test TSM_0600**

  [RETURN_VALUE / GOODCASE]

   **Robot file containing several tests, some PASSED, some FAILED (3), some UNKNOWN (4)**

   Expected: Return value of Robot Framework indicates number of FAILED together with number of UNKNOWN tests

   *Comment: Single file execution*

----

Generated: 03.04.2023 - 18:06:03

