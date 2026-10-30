# Runtime information

Besides the configuration parameters, the TestsuitesManagement provides further information during the test execution.

## Global variables

| Variable | Content |
|---|---|
| `${CONFIG}` | top level parameters of the configuration (`Project`, `TargetName`, `WelcomeString`, versions, ...) as `DotDict` |
| `${<name>}` | every parameter defined in `params` → `global` |
| `${SUITECOUNT}` | number of the current test suite (counted from 1) |
| `${TESTCOUNT}` | number of the current test case (counted from 1 over the entire execution) |

```robotframework
Log    Suite ${SUITECOUNT}, test ${TESTCOUNT} on target ${CONFIG.TargetName}
```

## Suite metadata

The following metadata are written to the top level suite and are visible in log and report:

| Metadata | Source |
|---|---|
| `project` | parameter `Project` of the configuration |
| `machine` | name of the computer |
| `tester` | name of the user |
| `testtool` | Robot Framework version (e.g. `Robot Framework 7.x (Python 3.x on win32)`) |
| `reference_version` | reference version for the [version control](version-control.md) |
| `reference_app_name` | RobotFramework AIO or TestsuitesManagement |
| `version_sw` | command line: `--variable version_sw:"..."` |
| `version_hw` | command line: `--variable version_hw:"..."` |
| `version_test` | command line: `--variable version_test:"..."` |

Example: document the versions of the system under test in the report:

```bash
robot --variable version_sw:"SW 1.2.3" --variable version_hw:"HW B2" tests/
```

## Overview of all command line variables

| Variable | Purpose | Details |
|---|---|---|
| `config_file` | parameter configuration file (level 1) | [Variants selection](variants-selection.md) |
| `variant` | variant name (level 2) | [Variants selection](variants-selection.md) |
| `local_config` | local configuration file | [Local configuration](local-configuration.md) |
| `version_sw`, `version_hw`, `version_test` | versions written to the metadata | see above |

| Environment variable | Purpose |
|---|---|
| `ROBOT_LOCAL_CONFIG` | local configuration file (if `local_config` is not given) |

## Log entries of the setup and teardown keywords

```text
INFO - Running with configuration level 2 (variant name in command line)
INFO - Version check passed (RobotFramework AIO (extended))
INFO - Loaded configuration file 'C:/project/config/config_variant_1.jsonp'
INFO - Suite Path: 'C:/project/tests/'
INFO - Local config file: 'C:/benches/bench1.jsonp'
INFO - Number of test suites: 1
INFO - Total number of testcases: 3
INFO - Test Count: 1                                         (testcase_setup)
INFO - TEST 'Show configuration' finished with result 'PASS' (testcase_teardown)
INFO - SUITE 'Example' finished with result 'PASS'           (testsuite_teardown)
```
