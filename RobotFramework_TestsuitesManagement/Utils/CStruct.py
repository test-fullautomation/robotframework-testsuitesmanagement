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
#################################################################################
#
# File: CStruct.py
# Initially created by Mai Dinh Nam Son (RBVH/ECM11) / Dec-2020
# Base on file lib\Misc\CStruct.py of TML Framework (Author: Pollerspoeck Thomas)
#
#
#################################################################################

# '''
# This class provides the "struct" functionality of "C/C++" in python.
# It simply helps to organize data which belongs logically together.

# Usage: oStruct=CStruct(attribute_1=value_1, ... attribute_n=value_n)
       # oStruct.attribute_1="....."
# '''

class CStruct:
    '''
This ``CStruct`` class creates the given attributes dynamically at runtime.
    '''

    def __init__(self, *args, **kwargs):
        '''
The constructor __init__ creates the given attributes dynamically at runtime.

**Arguments:**

Attributes to be created with the initial value.

**Returns:**

Accessible attributes.
        '''
        for k, v in kwargs.items():
            setattr(self, k, v)
