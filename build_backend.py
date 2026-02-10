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
Custom Build Backend

Currently reserved for future development
"""

import sys
import logging

from pathlib import Path
from typing import Dict, Optional

from setuptools.build_meta import (
    build_wheel as _build_wheel,
    build_sdist as _build_sdist,
)

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

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
        pass

    def run_pre_build_steps(self) -> int:
        """
Custom build steps
        """
        # logger.info("Entering pre build process")
        # !!! reserved for future development !!!
        # logger.info("Leaving pre build process")

        return SUCCESS

# eof class BuildManager:

build_backend = BuildManager()

def build_wheel(
    wheel_directory: str,
    config_settings: Optional[Dict] = None,
    metadata_directory: Optional[str] = None
) -> str:
    logger.info("Entering build_wheel")
    returnval = build_backend.run_pre_build_steps()
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
    returnval = build_backend.run_pre_build_steps()
    if returnval != SUCCESS:
        raise Exception(f"Execution of pre_build_steps failed with error code {returnval}. Premature end of build_sdist.")
    build_sdist_return = _build_sdist(sdist_directory, config_settings)
    logger.info("Leaving build_sdist")
    return build_sdist_return

# --------------------------------------------------------------------------------------------------------------
