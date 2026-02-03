# **************************************************************************************************************
#
#  Copyright 2020-2026 Robert Bosch GmbH
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
"""
Custom Build Backend including additional installation steps like

* Documentation rendering

All data needed to do this are taken from the repository configuration.
No define of any paths here.
"""

import os
import sys
import logging
import subprocess
import shlex

from pathlib import Path
from typing import Dict, Optional

import wheel.wheelfile

from setuptools.build_meta import (
    build_wheel as _build_wheel,
    build_sdist as _build_sdist,
)

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.CRepositoryConfig import CRepositoryConfig # provides repository and environment specific information

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------------------------

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

class BuildManager:
    """
Custom Build Backend
    """

    def __init__(self):
        self.project_root = Path(__file__).parent

        # setup of repository configuration
        self.repository_config = None
        try:
            self.repository_config = CRepositoryConfig(f"{__file__}")
        except Exception as ex:
            logger.critical(str(ex))
            raise Exception(str(ex))

    def genpackagedoc(self):
        """
Executes the documentation builder
        """

        DOCUMENTATIONBUILDER = self.repository_config.Get('DOCUMENTATIONBUILDER')
        PYTHON = self.repository_config.Get('PYTHON')

        listCmdLineParts = []
        listCmdLineParts.append(f"\"{PYTHON}\"")
        listCmdLineParts.append(f"\"{DOCUMENTATIONBUILDER}\"")
        sCmdLine = " ".join(listCmdLineParts)
        del listCmdLineParts
        listCmdLineParts = shlex.split(sCmdLine)
        # -- debug
        sCmdLine = " ".join(listCmdLineParts)
        logger.info(f"Executing: '{sCmdLine}'")
        nReturn = ERROR
        try:
            nReturn = subprocess.call(listCmdLineParts)
        except Exception as ex:
            logger.error(str(ex))
            return ERROR
        return nReturn
    # eof def genpackagedoc():

    def run_pre_build_steps(self) -> None:
        """
Custom build steps
        """
        logger.info("Entering pre build process")

        logger.info("Rendering documentation")
        returnval = None
        try:
            returnval = self.genpackagedoc()
            logger.info(f"Documentation renderer returned '{returnval}'")
        except Exception as ex:
            logger.error(str(ex))
            return ERROR
        if returnval != SUCCESS:
            return returnval

        logger.info("Leaving pre build process")

        return SUCCESS

# eof class BuildManager:

_manager = BuildManager()

def build_wheel(
    wheel_directory: str,
    config_settings: Optional[Dict] = None,
    metadata_directory: Optional[str] = None
) -> str:
    logger.info("Entering build_wheel")
    returnval = _manager.run_pre_build_steps()
    if returnval != SUCCESS:
        raise Exception(f"Execution of pre_build_steps failed with error code {returnval}. Premature end of build_wheel.")
    build_wheel_return = _build_wheel(wheel_directory, config_settings, metadata_directory)
    logger.info("Leaving build_wheel")
    return build_wheel_return


def build_sdist(
    sdist_directory: str,
    config_settings: Optional[Dict] = None
) -> str:
    logger.info("Entering build_sdist")
    returnval = _manager.run_pre_build_steps()
    if returnval != SUCCESS:
        raise Exception(f"Execution of pre_build_steps failed with error code {returnval}. Premature end of build_sdist.")
    build_sdist_return = _build_sdist(sdist_directory, config_settings)
    logger.info("Leaving build_sdist")
    return build_sdist_return

# --------------------------------------------------------------------------------------------------------------
