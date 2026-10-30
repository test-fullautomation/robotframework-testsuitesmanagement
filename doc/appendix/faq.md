# FAQ

??? question "Which configuration level should I use?"
    Level 2 (variant configuration file + variant name). It is the most flexible solution and allows new variants
    without changing the test code. See [Configuration levels](../user-guide/configuration-levels.md#why-is-level-2-recommended).

??? question "How do I know which configuration file was used?"
    The log file contains the level and the loaded file:
    `Running with configuration level 2 (...)` and `Loaded configuration file '...'`.

??? question "Why is my parameter not available as `${name}`?"
    Only parameters inside `params` → `global` become Robot Framework variables. Top level parameters are available
    via `${CONFIG}[name]`. See [Content of configuration files](../user-guide/configuration-files.md#summary-how-to-access-parameters).

??? question "Can I add own top level parameters?"
    No. The configuration is validated against a JSON schema. Put own parameters into `params` → `global`.

??? question "Do I need the version check?"
    No. Set `Maximum_version` and `Minimum_version` to `null` or remove them.

??? question "Can I use `.json` instead of `.jsonp`?"
    Yes, both extensions are accepted. But in a level 3 `config` folder, a file must not exist with both extensions.

??? question "How can I use different values on different test benches?"
    Use a [local configuration](../user-guide/local-configuration.md), preferably activated by the environment
    variable `ROBOT_LOCAL_CONFIG` on every test bench.

??? question "What happens if I pass a value with `--variable` that is also defined in the configuration?"
    The command line value wins - if the name is spelled exactly the same. See [Priority](../user-guide/priority.md).

??? question "Is it possible to use the configuration in Python code?"
    Within a test execution use the keyword `Get Config` or Robot Framework's `BuiltIn().get_variable_value()`.
    Outside of Robot Framework load the files directly with the JsonPreprocessor:
    `CJsonPreprocessor().jsonLoad("config.jsonp")`.

??? question "Where can I find more examples?"
    In the [Robot Framework tutorial](https://htmlpreview.github.io/?https://github.com/test-fullautomation/robotframework-tutorial/blob/develop/900_building_testsuites/building_testsuites.html)
    and in the test data of the repository (`atest` and `test/testfiles`).
