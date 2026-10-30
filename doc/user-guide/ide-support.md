# IDE support

The TestsuitesManagement sets `${CONFIG}` and all parameters of `params` → `global` at runtime
(`testsuite_setup`). A static code analysis like [RobotCode](https://robotcode.io) in VS Code does not execute
`testsuite_setup` and therefore reports these variables as unknown:

```text
Variable '${CONFIG.Project}' not found.  robotcode.namespace(VariableNotFound)
```

The test execution is not affected. To make the variables known to the IDE, the TestsuitesManagement provides the
variable file `RobotFramework_TestsuitesManagement.ide_variables`. It loads the configuration exactly like
`testsuite_setup` and returns the same variables to the code analysis.

## Setup

The variable file is registered in the IDE settings - **not** in the robot files.

**Arguments** (separated by `:`, on Windows with absolute paths by `;`):

| Argument | Description |
|---|---|
| `config_file` | variant configuration file (configuration level 2) or parameter configuration file (configuration level 1); relative to the project root |
| `variant` | optional; name of the variant (default: `default`); ignored for parameter configuration files |

=== "VS Code settings.json"

    ```json
    {
      "robotcode.robot.variableFiles": [
        "RobotFramework_TestsuitesManagement.ide_variables:config/variants.jsonp:variant1"
      ]
    }
    ```

=== "robot.toml"

    ```toml
    variable-files = [
      "RobotFramework_TestsuitesManagement.ide_variables:config/variants.jsonp:variant1"
    ]

    [tool.robotcode-analyze.cache]
    ignored-variables = ["RobotFramework_TestsuitesManagement.ide_variables"]
    ```

!!! tip "Changes of the configuration files"
    RobotCode caches the content of variable files. Changes of the configuration files are visible in the IDE
    after **RobotCode: Clear Cache and Restart Language Servers** - or immediately, if the variable file is excluded
    from the cache with `ignored-variables` (see above).

## Behavior

* During the static code analysis the variable file returns `${CONFIG}` and all parameters of `params` → `global`
  as `DotDict` (like at runtime).
* Additionally every key of a dictionary is returned as separate variable in dotdict notation, e.g.
  `${CONFIG.Project}` or `${dSUT.tuner.fm.frequency.nMax_MHz}`. Therefore `${CONFIG.` + `Ctrl+Space` lists the
  sub keys, and the hover shows the value of the selected variant.
* During the test execution the variable file returns **nothing**. The settings of RobotCode are also passed to
  test executions started from the IDE; variables that exist before `testsuite_setup` would not be overwritten by
  the TestsuitesManagement (see [Priority](priority.md#robot-framework-mechanisms)). Therefore the values at runtime always come from
  `testsuite_setup` - also if the IDE uses another variant.
* Errors (file not found, unknown variant, JSONP syntax errors) are shown by RobotCode as import error of the
  variable file.

## Limits

* Only the variables of the selected variant are known; a local configuration is not considered.
* The code completion of sub keys works with the dotdict notation only (`${CONFIG.Project}`), not with the item
  syntax (`${CONFIG}[Project]`). Keys that are no valid Python identifiers (e.g. with spaces) and elements of lists
  are not listed.
* Never define parameters of `params` → `global` statically in robot files, `robot.toml` or own variable files to
  silence the IDE - the TestsuitesManagement would not overwrite them at runtime.
