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
# **************************************************************************************************************
#
# tsm-tst-testfile-001.robot
#
# --------------------------------------------------------------------------------------------------------------

*** Settings ***

*** Test Cases ***

Test Case tsm-tst-testfile-001-A
   [documentation]    tsm-tst-testfile-001-A
   Log    teststring_common : ${teststring_common} (tsm-tst-testfile-001.robot [A])      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-tst-testfile-001.robot [A])    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-tst-testfile-001.robot [A])        console=yes

   FAIL

   Log    I must not be executed    console=yes

Test Case tsm-tst-testfile-001-B
   [documentation]    tsm-tst-testfile-001-B
   Log    teststring_common : ${teststring_common} (tsm-tst-testfile-001.robot [B])      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-tst-testfile-001.robot [B])    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-tst-testfile-001.robot [B])        console=yes

   UNKNOWN

   Log    I must not be executed    console=yes

Test Case tsm-tst-testfile-001-C
   [documentation]    tsm-tst-testfile-001-C
   Log    teststring_common : ${teststring_common} (tsm-tst-testfile-001.robot [C])      console=yes
   Log    teststring_variant : ${teststring_variant} (tsm-tst-testfile-001.robot [C])    console=yes
   Log    teststring_bench : ${teststring_bench} (tsm-tst-testfile-001.robot [C])        console=yes
