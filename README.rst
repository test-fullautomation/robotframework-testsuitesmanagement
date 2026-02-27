.. Copyright 2020-2026 Robert Bosch GmbH

.. Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

.. http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Package Description
===================

**RobotFramework_TestsuitesManagement** allows users to define dynamic configuration values in separate JSON configuration files.

These configuration values are accessible during test execution, but only under conditions specified by the user (e.g., for variant handling).
This means that not all parameter values are available during test execution - only those relevant to the current test scenario.

To achieve this, **RobotFramework_TestsuitesManagement** offers the following features:

* Splits all possible configuration values into multiple JSON configuration files, with each file containing a specific set of configuration parameters.
* Supports nested imports of JSON configuration files.
* Subsequent definitions in configuration files overwrite previous definitions of the same parameter.
* Provides various criteria for selecting which JSON configuration file Robot Framework should use during test execution.

How to install
--------------

The **RobotFramework_TestsuitesManagement** can be installed in two different ways.

1. Installation via PyPi (recommended for users)

   .. code::

      pip install RobotFramework_TestsuitesManagement

   `RobotFramework_TestsuitesManagement in PyPi <https://pypi.org/project/robotframework-testsuitesmanagement/>`_

2. Installation via GitHub (recommended for developers)

   * Clone the **robotframework-testsuitesmanagement** repository to your machine

     .. code::

        git clone https://github.com/test-fullautomation/robotframework-testsuitesmanagement.git

     `RobotFramework_TestsuitesManagement in GitHub <https://github.com/test-fullautomation/robotframework-testsuitesmanagement>`_

   * Use the following command to install **RobotFramework_TestsuitesManagement** (executed in repository main folder):

     .. code::

        python -m pip install .

     Or:

     .. code::

        python -m pip install --proxy <proxy> .

     This command will also download and install all dependencies that are required to work with the source files in the current repository.
     After the initial installation of **RobotFramework_TestsuitesManagement** is done, you have the following two possibilities:

     1. *Clean the previous installation*:

        .. code::

           python "./cleanup_installation.py"

        ``cleanup_installation.py`` explicitly deletes all files and folders within the component installation folder under
        ``site-packages`` and also deletes local build artefacts.

     2. *Render the component documentation*:

        .. code::

           python "./genpackagedoc.py"

        This would e.g. be required in case of changes in the interface of **RobotFramework_TestsuitesManagement**.

        The documentation is rendered by a separate application called **GenPackageDoc**, that is part
        of the build dependencies and runtime dependencies of **RobotFramework_TestsuitesManagement**.

        **GenPackageDoc** needs to be configured. Details about how to do this, can be found in the
        `README.rst <https://github.com/test-fullautomation/python-genpackagedoc/blob/develop/README.rst>`_
        (sections *Install dependencies* and *Configure dependencies*).

   * Use the following command to build **RobotFramework_TestsuitesManagement** (executed in repository main folder):

     .. code::

        python -m build .

     Or:

     .. code::

        python -m pip config set global.proxy <proxy>
        python -m build .


Package Documentation
---------------------

A detailed documentation of the **RobotFramework_TestsuitesManagement** can be found here:
`RobotFramework_TestsuitesManagement.pdf <https://github.com/test-fullautomation/robotframework-testsuitesmanagement/blob/develop/RobotFramework_TestsuitesManagement/RobotFramework_TestsuitesManagement.pdf>`_

For self-study also a tutorial is available containing lots of examples.
Here you find the rendered `tutorial documentation <https://htmlpreview.github.io/?https://github.com/test-fullautomation/robotframework-tutorial/blob/develop/900_building_testsuites/building_testsuites.html>`_.


Feedback
--------

To give us a feedback, you can send an email to `Thomas Pollerspöck <mailto:Thomas.Pollerspoeck@de.bosch.com>`_ or
`RBVH-ECM-Automation_Test_Framework-Associates <mailto:RBVH-ENG2-CMD-Associates@bcn.bosch.com>`_

About
-----

Maintainers
~~~~~~~~~~~

`Thomas Pollerspöck <mailto:Thomas.Pollerspoeck@de.bosch.com>`_

Contributors
~~~~~~~~~~~~

`Mai Dinh Nam Son <mailto:Son.MaiDinhNam@vn.bosch.com>`_

`Tran Duy Ngoan <mailto:Ngoan.TranDuy@vn.bosch.com>`_

`Nguyen Huynh Tri Cuong <mailto:Cuong.NguyenHuynhTri@vn.bosch.com>`_

`Tran Hoang Nguyen <mailto:Nguyen.TranHoang@vn.bosch.com>`_

`Holger Queckenstedt <mailto:Holger.Queckenstedt@de.bosch.com>`_

License
-------

Copyright 2020-2026 Robert Bosch GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
