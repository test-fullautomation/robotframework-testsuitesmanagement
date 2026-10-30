# Startup sequence

This page describes what happens from the start of `robot` until the first test case is executed.

## Overview

```mermaid
sequenceDiagram
    autonumber
    participant RF as robot
    participant LIB as Library (DynamicCore)
    participant LL as LibListener
    participant KW as CSetupKeywords
    participant C as CConfig
    participant JPP as JsonPreprocessor
    participant V as CVersion

    RF->>LIB: import library (Settings section)
    LIB->>LL: register ROBOT_LIBRARY_LISTENER
    RF->>LL: _start_suite(data, result)
    LL->>C: CConfig() (singleton), testcase_path, chdir
    alt first suite
        LL->>C: remember existing variables (buitin_variables)
        LL->>C: root suite name, total test count
        LL->>C: LOCAL_CONFIG / ROBOT_LOCAL_CONFIG, VARIANT,<br/>VERSION_SW/HW/TEST, CONFIG_FILE (-> level 1)
    end
    LL->>RF: ${SUITECOUNT}
    RF->>KW: Suite Setup: Testsuite Setup [file]
    KW->>C: load_config()
    C->>C: determine level, find configuration file
    C->>JPP: jsonLoad(configuration file)
    C->>JPP: jsonLoad(local configuration)
    C->>C: merge, schema validation, metadata
    C->>RF: set global variables, ${CONFIG}
    KW->>C: check_version()
    C->>V: verify_version(min, max)
    KW->>RF: log level, file, suite path, counters
    RF->>LL: _start_test
    LL->>RF: ${TESTCOUNT}
```

## Phase 1: Listener (`LibListener._start_suite`)

Executed for **every** suite, before the suite setup:

* `CConfig()` returns the singleton instance.
* `testcase_path` is set to the folder of the suite and the **current working directory is changed** to it.
  That's why relative paths in `Testsuite Setup` and in configuration files are relative to the suite file.

Additionally, executed only for the **first** suite (`suite_count == 0`):

| Collected information | Source |
|---|---|
| `buitin_variables` | names of all variables that exist at this point (built-in and command line) |
| `root_suite_name`, `total_testcases` | root of the suite tree |
| `local_config` | `--variable local_config:...` or environment variable `ROBOT_LOCAL_CONFIG` |
| `config_name` | `--variable variant:...` |
| `meta_data.version_sw/hw/test` | `--variable version_sw:...` etc. |
| `test_config_file`, `config_level = LEVEL_1` | `--variable config_file:...` |

At the end `suite_count` is incremented and `${SUITECOUNT}` is set.

`_end_suite` resets the level to `LEVEL_4` (and the configuration file, unless level 1 is active).
So every suite determines its level again in its own `Testsuite Setup`.

## Phase 2: `Testsuite Setup`

```mermaid
flowchart TD
    A["Testsuite Setup [file]"] --> B{"level 1<br/>from listener?"}
    B -- yes --> L["load_config()"]
    B -- no --> C{"file<br/>given?"}
    C -- yes --> D["level = 2"] --> L
    C -- no --> L
    L --> E{"is_cfg_loaded?"}
    E -- no --> F["log all errors from loaded_cfg_log<br/>raise 'unknown' message"]
    E -- yes --> G["log level<br/>(warning for level 4)"]
    G --> H["check_version()"]
    H --> I["log file, suite path,<br/>local config, counters"]
```

## Phase 3: `CConfig.load_config`

```mermaid
flowchart TD
    S([start]) --> L1{"level 1?"}
    L1 -- yes --> E1{"variant given<br/>or file empty?"}
    E1 -- yes --> ERR
    E1 -- no --> FILE
    L1 -- no --> L2{"level 2?"}
    L2 -- yes --> V2["__load_config_file_level2()<br/>read variant file, select variant"] --> FILE
    L2 -- no --> L3{"config/&lt;suite&gt;.jsonp or<br/>config/robot_config.jsonp?"}
    L3 -- yes --> FILE
    L3 -- no --> L4["level 4:<br/>Config/robot_config.jsonp"] --> FILE
    FILE{"file exists?"} -- no --> ERR
    FILE -- yes --> LOAD["JsonPreprocessor.jsonLoad()"]
    LOAD --> LOC{"local config?"}
    LOC -- yes --> LL["jsonLoad(local config)<br/>check: no WelcomeString, no default<br/>__merge_dicts()"] --> SCH
    LOC -- no --> SCH["jsonschema validation"]
    SCH --> VER["check format of<br/>Maximum/Minimum_version"]
    VER --> META["suite metadata"]
    META --> GLOB["__update_global_variable()"]
    GLOB --> CFG["${CONFIG} = DotDict<br/>(without params.global)"]
    CFG --> OK([is_cfg_loaded = True])
    ERR["append to loaded_cfg_log<br/>is_cfg_loaded = False"]
```

### Error handling

`CConfig.loaded_cfg_log` is a dictionary with three entries:

| Key | Content |
|---|---|
| `error` | list of error messages (logged as errors) |
| `info` | list of hints (also logged as errors) |
| `unknown` | final message; used as exception text that aborts the suite |

This allows to report all relevant information at once instead of stopping at the first problem.

### Setting global variables

`__update_global_variable` walks through `params` → `global`:

1. Reserved names (`Settings`, `Variables`, `Keywords`, `Comments`, `Documentation`, `Metadata`) cause an error.
2. Names contained in `buitin_variables` are **skipped** - this is how command line values win.
3. `__set_global_variable` checks the name against `^\p{L}[\p{L}\p{Nd}_]*$`, converts dictionaries (also inside
   lists) to `DotDict` and calls `BuiltIn().set_global_variable()`.

!!! note "Exact name comparison"
    `buitin_variables` contains the names as they were found at the first suite. The comparison is exact, therefore
    a command line variable only wins if it is spelled exactly like the configuration parameter
    (see [Priority](../user-guide/priority.md)).

## Phase 4: Version check

`CConfig.check_version()` uses the **low level** method `CVersion.verify_version()` and formulates own messages
that fit to Robot Framework tests. The reference version is taken from `AppConfig`:

| Installation | Reference version |
|---|---|
| part of RobotFramework AIO (`Config/package_context.json` exists) | bundle version |
| stand-alone | version of the TSM itself |
