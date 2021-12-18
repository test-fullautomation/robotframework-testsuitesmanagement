.. Copyright 2020-2022 Robert Bosch Car Multimedia GmbH

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Project Name 
============

This repository is using to develop python package library -
RobotFramework_Testsuites, this package is a part of ROBFW-AIO which is
changed into a more advanced from Robot Framework for automation test
projects in Bosch. This RobotFramework_Testsuites package manages Robot
test project using configuration file in json format, 4 levels
configuration, jsonschema validate, etc. The enhanced features will be
introduced below in details.

Table of Contents 
-----------------

-  `Getting Started  <#getting-started->`__

   -  `1. Configure with json files: <#1-configure-with-json-files>`__
   -  `2. Dotdict features: <#2-dotdict-features>`__

-  `Building and Testing  <#building-and-testing->`__
-  `Contribution Guidelines  <#contribution-guidelines->`__
-  `Feedback  <#feedback->`__
-  `About  <#about->`__

   -  `Maintainers  <#maintainers->`__
   -  `Contributors  <#contributors->`__
   -  `3rd Party Licenses  <#3rd-party-licenses->`__
   -  `Used Encryption  <#used-encryption->`__
   -  `License  <#license->`__

Getting Started 
---------------

The RobotFramework_Testsuites package works together with
`JsonPreprocessor python
package <https://sourcecode.socialcoding.bosch.com/projects/ROBFW/repos/python-jsonpreprocessor/browse>`__
to provide the enhanced features such as json configuration files, 4
different levels of configuation, config object and global params,
schema validation,… ### **1. Configure with json files:**

Together with JsonPreprocessor package, RobotFramework_Testsuites
supports configuring ROBFW automation test project with json files which
allow user adds the comments, imports params from other json files.
Adding comments and importing json files are enhanced features which are
developed and documented in `JsonPreprocessor python
package <https://sourcecode.socialcoding.bosch.com/projects/ROBFW/repos/python-jsonpreprocessor/browse>`__.

RobotFramework_Testsuites management difines 4 different configuration
levels, from level 1 -> level 4, Level 1 is highest priority, and level
4 is lowest priority. The detail of these configuration levels will be
introduced below:

**a. Level 1: Load configuration file while executing robot testsuite by
command.**

This is highest priority configuration level, it is called
**configuration level 1**

User can address the json configuration file when executing robot
testsuite with input parameter *–variable config_file:<filename>*

Ex: robot –variable config_file:<filename>

The level 1 configuration could be set by defined the ``${config_file}``
in ``*** Variables ***``

Ex:

.. code:: r

   *** Variables ***
   ${config_file}   <Path_to_configuration_file>

   *** Settings ***
   #Force Tags        atestExcluded
   Library      RobotFramework_Testsuites    WITH NAME    testsuites
   Suite Setup      testsuites.testsuite_setup
   Suite Teardown   testsuites.testsuite_teardown
   Test Setup       testsuites.testcase_setup
   Test Teardown    testsuites.testcase_teardown

**b. Level 2: In case project have many variants, it reads from content
of the json file to select the corresponding variant configuration.**

If the level 1 is not configured, it will check the configuration for
level 2.

In level 2 configuration, user has to create a json file which contains
different variants point to different configuration files. For example,
we create the ``variants_cfg.json`` with content below:

.. code:: json

   //*****************************************************************************
   // The file configures the access to all variant dependent robot_config*.json
   // files.
   //
   // The path to the robot_config*.json files depends on the test file location. A 
   // different number of ../ is required dependend on the directory depth of the test 
   // case location.
   // Therefore we use here three .../ to tell the ROBFW to search from the test 
   // file location up till the robot_config*.json files are found:
   // ./config/robot_config.json
   // ../config/robot_config.json
   // ../../config/robot_config.json
   // ../../../config/robot_config.json
   // and so on.
   //*****************************************************************************
   {
     "default": {
       "name": "robot_config.json",
       "path": ".../config/"
     },
     "variant_0": {
       "name": "robot_config.json",
       "path": ".../config/"
     },
     "variant_1": {
       "name": "robot_config_variant_1.json",
       "path": ".../config/"
     },
     "variant_2": {
       "name": "robot_config_variant_2.json",
       "path": ".../config/"
     }
   }

