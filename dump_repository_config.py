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
# dump_repository_config.py
#
# XC-CT/ECA3-Queckenstedt
#
# dump_repository_config.py is a little helper to get deeper knowledge about the environment under which
# the software in this repository is being executed.
#
# The script prints all repository configuration values to console:
# Reference:
# - config\repository_config.json
# - config\CRepositoryConfig.py
#
# --------------------------------------------------------------------------------------------------------------
#
import os, sys

import colorama as col

from config.CRepositoryConfig import CRepositoryConfig

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

# -- setting up the repository configuration (relative to the path of this script)
oRepositoryConfig = None
try:
    oRepositoryConfig = CRepositoryConfig(os.path.abspath(sys.argv[0]))
except Exception as ex:
    print()
    printexception(str(ex))
    print()
    sys.exit(ERROR)

# --------------------------------------------------------------------------------------------------------------

print(COLBG + "Repository configuration dump done")
print()
sys.exit(SUCCESS)

# --------------------------------------------------------------------------------------------------------------

