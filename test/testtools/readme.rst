.. Copyright 2020-2024 Robert Bosch GmbH

.. Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

.. http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


Code snippet generator
======================

GenSnippetsTSM.py

XC-HWP/ESW3-Queckenstedt

04.03.2024

**GenSnippetsTSM** generates and executes **TestsuitesManagement** related code snippets.

The base of the code snippets generation is mainly a combination of code patterns and lists of expressions
that are combined under several conditions. The goal is to have *stuff* to test the **TestsuitesManagement**.

The snippets together with the computed results are written to a log file in text format (to support diffs)
and to a report file in HTML format (to support better readibility by colored text).

Currently **GenSnippetsTSM** is a one-file tool; no separate configuration files, no command line parameter.

All code pattern are defined directly within class 'CSnippets()'.

Output files are written to script folder.

The purpose behind this script is not to have an automated test. Only in some snippets a valuation of results is done (where possible).
Because most of the snippets are created automatically, it is difficult (and not done here) to create the expected results also in an automated way.
It's on the user to interprete the results. **GenSnippetsTSM** only produces these results.
