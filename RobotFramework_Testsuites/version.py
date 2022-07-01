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
# *******************************************************************************
#
# File: version.py
#
# Initialy created by Tran Duy Ngoan(RBVH/ECM11) / October 2021
#
# This file provides the method to get the installed Robotframework AIo version
#  
# History:
# 
# 2020-10-25:
#  - initial version
#
# *******************************************************************************

from RobotFramework_Testsuites.Config import VERSION

def robfwaio_version():
   '''
   Return testsuitemanagement version as Robot framework AIO version
   '''
   print(f"{VERSION}")

if __name__=="__main__":
   robfwaio_version()