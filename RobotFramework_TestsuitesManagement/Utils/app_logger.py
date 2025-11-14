# **************************************************************************************************************
#
#  Copyright 2020-2025 Robert Bosch GmbH
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
# Defines an application specific logger (for CVersion of TestsuitesManagement only)
# that does not influence other modules.
#
# The robot.api logger must only be used in Python code that is executed as part of a Robot Framework keyword
# execution. But CVersion can also be used stand-alone in pure Python scripts outside the scope of the
# Robot Framework. Therefore, we need to use a pue Python logger. This file contains the definition
# of such a logger.

import logging
import sys

def setup_app_logger(name='TestsuitesManagement', level=logging.INFO):
    """
| Creates a completely isolated, application-specific logger.
| Returnes the creatted logger
    """
    # set the logger name
    logger = logging.getLogger(name)
    
    # prevent inheritance to root logger
    logger.propagate = False
    
    # set the log level
    logger.setLevel(level)
    
    # remove all existing handlers (important in case of reinitializations)
    logger.handlers.clear()
    
    # create a formatter
    formatter = logging.Formatter(
        fmt='[%(name)s] %(message)s',
    )
    
    # add handler to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # currently no own log file handler

    return logger

