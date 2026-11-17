#  Copyright 2020-2026 Robert Bosch GmbH
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


from robotlibcore import DynamicCore
from enum import Enum
from RobotFramework_TestsuitesManagement.Utils import LibListener
from RobotFramework_TestsuitesManagement.Keywords import (CSetupKeywords, CGeneralKeywords)
from RobotFramework_TestsuitesManagement.version import VERSION as LIBRARY_VERSION


class RobotFramework_TestsuitesManagement(DynamicCore):
    '''
The **RobotFramework_TestsuitesManagement** enables users to define dynamic configuration values within 
separate configuration files in JSONP format.

Details about how to install can be found in the
`README.rst <https://github.com/test-fullautomation/robotframework-testsuitesmanagement/blob/develop/README.rst>`_
    '''
    ROBOT_LIBRARY_DOC_FORMAT = 'reST'
    ROBOT_LIBRARY_SCOPE      = 'GLOBAL'
    ROBOT_LIBRARY_VERSION    = LIBRARY_VERSION

    def __init__(self, timeout=10.0):
        self.timeout = timeout
        libraries = [CSetupKeywords(), CGeneralKeywords()]
        self.ROBOT_LIBRARY_LISTENER = LibListener()
        DynamicCore.__init__(self, libraries)

class CConfigLevel(Enum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4

class CTestsuitesCfg():
    config_obj = None
