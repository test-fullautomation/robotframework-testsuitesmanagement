# Package Description

The **RobotFramework_TestsuitesManagement** allows users to define
dynamic configuration values within separate configuration files in JSON
format.

These configuration values are available during test execution - but
under certain conditions that can be defined by the user (e.g. to
realize a variant handling). This means: Not all parameter values are
available during test execution - only the ones that belong to the
current test scenario.

To realize this, the **RobotFramework_TestsuitesManagement** provides
the following features:

-   Split all possible configuration values into several JSON
    configuration files, with every configuration file contains a
    specific set of values for configuration parameter
-   Use nested imports of JSON configuration files
-   Follow up definitions in configuration files overwrite previous
    definitions (of the same parameter)
-   Select between several criteria to let the Robot Framework use a
    certain JSON configuration file

## How to install

The **RobotFramework_TestsuitesManagement** can be installed in two
different ways.

1.  Installation via PyPi (recommended for users)

    ``` 
    pip install RobotFramework_TestsuitesManagement
    ```

    [RobotFramework_TestsuitesManagement in
    PyPi](https://pypi.org/project/robotframework-testsuitesmanagement/)

2.  Installation via GitHub (recommended for developers)

    Clone the **RobotFramework_TestsuitesManagement** repository to your
    machine.

    ``` 
    git clone https://github.com/test-fullautomation/robotframework-testsuitesmanagement.git
    ```

    [RobotFramework_TestsuitesManagement in
    GitHub](https://github.com/test-fullautomation/robotframework-testsuitesmanagement)

    Use the following command to install
    **RobotFramework_TestsuitesManagement**:

    ``` 
    setup.py install
    ```

## Package Documentation

A detailed documentation of the **RobotFramework_TestsuitesManagement**
can be found here:
[RobotFramework_TestsuitesManagement.pdf](https://github.com/test-fullautomation/robotframework-testsuitesmanagement/blob/develop/RobotFramework_TestsuitesManagement/RobotFramework_TestsuitesManagement.pdf)

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
