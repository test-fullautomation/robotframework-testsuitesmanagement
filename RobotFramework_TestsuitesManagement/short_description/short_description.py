# --------------------------------------------------------------------------------------------------------------
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
# --------------------------------------------------------------------------------------------------------------
#
# The content of the docstrings in this file is intended to support the Robot Framework
# component libdoc. The goal is to provide a brief summary of the most important features
# of RobotFramework_TestsuitesManagement in the documentation format commonly used in Robot Framework.
#
# To avoid redundancies in the main documentation in PDF format, this file is excluded
# from processing by GenPackageDoc by:
#
# "EXCLUDE"        : ["short_description"]
#
# (see packagedoc_config.json)
#
# --------------------------------------------------------------------------------------------------------------

import ast
import inspect

from robot.api.deco import library
from robot.api.deco import keyword

@library
class short_description:

    @keyword
    def get_short_description(self):
        r"""
**Meaning of "Test Suites Management"**

In the scope of the **Robot Framework** a test suite is either a single robot file containing one or more test cases, or a set of several robot files.

Usually all test cases of a test suite run under the same conditions - but these conditions may be different. For example the same test case is used
to test several different variants of a system under test. Every variant requires individual values for certain configuration parameters.

Tests are carried out at several test benches. All test benches have different hardware configurations.
Also the different test benches may require individual values for configuration parameters used in the tests.

**Therefore the same tests have to run under different conditions!**

The **Robot Framework** provides several places to define parameters: robot files, resource files, parameter files. But these parameters
are fixed. Therefore we need a more dynamic way of accessing parameters. And we postulate the following: When switching between
tests of several variants and test executions on several test benches, no changes shall be required within the test code.

The outcome is that another position has to be introduced to store values for variant and test bench specific parameters.
And a possibility has to be provided to dynamically make either the one or the other set of values available during the execution of
tests - depending on outer circumstances like "*which variant?*" and "*which test bench?*".
Those dynamic configuration values are stored within separate configuration files in JSON format and the **TestsuitesManagement** makes the values
available globally during the test execution.

**Examples**

To activate the test suites management you have to import the **RobotFramework_TestsuitesManagement** library in the following way:

.. code:: python

   Library    RobotFramework_TestsuitesManagement    AS    tm

The next step is to call the ``testsuite_setup`` of the **RobotFramework_TestsuitesManagement** within the ``Suite Setup`` of your test:

.. code:: python

   Suite Setup    tm.testsuite_setup

In case you want to realize a variant handling you have to provide the path and the name of a variants configuration file to the ``testsuite_setup``:

.. code:: python

   Suite Setup    tm.testsuite_setup    .../config/exercise_variants.jsonp

The configuration files for the **RobotFramework_TestsuitesManagement** are explained in detail here:
`Tutorial: Building test suites <https://htmlpreview.github.io/?https://github.com/test-fullautomation/robotframework-tutorial/blob/develop/900_building_testsuites/building_testsuites.html#how-does-the-content-of-configuration-files-in-json-format-look-like>`_

**Package Documentation**

Details about how to install the component with PIP, can be found in the `README <https://github.com/test-fullautomation/robotframework-testsuitesmanagement/blob/develop/README.rst>`_

A detailed documentation of the **RobotFramework_TestsuitesManagement** can be found here:
`RobotFramework_TestsuitesManagement.pdf <https://github.com/test-fullautomation/robotframework-testsuitesmanagement/blob/develop/RobotFramework_TestsuitesManagement/RobotFramework_TestsuitesManagement.pdf>`_

For self-study also a tutorial is available containing lots of examples.
Here you find the rendered `tutorial documentation <https://htmlpreview.github.io/?https://github.com/test-fullautomation/robotframework-tutorial/blob/develop/900_building_testsuites/building_testsuites.html>`_.
        """
        # return the docstring above
        source = inspect.getsource(get_short_description)
        module = ast.parse(source)
        func_def = module.body[0]
        return ast.get_docstring(func_def)

