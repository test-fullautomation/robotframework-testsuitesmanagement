#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
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
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    include_package_data = True,
    name = "RobotFramework_Testsuites",
    version = "0.1.0",
    author = "Mai Dinh Nam Son <son.maidinhnam@vn.bosch.com>, Thomas Pollerspoeck <thomas.pollerspoeck@de.bosch.com>",
    description = "This package provide a testsuites management for RobotFramework AIO",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://sourcecode.socialcoding.bosch.com/projects/ROBFW/repos/robotframework-testsuitesmanagement/browse",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.9',
    entry_points={
        'console_scripts': [
            'robfwaio_version = RobotFramework_Testsuites.version:robfwaio_version',
        ]
    }
)