User can set configuration level 2 only in testsuite like below:

.. code:: r

   *** Settings ***
   Library      RobotFramework_Testsuites    WITH NAME    testsuites
   Suite Setup      testsuites.testsuite_setup    <Path_to_the_file_variants_cfg.json>
   Suite Teardown   testsuites.testsuite_teardown
   Test Setup       testsuites.testcase_setup
   Test Teardown    testsuites.testcase_teardown

**c. Level 3: Find the ``config/`` folder in testsuite directory, if the
config folder is found, ROBFW-AIO will load configuration file in this
folder.**

In case level 2 and level 2 are not configured, it will check the
configuration for level 3.

If there is the configuration file have the same with testsuite file
(ex: ``abc.rotbot`` & ``./config/abc.json``), then it will load this
configuration file. If not the first case, it will load the
configuration file ``./config/robot_config.json``. In case these 2
situations are not matched => ROBFW will load the configuration level 4
(default and lowest priority)

Ex: We have testsuite ``./component/abc.robot``

-  In ``./component/config/`` contains ``abc.json`` and
   ``robot_config.json``, then ``./component/config/abc.json`` will be
   loaded.
-  In ``./component/config/`` contains ``robot_config.json``, then
   ``./component/config/robot_config.json`` will be loaded.
-  If there is not ``./component/config/`` or the directory
   ``./component/config/`` doesn’t have ``abc.json`` or
   ``robot_config.json``, then configuration level 4 will be set.

**d. Level 4: Lowest priority level, it reads default configuration
file**

The default configuration file (``robot_config.json``) in install
ROBFW-AIO installation directory:
``C:\Program Files\RobotFramework\python39\Lib\site-packages\RobotFramework_Testsuites-0.1.0-py3.9.egg\RobotFramework_Testsuites\Config\robot_config.json``

The default configuration file just contains some basic parameters:
``Json  {   "Project": "G3g",   "WelcomeString": "Hello... ROBFW is running now!",   // Version control information.   "version": {     "majorversion": "0",     "minorversion": "1",     "patchversion": "1"   },   "TargetName" : "gen3flex@dlt" }``

**2. Dotdict features:**
~~~~~~~~~~~~~~~~~~~~~~~~

User can access dictionary object in robot test script by called
``${dict}[abc][def]`` or ``${dict.abc.def}``

-  **Note:** In case a parameter name contains a “.”, then we could not
   use dotdict but the traditional way ``${dict}[abc][def]`` is still
   working.

Building and Testing 
--------------------

If the repository contains SW, add instructions on how to build it from
source and test it in this section.

Contribution Guidelines 
-----------------------

Use this section to describe or link to documentation which explaining
how users can make contributions to the contents of this repository.
Consider adopting the `BIOS way of facilitating
contributions <http://bos.ch/ygF>`__.

Configure Git and correct EOL handling 
--------------------------------------

Here you can find the references for `Dealing with line
endings <https://help.github.com/articles/dealing-with-line-endings/>`__.

Every time you press return on your keyboard you’re actually inserting
an invisible character called a line ending. Historically, different
operating systems have handled line endings differently. When you view
changes in a file, Git handles line endings in its own way. Since you’re
collaborating on projects with Git and GitHub, Git might produce
unexpected results if, for example, you’re working on a Windows machine,
and your collaborator has made a change in OS X.

To avoid problems in your diffs, you can configure Git to properly
handle line endings. If you are storing the .gitattributes file directly
inside of your repository, than you can asure that all EOL are manged by
git correctly as defined.

Feedback 
--------

Consider using this section to describe how you would like other
developers to get in contact with you or provide feedback.

About 
-----

Maintainers 
~~~~~~~~~~~

List the maintainers of this repository here. Consider linking to their
Bosch Connect profile pages. Mention or link to their email as a
minimum.

Contributors 
~~~~~~~~~~~~

Consider listing contributors in this section to give explicit credit.
You could also ask contributors to add themselves in this file on their
own.

License 
~~~~~~~

robotframework-qconnect-base is open source software provided under the `Apache License
2.0`__. 

__ http://apache.org/licenses/LICENSE-2.0
