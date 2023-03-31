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

Component test of RobotFramework_TestsuitesManagement
=====================================================

XC-CT/ECA3-Queckenstedt

31.03.2023

----

Execution
---------

The component test is executed by the main test script ``component_test.py``.

This script executes a bunch of test cases that are configured in

.. code::

   testconfig/TestConfig.py

The executed robot test files together with the JSON configuration files are placed in folder

.. code::

   testcases

The log files of the test execution can be found in folder

.. code::

   testlogfiles

  Caution:
  The complete log files folder testlogfiles will be deleted at the beginning of every component test execution.
  Do not place any manually generated content here.

Per default all test cases defined in ``TestConfig.py``, are executed. Alternatively a single test case can
be choosed for execution by providing the test id (``TESTID``) in command line in the following way:

.. code::

   component_test.py --testid="<TESTID>"

The ``TESTID`` is part of the test case configuration in ``TestConfig.py``.

Another possibility is available to execute the component test (under pytest conditions). This is
described in one of the next parts of this readme.

----

Test case results
-----------------

The result of a single test case depends on the return value of the Robot Framework (like defined
in ``TestConfig.py``) and on the result of a log file comparison.
If both is passed, the result of the test case is ``PASSED``. Otherwise: In case of internal errors
the result of the test case is ``UNKNOWN``, in case of the return value is not like expected or in case
of any deviation between the current test log files and the reference log files, the result of the
test case is ``FAILED``.

The return value of ``component_test.py`` is 0 in case of all test cases are ``PASSED`` (and no internal
errors happened), otherwise 1.

----

Naming conventions
------------------

The configuration of a test case includes (beneath others) a ``TESTID``, a ``SECTION`` and a ``SUBSECTION`` (see
``TestConfig.py``).

