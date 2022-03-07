> Licensed under the Apache License, Version 2.0 (the \"License\"); you
> may not use this file except in compliance with the License. You may
> obtain a copy of the License at
>
> <http://www.apache.org/licenses/LICENSE-2.0>
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an \"AS IS\" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
> implied. See the License for the specific language governing
> permissions and limitations under the License.

# ROBFW TESTSUITES MANAGEMENT DOCUMENTATION

**This is the documentation for robotframework-testsuitesmanagement
repository**

## Getting Started

The RobotFramework_Testsuites package works together with
[JsonPreprocessor](https://github.com/test-fullautomation/python-jsonpreprocessor)
python package to provide the enhanced features such as json
configuration files, 4 different levels of configuation, config object
and global params, schema validation,\...

### How to install

Firstly, clone **RobotFramework_Testsuites** repository to your machine

``` bat
git clone https://github.com/test-fullautomation/robotframework-testsuitesmanagement.git
```

Go to **robotframework-testsuitesmanagement**, using the 2 common
commands below to build or install this package:

``` bat
setup.py build      will build the package underneath 'build/'
setup.py install    will install the package
```

After the build processes are completed, the package is located in
**build/**, and the documents are located in **doc/\_build/**.

We can use `--help` to discover the options for `build` command, ex:

``` bat
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
```

## Features

### ROBFW project is configured with json files

Together with `JsonPreprocessor` package, `RobotFramework_Testsuites`
supports configuring ROBFW automation test project with json files which
allow user adds the comments, imports params from other json files.
Adding comments and importing json files are enhanced features which are
developed and documented in `JsonPreprocessor` python package.

`RobotFramework_Testsuites` management difines 4 different configuration
levels, from level 1 -\> level 4, Level 1 is highest priority, and level
4 is lowest priority:

**Level 1: Load configuration file while executing robot testsuite by
command**

User can address the json configuration file when executing robot
testsuite with input parameter
`--variable config_file:" <path_to_json_file>"`

Ex:
`robot --variable config_file:"<path_to_json_file>" <path_to_testsuite>`

**Level 2: In case project have many variants, it reads from json
file\'s content to select the corresponding variant configuration**

In level 2 configuration, user has to create a json file which contains
different variants point to different configuration files. For example,
we create the `variants_cfg.json` with content below:

``` json
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
```

User can set configuration level 2 only in testsuite like below:

``` robot
*** Settings ***
Library      RobotFramework_Testsuites    WITH NAME    testsuites
Suite Setup      testsuites.testsuite_setup    <Path_to_the_file_variants_cfg.json>
```

**Level 3: Find the config/ folder in testsuite directory, if the config
folder is found, it will load configuration file in this folder**

If there is the configuration file have the same name with testsuite
file (ex: `abc.rotbot` & `./config/abc.json`), then it will load this
configuration file. If the first case doesn\'t occur, it will load the
configuration file `./config/robot_config.json`. In case these 2 cases
are not matched, it will load the configuration level 4 (default and
lowest priority)

**Level 4: Lowest priority level, it reads default configuration file**

The default configuration file (`robot_config.json`) in installation
directory:

`python39\Lib\site-packages\RobotFramework_Testsuites-0.1.0-py3.9.egg\RobotFramework_Testsuites\Config\robot_config.json`

### Dotdict features

User can access dictionary object in robot test script by called
`${dict}[abc][def]` or `${dict.abc.def}`

**Note:** In case a parameter name contains a \".\", then we could not
use dotdict but the traditional way `${dict}[abc][def]` is still
working.

### Package Documentation

A detailed documentation of the Python Extensions Collection package can
be found here:
[RobotFramework-Testsuites.pdf](https://github.com/test-fullautomation/robotframework-testsuitesmanagement/blob/develop/doc/_build/latex/RobotFramework-Testsuites.pdf)

## Feedback

To give us a feedback, you can send an email to [Thomas
Pollerspöck](mailto:Thomas.Pollerspoeck@de.bosch.com) or
[RBVH-ECM-Automation_Test_Framework-Associates](mailto:RBVH-ENG2-CMD-Associates@bcn.bosch.com)

## About

### Maintainers

[Thomas Pollerspöck](mailto:Thomas.Pollerspoeck@de.bosch.com)

### Contributors

[Mai Dinh Nam Son](mailto:Son.MaiDinhNam@vn.bosch.com)

[Tran Duy Ngoan](mailto:Ngoan.TranDuy@vn.bosch.com)

[Nguyen Huynh Tri Cuong](mailto:Cuong.NguyenHuynhTri@vn.bosch.com)

[Tran Hoang Nguyen](mailto:Nguyen.TranHoang@vn.bosch.com)

[Holger Queckenstedt](mailto:Holger.Queckenstedt@de.bosch.com)

## License

Copyright 2020-2022 Robert Bosch GmbH

Licensed under the Apache License, Version 2.0 (the \"License\"); you
may not use this file except in compliance with the License. You may
obtain a copy of the License at

> <http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an \"AS IS\" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
