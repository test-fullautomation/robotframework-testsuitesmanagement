#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# -*- coding: utf-8 -*-

# **************************************************************************************************************
#
# setup.py
#
# CM-CI1/ECA3-Queckenstedt
#
# Extends the standard setuptools installation by adding the documentation in HTML format
# (requires installation mode) and tidying up some folders.
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# This script deletes folders (as defined in config.CConfig, depending on the position of this script):
# - previous builds within this repository
# - previous installations within
#   * %ROBOTPYTHONPATH%\Lib\site-packages (Windows)
#   * ${RobotPythonPath}/../lib/python3.9/site-packages (Linux)
#
# before the build and the installation start again!
#
#                                         !!! USE WITH CAUTION !!!
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# --------------------------------------------------------------------------------------------------------------
#
# * Hints:
#
# The usual
#    packages = setuptools.find_packages(),
# is replaced by
#    packages = [str(oRepositoryConfig.Get('sPackageName')), ],
# to avoid that also config.CConfig() and config.CExtendedSetup() are part of the distribution.
# CConfig and CExtendedSetup() are only repository internal helper.
#
# * Possible improvements:
#
#   - What does install.run(self) return? How to realize error handling?
#
# * Known issues:
#
#   - setuptools do not properly update an existing package installation under %ROBOTPYTHONPATH%\Lib\site-packages\<package name>!
#     > Files modified manually within installation folder, are still modified after repeated execution of setuptools.
#     > Files added manually within installation folder, are still present there after repeated execution of setuptools.
#     > Only files deleted manually within installation folder, are are restored there after repeated execution of setuptools.
#   - No such issues with %ROBOTPYTHONPATH%\Lib\site-packages\<package name>-<versions>.egg-info.
#   - Solution: explicit deletion of all previous output (all documentation-, build- and installation-folder, except the egg-info folder)
#     (see 'delete_previous_build()' and 'delete_previous_installation()')
#
# --------------------------------------------------------------------------------------------------------------
#
# 11.10.2021 / XC-CI1/ECA3-Queckenstedt
# Fixed computation order of readme files together with long_description
# 
# 30.09.2021 / XC-CI1/ECA3-Queckenstedt
# Added wrapper for error messages
# 
# Initial version 08/2021
#
# --------------------------------------------------------------------------------------------------------------

import os, sys, platform, shlex, subprocess
import setuptools
from setuptools.command.install import install

from config.CConfig import CConfig # providing repository and environment specific information
from config.CExtendedSetup import CExtendedSetup # providing functions to support the extended setup process

import colorama as col

col.init(autoreset=True)

COLBR = col.Style.BRIGHT + col.Fore.RED
COLBY = col.Style.BRIGHT + col.Fore.YELLOW
COLBG = col.Style.BRIGHT + col.Fore.GREEN

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg):
    sys.stderr.write(COLBR + f"Error: {sMsg}!\n")

def printexception(sMsg):
    sys.stderr.write(COLBR + f"Exception: {sMsg}!\n")

# --------------------------------------------------------------------------------------------------------------

class ExtendedInstallCommand(install):
    """Extended installation for installation mode."""
    def run(self):
        # Extended installation step 1/5 moved to outside ExtendedInstallCommand because results are needed earlier
        print()
        print(COLBY + "Extended installation step 2/5: Deleting previous setup outputs (build, dist, <package name>.egg-info within repository)")
        print()
        nReturn = oExtendedSetup.delete_previous_build()
        if nReturn != SUCCESS:
            return nReturn
        print()
        print(COLBY + "Extended installation step 3/5: Deleting previous package installation folder within site-packages") # (<package name> and <package name>_doc under %ROBOTPYTHONPATH%\Lib\site-packages
        print()
        nReturn = oExtendedSetup.delete_previous_installation()
        if nReturn != SUCCESS:
            return nReturn
        print(COLBY + "Extended installation step 4/5: install.run(self)") # creates the build folder .\build
        print()
        install.run(self) # TODO: What does install.run(self) return? How to realize error handling?
        print()
        print(COLBY + "Extended installation step 5/5: Add html documentation to package installation folder") # (./doc/_build/html to %ROBOTPYTHONPATH%\Lib\site-packages\<package name>_doc)
        print()
        nReturn = oExtendedSetup.add_htmldoc_to_installation()
        if nReturn != SUCCESS:
            return nReturn
        print()
        print(COLBG + "Extended installation done")
        print()
        return SUCCESS

# eof class ExtendedInstallCommand(install):

# --------------------------------------------------------------------------------------------------------------

# -- setting up the repository configuration
oRepositoryConfig = None
sReferencePath = os.path.dirname(os.path.abspath(sys.argv[0]))
try:
    oRepositoryConfig = CConfig(sReferencePath)
except Exception as ex:
    print()
    printexception(str(ex))
    print()
    sys.exit(ERROR)

# -- setting up the extended setup
oExtendedSetup = None
try:
    oExtendedSetup = CExtendedSetup(oRepositoryConfig)
except Exception as ex:
    print()
    printexception(str(ex))
    print()
    sys.exit(ERROR)

# --------------------------------------------------------------------------------------------------------------

print()
print(COLBY + "Entering extended installation")
print()
print(COLBY + "Extended installation step 1/5: Calling the documentation builder")
# (previously called inside ExtendedInstallCommand - but this is too late, because the content of the initially
# generated or updated README file is already needed for the long_description below.)
print()
nReturn = oExtendedSetup.gen_doc()
if nReturn != SUCCESS:
    sys.exit(nReturn)
print()

# --------------------------------------------------------------------------------------------------------------

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
# --------------------------------------------------------------------------------------------------------------

setuptools.setup(
    name         = str(oRepositoryConfig.Get('sPackageName')),
    version      = str(oRepositoryConfig.Get('sVersion')),
    author       = str(oRepositoryConfig.Get('sAuthor')),
    author_email = str(oRepositoryConfig.Get('sAuthorEMail')),
    description  = str(oRepositoryConfig.Get('sDescription')),
    long_description = long_description,
    long_description_content_type = str(oRepositoryConfig.Get('sLongDescriptionContentType')),
    url = str(oRepositoryConfig.Get('sURL')),
    packages = [str(oRepositoryConfig.Get('sPackageName')), ],
    classifiers = [
        str(oRepositoryConfig.Get('sProgrammingLanguage')),
        str(oRepositoryConfig.Get('sLicence')),
        str(oRepositoryConfig.Get('sOperatingSystem'))
    ],
    python_requires = str(oRepositoryConfig.Get('sPythonRequires')),
    cmdclass={
        'install': ExtendedInstallCommand,
    },
)

# --------------------------------------------------------------------------------------------------------------
