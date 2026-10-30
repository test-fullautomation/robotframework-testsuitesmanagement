# Troubleshooting

If the configuration cannot be loaded, the TestsuitesManagement writes the reasons as `ERROR` to the log and aborts
the test suite with:

```text
Not possible to load the test configuration. The test execution will be aborted!
```

Depending on the installation, the result of the suite is `UNKNOWN` (RobotFramework AIO) or `FAIL`.
Look at the `ERROR` entries **before** this message - they contain the reason and the affected file.

## Typical errors

??? failure "Redundant settings detected in command line: Parameter 'variant' is used together with parameter 'config_file'."
    `config_file` (level 1) and `variant` (level 2) must not be used together. Remove one of them.
    See [Priority](priority.md#config_file-and-variant-together).

??? failure "Not able to get a configuration for variant '...' because of a variant configuration file is not available."
    A variant is given in command line, but `testsuite_setup` is called without variant configuration file.
    Pass the variant configuration file: `tm.testsuite_setup    .../config/variants.jsonp`.

??? failure "Could not find the variant configuration file: '.../config/variants.jsonp'"
    The three dots search did not find the file in the robot file folder or any parent folder.
    Check the name and the position of the `config` folder.

??? failure "The variant '...' is not defined in '...'. Please find the suitable variant in this list: ..."
    Typo in the variant name. The message lists all variants of the variant configuration file.

??? failure "The variant name '...' is invalid."
    The variant name contains characters that are not allowed. See [Variant configuration file](configuration-files.md#variant-configuration-file).

??? failure "The 'name' or 'path' property is not defined for the variant '...'."
    Every variant entry needs both keys `name` and `path`.

??? failure "Configuration file duplicate detected (both extensions: 'jsonp' and 'json')!"
    In the `config` folder (level 3) both `<name>.jsonp` and `<name>.json` exist. Remove one of them.

??? failure "Did not find configuration file: '...'!"
    The file given by `config_file` or by the variant configuration does not exist. Relative paths in the variant
    configuration file are relative to the variant configuration file.

??? failure "Verification against JSON schema failed ... Please put the additional params into 'params': { 'global': {...}"
    The parameter configuration file contains an unknown top level key. Move user defined parameters into `params` → `global`.

??? failure "Required parameter ... is missing in file '...'."
    One of the mandatory parameters `Project`, `WelcomeString` or `TargetName` is missing.

??? failure "Variable name '...' is invalid. Expected format: ..."
    A key in `params` → `global` violates the [naming convention](naming-convention.md).

??? failure "'...' is a reserved keyword in Robot Framework and cannot be used as parameter name."
    Rename the parameter. See [Reserved names](naming-convention.md#reserved-names).

??? failure "Loading local config failed with file: ... Wrong local config file was chosen, please check!!!"
    The local configuration contains `WelcomeString` (it is a full configuration) or `default` (it is a variant
    configuration file). A local configuration has to be a fragment. See [Local configuration](local-configuration.md).

??? failure "The local configuration file ... which set in ROBOT_LOCAL_CONFIG variable, does not exist!!!"
    The environment variable `ROBOT_LOCAL_CONFIG` points to a file that does not exist.

??? failure "Version check failed: ..." / "Version format error: ..."
    See [Version control](version-control.md).

??? failure "JSONP syntax errors"
    Errors of the JSONP format (e.g. a missing comma, an unknown parameter `${...}`) are reported by the JsonPreprocessor
    together with the affected file and an extract of the code. See [The JSONP format](../jsonp-format/index.md).

## Unexpected values?

| Symptom | Possible reason |
|---|---|
| The configuration of another variant is used | wrong `variant` in command line, or `default` points to another file |
| Level 4 warning in log | no variant configuration file given, no `config` folder found |
| A value from command line is ignored | different spelling of the name, see [Priority](priority.md) |
| Two parameters have the same value | names differ only in underscores or case, see [Naming convention](naming-convention.md#underscores-and-case) |
| A value of an imported file is not used | the `[import]` is placed after the definition, see [Nested configuration files](nested-configuration.md#rules) |
| The IDE reports `Variable '${CONFIG...}' not found` | the variables are set at runtime only, see [IDE support](ide-support.md) |
| A parameter of `params` → `global` keeps another value | the variable is already defined before `testsuite_setup` (robot file, `robot.toml`, own variable file), see [IDE support](ide-support.md#limits) |

!!! tip
    Use the keyword [`Get Config`](../reference/keywords.md#get-config) to log the complete loaded configuration.
