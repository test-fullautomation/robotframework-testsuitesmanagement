# **************************************************************************************************************
#
#  Copyright 2020-2023 Robert Bosch GmbH
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
#
# **************************************************************************************************************
#
# setup.py
#
# XC-CT/ECA3-Queckenstedt
#
# Extends the standard setuptools installation by adding the documentation in PDF format
# (requires installation mode) and tidying up some folders.
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# This script deletes folders (as defined in config.CRepositoryConfig, depending on the position of this script):
# - previous builds within this repository
# - previous installations within
#   * <Python installation>\Lib\site-packages (Windows)
#   * <Python installation>/../lib/python3.9/site-packages (Linux)
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
#    packages = [str(oRepositoryConfig.Get('PACKAGENAME')), ],
# to avoid that also config.CRepositoryConfig() and additions.CExtendedSetup() are part of the distribution.
# CRepositoryConfig and CExtendedSetup() are only repository internal helper.
#
# * Known issues:
#
#   - setuptools do not properly update an existing package installation under <Python installation>\Lib\site-packages\<package name>!
#     > Files modified manually within installation folder, are still modified after repeated execution of setuptools.
#     > Files added manually within installation folder, are still present there after repeated execution of setuptools.
#     > Only files deleted manually within installation folder, are are restored there after repeated execution of setuptools.
#   - No such issues with <Python installation>\Lib\site-packages\<package name>-<versions>.egg-info.
#   - Solution: explicit deletion of all previous output (all documentation-, build- and installation-folder, except the egg-info folder)
#     (see 'delete_previous_build()' and 'delete_previous_installation()')
#
# --------------------------------------------------------------------------------------------------------------
#
# 29.06.2022
#
# --------------------------------------------------------------------------------------------------------------

import os, sys, platform, shlex, subprocess
import setuptools
from setuptools.command.install import install

# prefer the repository local version of all additional libraries (instead of the installed version under site-packages)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "./additions")))

from config.CRepositoryConfig import CRepositoryConfig # providing repository and environment specific information
from additions.CExtendedSetup import CExtendedSetup # providing functions to support the extended setup process

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
    """Extended setup for installation mode."""

    def run(self):

        listCmdArgs = sys.argv
        if ( ('install' in listCmdArgs) or ('build' in listCmdArgs) or ('sdist' in listCmdArgs) or ('bdist_wheel' in listCmdArgs) ):
            install.run(self)
        return SUCCESS

# eof class ExtendedInstallCommand(install):

# --------------------------------------------------------------------------------------------------------------

# -- Even in case of other command line parameters than 'install' or 'build' are used we need the following objects.
#    (Without repository configuration commands like '--author-email' would not be possible)

# -- setting up the repository configuration
oRepositoryConfig = None
try:
    oRepositoryConfig = CRepositoryConfig(os.path.abspath(sys.argv[0]))
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

long_description = "long description" # variable is required even in case of other command line parameters than 'install' or 'build' are used

listCmdArgs = sys.argv
if ( ('install' in listCmdArgs) or ('build' in listCmdArgs) or ('sdist' in listCmdArgs) or ('bdist_wheel' in listCmdArgs) ):
    print()
    print(COLBY + "Entering extended installation")
    print()

    print(COLBY + "Extended setup step 1/5: Calling the documentation builder")
    print()

    nReturn = oExtendedSetup.genpackagedoc()
    if nReturn != SUCCESS:
        sys.exit(nReturn)

    print(COLBY + "Extended setup step 2/5: Converting the repository README")
    print()

    nReturn = oExtendedSetup.convert_repo_readme()
    if nReturn != SUCCESS:
        sys.exit(nReturn)

    print(COLBY + "Extended setup step 3/5: Deleting previous setup outputs (build, dist, <package name>.egg-info within repository)")
    print()
    nReturn = oExtendedSetup.delete_previous_build()
    if nReturn != SUCCESS:
        sys.exit(nReturn)

    if ( ('bdist_wheel' in listCmdArgs) or ('build' in listCmdArgs) ):
        print()
        print(COLBY + "Skipping extended setup step 4/5: Deleting previous package installation folder within site-packages")
        print()
    else:
        print()
        print(COLBY + "Extended setup step 4/5: Deleting previous package installation folder within site-packages") # (<package name> and <package name>_doc under <Python installation>\Lib\site-packages
        print()
        nReturn = oExtendedSetup.delete_previous_installation()
        if nReturn != SUCCESS:
            sys.exit(nReturn)

    README_MD = str(oRepositoryConfig.Get('README_MD'))
    with open(README_MD, "r", encoding="utf-8") as fh:
        long_description = fh.read()
    fh.close()


# --------------------------------------------------------------------------------------------------------------

# -- the 'setup' itself

print(COLBY + "Extended setup step 5/5: install.run(self)")
print()

setuptools.setup(
    name         = str(oRepositoryConfig.Get('REPOSITORYNAME')),
    version      = str(oRepositoryConfig.Get('PACKAGEVERSION')),
    author       = str(oRepositoryConfig.Get('AUTHOR')),
    author_email = str(oRepositoryConfig.Get('AUTHOREMAIL')),
    description  = str(oRepositoryConfig.Get('DESCRIPTION')),
    long_description = long_description,
    long_description_content_type = str(oRepositoryConfig.Get('LONGDESCRIPTIONCONTENTTYPE')),
    url = str(oRepositoryConfig.Get('URL')),

    packages = [str(oRepositoryConfig.Get('PACKAGENAME')),
                str(oRepositoryConfig.Get('PACKAGENAME')) + ".Config",
                str(oRepositoryConfig.Get('PACKAGENAME')) + ".Keywords",
                str(oRepositoryConfig.Get('PACKAGENAME')) + ".Utils",
                str(oRepositoryConfig.Get('PACKAGENAME')) + ".Utils.Events"],

    package_dir = {str(oRepositoryConfig.Get('REPOSITORYNAME')) : str(oRepositoryConfig.Get('PACKAGENAME'))},

    include_package_data = True,

    classifiers = [
        str(oRepositoryConfig.Get('PROGRAMMINGLANGUAGE')),
        str(oRepositoryConfig.Get('LICENCE')),
        str(oRepositoryConfig.Get('OPERATINGSYSTEM')),
        str(oRepositoryConfig.Get('DEVELOPMENTSTATUS')),
        str(oRepositoryConfig.Get('INTENDEDAUDIENCE')),
        str(oRepositoryConfig.Get('TOPIC')),
    ],
    python_requires = str(oRepositoryConfig.Get('PYTHONREQUIRES')),
    cmdclass={
        'install': ExtendedInstallCommand,
    },
    install_requires = oRepositoryConfig.Get('INSTALLREQUIRES'),
    entry_points={
        'console_scripts': oRepositoryConfig.Get('CONSOLESCRIPTS'),
    },
    package_data={f"{oRepositoryConfig.Get('PACKAGENAME')}" : oRepositoryConfig.Get('PACKAGEDATA')},
)
# --------------------------------------------------------------------------------------------------------------

print()
print(COLBG + "Extended installation done")
print()

# --------------------------------------------------------------------------------------------------------------

