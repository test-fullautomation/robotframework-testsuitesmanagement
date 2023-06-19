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
# readme.rst2md.py
#
# XC-CT/ECA3-Queckenstedt
#
# --------------------------------------------------------------------------------------------------------------
#
# Little helper to convert the README.rst file within this repository separately to md format (README.md).
# This is what also the setup.py does during installation.
#
# In both cases the philosophy is: The rst file is the master. The user has to maintain this version
# of the README. The md version is generated automatically out of the rst version.
#
# --------------------------------------------------------------------------------------------------------------
#
# 24.10.2022
#
# --------------------------------------------------------------------------------------------------------------

import os, sys

from config.CRepositoryConfig import CRepositoryConfig # providing repository and environment specific information
from additions.CExtendedSetup import CExtendedSetup # providing functions to support the extended setup process

import colorama as col

col.init(autoreset=True)

COLBR = col.Style.BRIGHT + col.Fore.RED

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg):
    sys.stderr.write(COLBR + f"Error: {sMsg}!\n")

def printexception(sMsg):
    sys.stderr.write(COLBR + f"Exception: {sMsg}!\n")

# --------------------------------------------------------------------------------------------------------------

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

nReturn = oExtendedSetup.convert_repo_readme()

sys.exit(nReturn)

# --------------------------------------------------------------------------------------------------------------

