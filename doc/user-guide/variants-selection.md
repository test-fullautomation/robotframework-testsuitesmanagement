# Variants selection

This section contains the command line examples for the [configuration levels](configuration-levels.md).

## Level 1 - parameter configuration file in command line

```bash
robot --variable config_file:"(path to parameter configuration file)" tests/
```

## Level 2 - variant name in command line

```bash
robot --variable variant:"(variant name)" tests/
```

Requires a variant configuration file passed to `testsuite_setup`:

```robotframework
Suite Setup    tm.testsuite_setup    .../config/exercise_variants.jsonp
```

Without `--variable variant:...` the variant `default` is used.

!!! danger "Not allowed"
    `config_file` and `variant` must not be used together. Between levels there is an *either-or* relationship -
    the TestsuitesManagement aborts the execution with:

    ```text
    Redundant settings detected in command line: Parameter 'variant' is used together with parameter 'config_file'.
    ```

## Level 3 - parameter configuration from a `config` folder

The folder `config` has to be placed in the same folder as the test suites. Files in this folder are considered
under two conditions:

| Rule | Example |
|---|---|
| file with the same name as the robot file (higher priority) | `example.robot` → `./config/example.jsonp` |
| file with the fixed name `robot_config.jsonp` | `./config/robot_config.jsonp` |

With the first rule every test suite in a folder can have its own individual configuration.

```text
tests/
├── config/
│   ├── example.jsonp          # used by example.robot
│   └── robot_config.jsonp     # used by all other robot files
├── example.robot
└── other.robot
```

!!! note
    Instead of `.jsonp` also the extension `.json` is accepted. But both files (`example.jsonp` **and**
    `example.json`) must not exist at the same time - this causes the error
    *"Configuration file duplicate detected (both extensions: 'jsonp' and 'json')!"*.

## Level 4 - default configuration

No command line parameter, no variant configuration file, no `config` folder: the TestsuitesManagement
loads the default configuration of the installation and logs a warning.
