Setups
======

20.02.2026

--------------------------------------------------------------------------------------------------------------

The JSON file setup.json defines the repository-specific actions that must be executed (for example, during automatically
running setup processes) to generate a build or install the component.

"PROXYSETTINGS" and "PYTHON" are placeholders for the proxy settings (if needed) and for the Python interpreter.
These placeholders are not defined in the JSON file and must be resolved by the process that computes the JSON file.

In "setup_steps", the keys "CLEANUP", "GENPACKAGEDOC", "INSTALL", and "BUILD" are placeholders that define
individual setup steps.

In "setup_type", the required setup steps are listed for each type.

The distinction between "setup_steps" and "setup_type" enables a very flexible definition of individual setup steps.