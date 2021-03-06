#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
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
import os
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger

@keyword
def subprocess_execution(testscript):
    
    curDir = os.getcwd()
    suite_dir = os.path.dirname(BuiltIn().get_variable_value("${SUITE_SOURCE}"))
    os.chdir(suite_dir)
    print('INFO: Executed test - ', os.path.abspath(testscript))
    try:
        if os.name == 'nt':
            result = os.popen(os.path.abspath(testscript)).read()
        else:
            result = os.popen('robot ' + os.path.abspath(testscript)).read()
    except:
        pass
    
    if '| PASS |' in result:
        logger.info(result)
        os.chdir(curDir)
        return "Passed"
    else:
        logger.info(result)
        os.chdir(curDir)
        return "Failed"
