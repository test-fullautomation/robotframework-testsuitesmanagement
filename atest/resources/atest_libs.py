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
def subprocess_execution(testscript, args = ''):
    
    curDir = os.getcwd()
    suite_dir = os.path.dirname(BuiltIn().get_variable_value("${SUITE_SOURCE}"))
    os.chdir(suite_dir)
    print('INFO: Executed test - ', os.path.abspath(testscript))
    try:
        if os.name == 'nt':
            if args != '':
                command = '"' + os.environ['RobotPythonPath'] + '/python.exe" -m robot.run ' + args + " " \
                    + os.path.abspath(testscript)
                result = os.popen(command).read()
            else:
                command = '"' + os.environ['RobotPythonPath'] + '/python.exe" -m robot.run ' + os.path.abspath(testscript)
                result = os.popen(command).read()
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

@keyword
def create_valid_default_local_config_file():
    curDir = os.getcwd()
    suite_dir = os.path.dirname(BuiltIn().get_variable_value("${SUITE_SOURCE}"))
    os.chdir(suite_dir)
    os.system("copy " + os.path.abspath("../../general_config/localconfig/local_config_invalid.json") \
        + " " + os.environ['ROBOT_LOCAL_CONFIG'] + "\\local_config.json")

@keyword
def delete_default_local_config_file():
    try:
        os.remove(os.environ['ROBOT_LOCAL_CONFIG'] + "/local_config.json")
    except:
        pass