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


from robot.api import logger
from robot.errors import DataError
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import is_string
from robot.utils.importer import Importer

from robotlibcore import DynamicCore
from enum import Enum
from RobotFramework_TestsuitesManagement.Utils import LibListener
from RobotFramework_TestsuitesManagement.Keywords import (CSetupKeywords, CGeneralKeywords)
from RobotFramework_TestsuitesManagement.Config import BUNDLE_VERSION as VERSION


class RobotFramework_TestsuitesManagement(DynamicCore):
    # '''
    # **Class: RobotFramework_TestsuitesManagement**

       # RobotFramework_TestsuitesManagement is the Bosch testing library for Robot Framework.

       # RobotFramework_TestsuitesManagement control peripheral devices, tools and target under testing.
    # '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    # '''
    # Constructor
    # Args:
        # None
    # Returns:
        # None
    # '''
    def __init__(self, timeout=10.0):
        self.timeout = timeout
        self._running_on_failure_keyword = False
        self.run_on_failure_keyword = None # will update later
        libraries = [CSetupKeywords(), CGeneralKeywords()]
        self.ROBOT_LIBRARY_LISTENER = LibListener()
        self._running_keyword = None
        DynamicCore.__init__(self, libraries)

    # '''
    # Method: run_keyword
    # Args:
        # name: string
    # Returns:
        # DynamicCore.run_keyword
    # '''
    def run_keyword(self, name, args, kwargs):
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except Exception:
            self.failure_occurred()
            raise

    # '''
    # Method: get_keyword_tags
    # Args:
        # name: String
    # Returns:
        # tags
    # '''
    def get_keyword_tags(self, name):
        tags = list(DynamicCore.get_keyword_tags(self, name))
        return tags

    # '''
    # Method: get_keyword_documentation
    # Args:
        # name: string
    # Returns:
        # DynamicCore.get_keyword_documentation
    # '''
    def get_keyword_documentation(self, name):
        return DynamicCore.get_keyword_documentation(self, name)

    # '''
    # Method: failure_occurred is executed when RobotFramework_TestsuitesManagement keyword fails.
    # By default, executes the registered run-on-failure keyword. RobotFramework_TestsuitesManagement can
    # overwrite this hook method in case provides custom functionality instead.
    # Args:
        # None
    # Returns:
        # None
    # '''
    def failure_occurred(self):
        if self._running_on_failure_keyword or not self.run_on_failure_keyword:
            return None
        try:
            self._running_on_failure_keyword = True
            BuiltIn().run_keyword(self.run_on_failure_keyword)
        except Exception as error:
            logger.warn(f"Keyword '{self.run_on_failure_keyword}' could not be run on failure: '{error}'")
        finally:
            self._running_on_failure_keyword = False

class CConfigLevel(Enum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4

class CTestsuitesCfg():
    oConfig = None

    def __init__(self):
        pass
