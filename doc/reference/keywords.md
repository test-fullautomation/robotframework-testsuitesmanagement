# Keywords

Import of the library:

```robotframework
*** Settings ***
Library    RobotFramework_TestsuitesManagement    AS    tm
```

The library has the scope `GLOBAL`. Keywords can be written in Robot Framework style (`Testsuite Setup`) or
in Python style (`testsuite_setup`).

## Overview

| Group | Keywords |
|---|---|
| Setup and teardown | [Testsuite Setup](#testsuite-setup), [Testsuite Teardown](#testsuite-teardown), [Testcase Setup](#testcase-setup), [Testcase Teardown](#testcase-teardown) |
| Configuration | [Get Config](#get-config), [Load Json](#load-json) |
| Installation | [Is Robotframework AIO](#is-robotframework-aio), [Get Package Context File](#get-package-context-file) |
| Version information | [Get Reference Version](#get-reference-version) and others, [Get TSM Version](#get-tsm-version) and others, [Get Bundle Version](#get-bundle-version) and others |
| Version control | [Check Version](#check-version), [Get Status Messages](#get-status-messages) |

## Setup and teardown

### Testsuite Setup

```robotframework
tm.testsuite_setup    [testsuite_cfg_file]
```

Loads the configuration, executes the implicit version check and logs basic information about the test execution.

| Argument | Default | Description |
|---|---|---|
| `testsuite_cfg_file` | `''` | path to the variant configuration file (activates [level 2](../user-guide/configuration-levels.md)); absolute, relative to the robot file, or with `.../` for upward search |

If the configuration cannot be loaded, the suite is aborted. See [Troubleshooting](../user-guide/troubleshooting.md).

### Testsuite Teardown

```robotframework
tm.testsuite_teardown
```

Writes the result of the test suite to the log: `SUITE '<name>' finished with result '<status>'` (plus the reason, if not passed).

### Testcase Setup

```robotframework
tm.testcase_setup
```

Writes the number of the current test case to the log: `Test Count: <n>`.

### Testcase Teardown

```robotframework
tm.testcase_teardown
```

Writes the result of the test case to the log: `TEST '<name>' finished with result '<status>'` (plus the reason, if not passed).

## Configuration

### Get Config

```robotframework
${config}=    tm.get_config
```

Returns a copy of the complete loaded configuration (including `params`) as dictionary.

### Load Json

```robotframework
${data}=    tm.load_json    json_file    [level=1]    [variant=default]
```

Loads a JSONP file with the JsonPreprocessor and returns the content.

| Argument | Default | Description |
|---|---|---|
| `json_file` | - | path to the JSONP file |
| `level` | `1` | `1`: return the content of `json_file`. Other value: `json_file` is a variant configuration file - the parameter configuration file of `variant` is loaded and returned |
| `variant` | `default` | variant name (only used if `level` is not `1`) |

!!! note
    `load_json` only reads files - the loaded values do **not** change the active configuration and do not create
    global variables.

## Installation

### Is Robotframework AIO

```robotframework
${is_aio}=    tm.is_robotframework_aio
```

Returns `True` if the TestsuitesManagement is part of a RobotFramework AIO installation, `False` for a stand-alone installation.

### Get Package Context File

```robotframework
${file}=    tm.get_package_context_file
```

Returns path and name of the RobotFramework AIO package context file (`None` in a stand-alone installation).

## Version information

All keywords have no arguments and return a string (or `None`, if the information is not available).

### Get Reference Version

The **reference** is the RobotFramework AIO bundle (if installed) or the TestsuitesManagement (stand-alone).

| Keyword | Returns |
|---|---|
| `get_reference_version` | version used as reference for version checks |
| `get_reference_version_date` | date of this version |
| `get_reference_app_name` | name of the reference application |
| `get_reference_installer_location` | download location of the reference installer |

### Get TSM Version

| Keyword | Returns |
|---|---|
| `get_tsm_version` | version of the TestsuitesManagement |
| `get_tsm_version_date` | date of this version |
| `get_tsm_app_name` | `RobotFramework_TestsuitesManagement` |
| `get_tsm_installer_location` | GitHub release page of the TestsuitesManagement |

### Get Bundle Version

| Keyword | Returns |
|---|---|
| `get_bundle_version` | version of the RobotFramework AIO bundle |
| `get_bundle_version_date` | date of this version |
| `get_bundle_name` | name of the bundle |
| `get_bundle_installer_location` | download location of the bundle installer |

In a stand-alone installation the bundle keywords return `None`.

## Version control

### Check Version

```robotframework
${result}=    tm.check_version    [min_version]    [max_version]    [reference_version]    [status_messages]
```

Checks `min_version` and `max_version` against `reference_version`.

| Argument | Default | Description |
|---|---|---|
| `min_version` | `None` | lowest allowed version; `None`: not checked |
| `max_version` | `None` | highest allowed version; `None`: not checked |
| `reference_version` | `None` | version to check; `None`: version of the installed software |
| `status_messages` | `None` | own status messages (see [Get Status Messages](#get-status-messages)) |

Returns `True` if the check passed or was skipped. Otherwise an error is logged and the execution is aborted.
Details and examples: [Version control](../user-guide/version-control.md).

### Get Status Messages

```robotframework
${messages}=    tm.get_status_messages
```

Returns a dictionary with the default status messages of the version check. The keys are the
[result tokens](../user-guide/version-control.md#results-at-a-glance).
