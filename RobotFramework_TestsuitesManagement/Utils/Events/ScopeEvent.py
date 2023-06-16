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

from robot.libraries.BuiltIn import BuiltIn

from .Event import Event


class ScopeEvent(Event):

    def __init__(self, scope, action, *args, **kwargs):
        self.scope = scope
        self.action = action
        self.args = args
        self.kwargs = kwargs

        if scope == 'current':
            suite = BuiltIn().get_variable_value('${SUITE NAME}')
            test = BuiltIn().get_variable_value('${TEST NAME}', '')
            self.scope = suite + '.' + test if test != '' else suite

    def trigger(self, *args, **kwargs):
        if args[0] == self.scope:
            self.action(*self.args, **self.kwargs)


class ScopeStart(ScopeEvent):
    name = 'scope_start'

class ScopeEnd(ScopeEvent):
    name = 'scope_end'
