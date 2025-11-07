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
# Defines a component specific logger configuration for Robot Framework independent internal loggers
# (used in Python methods)

import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  # loggers shall not influence each other!
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'DEBUG',
        },
        # TODO: which file to be defined
        # 'file': {
            # 'class': 'logging.FileHandler',
            # 'filename': 'app.log',
            # 'formatter': 'standard',
            # 'level': 'DEBUG',
        # },
    },
    'root': {
        'handlers': ['console'], # , 'file'],
        'level': 'DEBUG',
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
