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
'''
Variable file for the static code analysis of robot files (IntelliSense in the IDE).

The TestsuitesManagement sets ``${CONFIG}`` and all parameters of ``params`` → ``global`` at runtime
(``testsuite_setup``). A static code analysis (e.g. RobotCode) does not know them and reports
"Variable not found". This variable file provides the same variables to the code analysis.

Usage (VS Code ``settings.json``):

.. code:: json

   "robotcode.robot.variableFiles": [
      "RobotFramework_TestsuitesManagement.ide_variables:./config/variants.jsonp:variant1"
   ]

The variables are only returned during the static code analysis. During a test execution the variable file
returns nothing, because variables that exist before ``testsuite_setup`` are not overwritten by the
TestsuitesManagement.
'''

import os
import sys

from JsonPreprocessor import CJsonPreprocessor
from robot.utils.dotdict import DotDict

# Module that is loaded only by RobotCode's code analysis (language server, 'robotcode analyze'),
# not by test executions.
ANALYSIS_MODULE = "robotcode.robot.diagnostics.library_doc"


def is_static_analysis() -> bool:
    '''
Returns ``True`` if the variable file is loaded by a static code analysis (RobotCode).
    '''
    return ANALYSIS_MODULE in sys.modules


def _to_robot(value):
    # same conversion as CConfig.__set_global_variable
    if isinstance(value, dict):
        return DotDict(value)
    if isinstance(value, list):
        return [DotDict(item) if isinstance(item, dict) else item for item in value]
    return value


def load_config(config_file: str, variant: str = "default") -> dict:
    '''
Loads a configuration like the TestsuitesManagement does and returns the variables
``CONFIG`` and all parameters of ``params`` → ``global``.

**Arguments:**

* ``config_file``

   / *Condition*: required / *Type*: str /

   Path to a variant configuration file (configuration level 2) or to a parameter configuration file
   (configuration level 1). Relative paths are relative to the current working directory.

* ``variant``

   / *Condition*: optional / *Type*: str / *Default*: 'default' /

   Name of the variant. Ignored if ``config_file`` is a parameter configuration file.

**Returns:**

* ``variables``

   / *Type*: dict /
    '''
    jpp = CJsonPreprocessor(syntax="python")
    config_file = os.path.abspath(config_file)
    config = jpp.jsonLoad(config_file)

    if "WelcomeString" not in config:
        # variant configuration file
        if variant not in config:
            raise ValueError(f"The variant '{variant}' is not defined in '{config_file}'. "
                             f"Available variants: {', '.join(config.keys())}")
        name = config[variant]['name']
        path = config[variant]['path']
        if path.startswith('.'):
            path = os.path.join(os.path.dirname(config_file), path)
        config = jpp.jsonLoad(os.path.abspath(os.path.join(path, name)))

    params_global = config.get('params', {}).pop('global', {})
    variables = {key: _to_robot(value) for key, value in params_global.items()}
    variables['CONFIG'] = DotDict(config)
    return variables


def _add_nested_keys(name: str, value, variables: dict):
    # makes the keys of dictionaries known as variables 'name.key' (code completion of '${CONFIG.')
    if isinstance(value, dict):
        for key, sub_value in value.items():
            if isinstance(key, str) and key.isidentifier():
                nested_name = f"{name}.{key}"
                variables[nested_name] = _to_robot(sub_value)
                _add_nested_keys(nested_name, sub_value, variables)


def get_variables(config_file: str, variant: str = "default") -> dict:
    '''
Robot Framework variable file interface. Returns the variables of ``load_config()`` during a static code
analysis, otherwise an empty dictionary.

Additionally every key of a dictionary is returned as separate variable in dotdict notation
(e.g. ``CONFIG.Project``), to enable the code completion of ``${CONFIG.`` in the IDE.
    '''
    if not is_static_analysis():
        return {}
    variables = load_config(config_file, variant)
    for name, value in list(variables.items()):
        _add_nested_keys(name, value, variables)
    return variables
