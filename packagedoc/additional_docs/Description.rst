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

Getting Started
---------------

How to install
~~~~~~~~~~~~~~

Firstly, clone **RobotFramework_Testsuites** repository to your machine

.. code-block:: bat

  git clone https://github.com/test-fullautomation/robotframework-testsuitesmanagement.git

Go to **robotframework-testsuitesmanagement**, using the 2 common commands below to build or install this package:

.. code-block:: bat

    setup.py build      will build the package underneath 'build/'
    setup.py install    will install the package

After the build processes are completed, the package is located in **build/**, and the documents are 
located in **build/lib/RobotFramework_Testsuites**.

We can use ``--help`` to discover the options for ``build`` command, example:

.. code-block:: bat

     setup.py build      will build the package underneath 'build/'
     setup.py install    will install the package
   
   Global options:
     --verbose (-v)      run verbosely (default)
     --quiet (-q)        run quietly (turns verbosity off)
     --dry-run (-n)      don't actually do anything
     --help (-h)         show detailed help message
     --no-user-cfg       ignore pydistutils.cfg in your home directory
     --command-packages  list of packages that provide distutils commands
   
   Information display options (just display information, ignore any commands)
     --help-commands     list all available commands
     --name              print package name
     --version (-V)      print package version
     --fullname          print <package name>-<version>
     --author            print the author's name
     --author-email      print the author's email address
     --maintainer        print the maintainer's name
     --maintainer-email  print the maintainer's email address
     --contact           print the maintainer's name if known, else the author's
     --contact-email     print the maintainer's email address if known, else the
                         author's
     --url               print the URL for this package
     --license           print the license of the package
     --licence           alias for --license
     --description       print the package description
     --long-description  print the long package description
     --platforms         print the list of platforms
     --classifiers       print the list of classifiers
     --keywords          print the list of keywords
     --provides          print the list of packages/modules provided
     --requires          print the list of packages/modules required
     --obsoletes         print the list of packages/modules made obsolete
   
   usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
      or: setup.py --help [cmd1 cmd2 ...]
      or: setup.py --help-commands
      or: setup.py cmd --help

Features
--------

Using configuration files in Json format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nowadays, Json is the leading of structuring data for exchange not only for web applications but also for other software 
applications. Json format is used to represent data, and become the universal standard of data exchange, that the reason 
we decided using Json format as configuration file for RobotFramework AIO.

Together with ``JsonPreprocessor`` package, ``RobotFramework_Testsuites`` supports configuring RobotFramework AIO automation 
test project with json files which allow user adds the comments, imports params from other json files. Adding comments and 
importing json files are enhanced features which are developed and documented in ``JsonPreprocessor`` python package.

Define 4 levels of configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``RobotFramework_Testsuites`` management defines 4 different configuration levels, from level 1 to level 4 level 1 is highest 
priority, and level 4 is lowest priority:

**Level 1: Loads configuration file via input parameter of robot command**

This is highest priority of loading configuration method, that means, configuration level 2 or 3 will be ignored even it is set.

This level 1 configuration is designed to force RobotFramework AIO executing with the configuration file for some purpose:

* In case the use wants to execute the robot run with specific configuration file for the particular purposes.

* User re-produces and verifies an issue or a corner case with new configuration file and doesn't want to modify the current 
  configuration file.

User can address the json configuration file when executing robot testsuite with input parameter 
``--variable config_file:"<path_to_json_file>"``

.. code-block::

robot --variable config_file:"<path_to_json_file>" <path_to_testsuite>

**Level 2: Loads Json configuration according to variant name**

This level 2 is designed for the scenario that user creates the automation testing project which running 
for many different variants. When trigger robot run, it will load the appropriate json configuration file.

To set RobotFrameowork AIO run with level 2, first user has to create a json file which contains different 
variants point to different configuration files.

For example, we create the ``variants_cfg.json`` with content below:

.. code-block:: json

   {
     "default": {
       "name": "<default_cfg_file>",
       "path": "<path>"
     },
     "variant_0": {
       "name": "<file_name_variant_0>",
       "path": "<path>"
     },
     "variant_1": {
       "name": "<file_name_variant_1>",
       "path": "<path>"
     },
     "variant_2": {
       "name": "<file_name_variant_2>",
       "path": "<path>"
     }
   }

Then the path of ``variants_cfg.json`` file has to add as input parameter of ``testsuites.testsuite_setup`` 
in ``Suite Setup`` of a testsuite.

In case of user wants to set configuration level 2 for entire RobotFrameowork test project instead of 
indiviual robot testsuite file, ``__init__.robot`` file has to be created at the highest folder of 
RobotFrameowork test project, and the path of ``variants_cfg.json`` file has to be added as input parameter of 
``testsuites.testsuite_setup`` in ``Suite Setup`` of the ``__init__.robot`` file.

.. code-block::

   *** Settings ***
   Library      RobotFramework_Testsuites    WITH NAME    testsuites
   Suite Setup      testsuites.testsuite_setup    <Path_to_the_file_variants_cfg.json>

**Level 3: Find the ``config/`` folder in current testsuite directory**

Configuration level 3 is triggered only in case of level 1 and level 2 were not set.

The configuration level 3 will check in ``config/`` folder in current testsuite directory the existence of json 
file which has the same name with testsuite file (ex: ``abc.rotbot`` & ``./config/abc.json``), then it will 
load this configuration file. In case there is no json file has the same name with robot testsuite file, it will 
check the existence of ``./config/robot_config.json`` then load this ``./config/robot_config.json`` file as 
configuration file. 

**Level 4: Lowest priority level, it reads default configuration file**

In case testsuites management library detects that configuration level 1, level 2, and level 3 are not set, the 
robot execution will use the configuration level 4 by default.

The default configuration file (``robot_config.json``) in installation directory:

``\RobotFramework_Testsuites\Config\robot_config.json``

**Access dictionary object of configuration by traditional way or using "."**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

User can access dictionary object which is defined in configuration file in robot test script by called ``${dict}[abc][def]`` 
or ``${dict.abc.def}``

**Note:** In case a parameter name contains a ".", then it is not possible to use dotdict but the traditional way ``${dict}[abc][def]`` 
is still working.