The ``TESTID`` is a unique identifier for a test case and consists of a component specific prefix (to make
these id's much more unique also over all tested components) and a number. ``SECTION`` and ``SUBSECTION`` are
labels that are used to give a test case a more meaningful name. ``SECTION`` contains the name of the tested
feature; ``SUBSECTION`` is used to indicate a GOODCASE or a BADCASE test.

TESTID, ``SECTION`` and ``SUBSECTION`` are used together to define the names of test cases, log file folders and
log files.

Example: The test case name of a good case test of the variant handling with ``TESTID`` ``TSM_0001`` is:

.. code::

   TSM_0001-(VARIANT_HANDLING)-[GOODCASE]

With: 

* ``TSM_0001``" is the ``TESTID``
* ``VARIANT_HANDLING`` is the ``SECTION`` (*to ease the readability the* ``SECTION`` *is encapsulated in round brackets*)
* ``GOODCASE`` is the ``SUBSECTION`` (*to ease the readability the* ``SUBSECTION`` *is encapsulated in edged brackets*)

The log files of this test case are placed within a folder with the same name.

To ensure an unique look&feel of all names, the content of ``SECTION`` and ``SUBSECTION`` should be written in
capital letters only (with the underline as separator character).

----

Log file comparison
-------------------

Current log files are compared with reference log files, that are log files from previous executions.
The user has to check them manually. In case of the user decides that the content of the log file is
like expected and shall be used as reference, the file has to be stored within the folder

.. code::

   referencelogfiles

under the same name (and within the same sub folder).

The log file comparison considers the debug log file in text format and the XML log file.

Example:

* Current log files:

  .. code::

     testlogfiles/TSM_0001-(VARIANT_HANDLING)-[GOODCASE]/TSM_0001-(VARIANT_HANDLING)-[GOODCASE].log
     testlogfiles/TSM_0001-(VARIANT_HANDLING)-[GOODCASE]/TSM_0001-(VARIANT_HANDLING)-[GOODCASE].xml

* Reference log files:

  .. code::

     referencelogfiles/TSM_0001-(VARIANT_HANDLING)-[GOODCASE]/TSM_0001-(VARIANT_HANDLING)-[GOODCASE].log
     referencelogfiles/TSM_0001-(VARIANT_HANDLING)-[GOODCASE]/TSM_0001-(VARIANT_HANDLING)-[GOODCASE].xml

The comparison is based on a set of regular expressions, that are used to create a subset of the log files content.
And these subsets are compared (not the entire log files itself). This is to ensure that irrelevant content like
timestamps or operating system dependent path separators do not harm the results.

The regular expressions are defined in the following pattern files: 

.. code::

   testconfig/tsm_test_pattern_TXT.txt
   testconfig/tsm_test_pattern_XML.txt

The log file comparison can be switched off. This is useful to save time during the development of new test cases
and in case of a valid reference log file is not available yet.

Option 1: The log file comparison for all test cases defined in ``TestConfig.py`` can be switched off in command line of
``component_test.py`` with

.. code::

   --skiplogcompare.

Option 2: The log file comparison for a single test case only can be switched off in ``TestConfig.py`` (where this test case
is defined) with the optional

.. code::

   dictUsecase['LOGCOMPARE'] = False

as part of the definition.

----

Web application support
-----------------------

Test results can be shown on a database supported web page. The software that is required to enable this, can be found here:

.. code::

   https://github.com/test-fullautomation/testresultwebapp
   https://github.com/test-fullautomation/python-pytestlog2db (pytestlog2db.py)
   https://github.com/test-fullautomation/robotframework-robotlog2db (robotlog2db.py)

The ``testresultwebapp`` provides the web page (a so called dashboard displaying the results), ``pytestlog2db.py`` writes test results
created from Python pytest module into the database and ``robotlog2db.py`` writes test results created from Robot Framework
into the database. Both ``2db`` applications work with the result log files in XML format (like generated by pytest and Robot Framework).

This component test executes test files of the Robot Framework. First results are therefore available in XML result file format
of the Robot Framework. The problem now is: We cannot let ``robotlog2db.py`` write the results in these XML files to a database
immediately - because the decision if a test case was successful or not, is not made inside these log files. This decision is made
one level higher (within the component test script ``component_test.py``).

Therefore we need a possibility to create a new XML result file that contain the results of this component test and can be computed
by one of the ``2db`` applications.

This is realized in the following way:

With the command line option

.. code::

   --codedump

``component_test.py`` creates for every combination of ``SECTION`` and ``SUBSECTION`` a pytest file containing all test cases belonging to this
combination. Every test case inside these pytest files does nothing else than calling ``component_test.py`` with the test id of this test case.
Therefore the same code is executed, but because of the Python pytest module is involved now, we have an XML result log file in
pytest format available. And this XML file can be computed by ``pytestlog2db.py``.

All automatically generated pytest code files can be found here:

.. code::

   pytest/pytestfiles

To execute these files this script can be used:

.. code::

   pytest/executepytest.py

Example

Call of a single test case in command line:

.. code::

   component_test.py --testid="TSM_00001"

Corresponding pytest file containing the call of this test:

.. code::

   pytest/pytestfiles/test_01_VARIANT_HANDLING_GOODCASE.py

Class name inside the pytest file containing the call of this test:

.. code::

   class Test_VARIANT_HANDLING_GOODCASE:

The test code itself:

.. code::

   def test_TSM_0001(self, Description):
      nReturn = CExecute.Execute("TSM_0001")
      assert nReturn == 0

The pytest XML log file can be found here:

.. code::

   pytest/logfiles/PyTestLog.xml

----

Test case documentation
-----------------------

The configuration of every test case inside ``TestConfig.py`` includes a description and an expectation.

**Example**

.. code::

   dictUsecase['DESCRIPTION'] = "Without variant configuration file in suite setup of robot file; default config level 4"
   dictUsecase['EXPECTATION'] = "Execution with config level 4"

The content is printed to console during every component test execution.

Additionally to this the command line option ``--codedump`` also generates out of all test case configurations several
test case overview lists in the following formats:

.. code::

   TSM_TestUsecases.csv
   TSM_TestUsecases.html
   TSM_TestUsecases.rst
   TSM_TestUsecases.txt

----

Advanced features: PRESTEP and POSTSTEP
---------------------------------------

It might be required to do some certain things before a test case is executed and also after the execution.

For example a test case requires an environment variable. This environment variable has to be created before the execution
and to be removed afterthe execution.

For every additional step a separate function is required that has to be implemented in

.. code::

   libs/CAdditionalSteps.py

Inside ``TestConfig.py`` where all test acses are configured, the execution of these additional steps can be triggered in this way:

dictUsecase['PRESTEP']  = "LocalConfigEnvVar_Create"
dictUsecase['POSTSTEP'] = "LocalConfigEnvVar_Delete"

With ``LocalConfigEnvVar_Create`` and ``LocalConfigEnvVar_Delete`` are the function names.

The usage of ``PRESTEP`` and ``POSTSTEP`` is optional.

