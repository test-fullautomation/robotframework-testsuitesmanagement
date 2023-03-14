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

.. 14.03.2023

Test Use Cases
==============

* **Test TSM_0001**

  [VARIANT_HANDLING / GOODCASE]

   **No variant configuration; default config level 4**

   Expected: Execution with config level 4

  (*Single file execution*)

----

* **Test TSM_0002**

  [VARIANT_HANDLING / GOODCASE]

   **With variant configuration; default variant**

   Expected: Execution with default variant

  (*Single file execution*)

----

* **Test TSM_0003**

  [VARIANT_HANDLING / GOODCASE]

   **With variant name in command line / (variant1)**

   Expected: Execution with selected variant 1

  (*Single file execution*)

----

* **Test TSM_0004**

  [VARIANT_HANDLING / GOODCASE]

   **With variant name in command line / with 4 byte UTF-8 characters inside name**

   Expected: Execution with selected variant

  (*Single file execution*)

----

* **Test TSM_0005**

  [VARIANT_HANDLING / GOODCASE]

   **With variant file in command line / (tsm-test_config_variant2.json)**

   Expected: Execution with selected variant 2

  (*Single file execution*)

----

* **Test TSM_0006**

  [VARIANT_HANDLING / GOODCASE]

   **With variant file in command line / with 4 byte UTF-8 characters inside name**

   Expected: Execution with selected config file for variant

  (*Single file execution*)

----

* **Test TSM_0007**

  [VARIANT_HANDLING / GOODCASE]

   **With variant name and single parameter in command line / (variant1; teststring_variant)**

   Expected: Single command line parameter value overwrites variant 1 configuration value

  (*Single file execution*)

----

* **Test TSM_0008**

  [COMMAND_LINE / BADCASE]

   **Both given: variant name and config file**

   Expected: Both together is not accepted; error message; test result UNKNOWN

  (*Single file execution*)

----

Updated: 14.03.2023 - 13:48:49

