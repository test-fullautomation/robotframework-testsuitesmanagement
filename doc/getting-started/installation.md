# Installation

## Requirements

- Python 3.11 or newer
- Robot Framework 6.1 or newer (installed automatically as dependency)

The TestsuitesManagement is also part of the **RobotFramework AIO** bundle. If you use RobotFramework AIO,
it is already installed and no further steps are required.

## Installation from PyPI (recommended for users)

```bash
pip install RobotFramework_TestsuitesManagement
```

All required dependencies (e.g. the `JsonPreprocessor`, `jsonschema`, `robotframework-pythonlibcore`) are installed
automatically.

## Installation from GitHub (recommended for developers)

```bash
git clone https://github.com/test-fullautomation/robotframework-testsuitesmanagement.git
cd robotframework-testsuitesmanagement
python -m pip install .
```

Behind a proxy:

```bash
python -m pip install --proxy <proxy> .
```

Further developer topics (build, tests, documentation) are described in
[For Developers - Build, test and document](../developers/build-and-test.md).

## Check the installation

```bash
python -c "import RobotFramework_TestsuitesManagement as tm; print(tm.LIBRARY_VERSION)"
```

The console script `robfwaio_version` prints the version of the installed RobotFramework AIO bundle
(in a stand-alone installation of the TestsuitesManagement the output is `None`):

```bash
robfwaio_version
```

!!! info "Stand-alone or bundle?"
    In a stand-alone installation the version of the TestsuitesManagement is used as reference for the
    [version control](../user-guide/version-control.md). Within RobotFramework AIO the version of the entire bundle is used.
