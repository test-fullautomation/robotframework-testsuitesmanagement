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

from robot.api.deco import keyword, not_keyword
from robot.utils import is_string

class COnFailureHandle():

    @not_keyword
    def is_noney(self, item):
        return item is None or is_string(item) and item.upper() == 'NONE'

    # @keyword
    # def register_keyword_run_on_failure(self, keyword):
    #     '''
    #     TBD
    #     '''
