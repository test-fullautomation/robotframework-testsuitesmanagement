.. Copyright 2020-2023 Robert Bosch GmbH

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

The **RobotFramework_TestsuitesManagement** enables users to define dynamic configuration values within separate configuration files in JSON format.

These configuration values are available during test execution - but under certain conditions that can be defined by the user
(e.g. to realize a variant handling). This means: Not all parameter values are available during test execution - only the ones
that belong to the current test scenario.

To realize this, the **RobotFramework_TestsuitesManagement** provides the following features:

* Split all possible configuration values into several JSON configuration files, with every configuration file contains a specific set of values for configuration parameter
* Use nested imports of JSON configuration files
* Follow up definitions in configuration files overwrite previous definitions (of the same parameter)
* Select between several criteria to let the Robot Framework use a certain JSON configuration file

How to install
--------------

The **RobotFramework_TestsuitesManagement** can be installed in two different ways.

1. Installation via PyPi (recommended for users)

   .. code::

      pip install RobotFramework_TestsuitesManagement

   `RobotFramework_TestsuitesManagement in PyPi <https://pypi.org/project/robotframework-testsuitesmanagement/>`_

2. Installation via GitHub (recommended for developers)

   * Clone the **RobotFramework_TestsuitesManagement** repository to your machine

     .. code::

        git clone https://github.com/test-fullautomation/robotframework-testsuitesmanagement.git

     `RobotFramework_TestsuitesManagement in GitHub <https://github.com/test-fullautomation/robotframework-testsuitesmanagement>`_

   * Install dependencies

     **RobotFramework_TestsuitesManagement** requires some additional Python libraries. Before you install the cloned repository sources
     you have to install the dependencies manually. The names of all related packages you can find in the file ``requirements.txt``
     in the repository root folder. Use pip to install them:

     .. code::

        pip install -r requirements.txt

     Additionally install **LaTeX** (recommended: TeX Live). This is used to render the documentation.

   * Configure dependencies

     The installation of **RobotFramework_TestsuitesManagement** includes to generate the documentation in PDF format. This is done by
     an application called **GenPackageDoc**, that is part of the installation dependencies (see ``requirements.txt``).

     **GenPackageDoc** uses **LaTeX** to generate the documentation in PDF format. Therefore **GenPackageDoc** needs to know where to find
     **LaTeX**. This is defined in the **GenPackageDoc** configuration file

     .. code::

        packagedoc\packagedoc_config.json

     Before you start the installation you have to introduce the following environment variable, that is used in ``packagedoc_config.json``:

     - ``GENDOC_LATEXPATH`` : path to ``pdflatex`` executable

   * Use the following command to install **RobotFramework_TestsuitesManagement**:

     .. code::

        setup.py install


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

Copyright 2020-2023 Robert Bosch GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
