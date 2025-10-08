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
# Validates the current package version with maximum and minimum versions
#
import os
import regex
import json
from enum import Enum
from jsonschema import validate
from robot.api import logger
from RobotFramework_TestsuitesManagement.version import VERSION, VERSION_DATE

INSTALLER_LOCATION = "https://github.com/test-fullautomation/robotframework-testsuitesmanagement/releases"
BUNDLE_NAME = "RobotFramework_TestsuitesManagement"
BUNDLE_VERSION = VERSION
BUNDLE_VERSION_DATE = VERSION_DATE

# Load package context file
context_filename = "package_context.json"
context_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"Config/{context_filename}")
context_config = None

if os.path.isfile(context_filepath):
    if os.stat(context_filepath).st_size == 0:
        logger.warn(f"The '{context_filepath}' file is existing but empty.")
    else:
        package_context_schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "installer_location": {"type": "string"},
                "bundle_name": {"type": "string"},
                "bundle_version": {"type": "string"},
                "bundle_version_date": {"type": "string"}
            },
            "required": ["bundle_name", "bundle_version", "bundle_version_date"]
        }
        try:
            with open(context_filepath) as f:
                context_config = json.load(f)
        except Exception as reason:
            errorMsg = f"Cannot load the '{context_filepath}' file. Reason: {reason}"
            logger.error(errorMsg)
            raise Exception(errorMsg)
        
        try:
            validate(instance=context_config, schema=package_context_schema)
        except Exception as reason:
            errorMsg = f"Invalid '{context_filepath}' file. Reason: {reason}"
            logger.error(errorMsg)
            raise Exception(errorMsg)

        if ('installer_location' in context_config) and context_config['installer_location']:
            INSTALLER_LOCATION = context_config['installer_location']
        if ('bundle_name' in context_config) and context_config['bundle_name']:
            BUNDLE_NAME = context_config['bundle_name']
        if ('bundle_version' in context_config) and context_config['bundle_version']:
            BUNDLE_VERSION = context_config['bundle_version']
        if ('bundle_version_date' in context_config) and context_config['bundle_version_date']:
            BUNDLE_VERSION_DATE = context_config['bundle_version_date']

def bundle_version():
   '''
This function prints out the package version which is:

- RobotFramework_TestsuitesManagement version when this module is installed
stand-alone (via `pip` or directly from sourcecode)

- RobotFramework AIO version when this module is bundled with RobotFramework AIO
package

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
   '''
   print(f"{BUNDLE_VERSION}")

class enVersionCheckResult(Enum):
    WITHOUTVERSION = "without_version_check"
    WRONGMINMAX    = "wrong_minmax"
    CONFLICTMIN    = "conflict_min"
    CONFLICTMAX    = "conflict_max"
    UNKNOWN        = "internal_error" # error when reading the RobotFramework AIO bundle version 

class CVersion():
    '''
Validates a bundle version of an installed package
    '''
    def __init__(self):
        self.reason = None

    def verifyVersion(self, min_version='', max_version=''):
        '''
This method verifyVersion validates the current ROBFW-AIO package version with maximum and minimum version.

The package version is the version when this module is installed stand-alone

**Arguments:**

* ``min_version``

   / *Condition*: optional / *Type*: string /

* ``max_version``

   / *Condition*: optional / *Type*: string /

**Returns:**

* ``response``

  / *Type*: boolean /

  ``True`` if version checking is fine else ``False``. 

  * ``reason``

  / *Type*: String /

  A short reason if version checking is failed. 
        '''
        if not isinstance(min_version, str):
            if min_version is None:
                min_version = ''
            else:
                raise Exception(f"The minimum version requires a string format, but the type is '{type(min_version)}'")
        if  not isinstance(max_version, str):
            if max_version is None:
                max_version = ''
            else:
                raise Exception(f"The maximum version requires a string format, but the type is '{type(max_version)}'")
        try:
            tCurrentVersion = self.tupleVersion(BUNDLE_VERSION)
        except:
            self.reason = enVersionCheckResult.UNKNOWN.value
            return False, self.reason
        # Verify format of provided min and max versions then parse to tuples
        tMinVersion = None
        tMaxVersion = None
        if min_version.strip() == '' and max_version.strip() == '':
            self.reason = enVersionCheckResult.WITHOUTVERSION.value
            return None, self.reason
        if min_version != '':
            tMinVersion = self.tupleVersion(min_version)
        if max_version != '':
            tMaxVersion = self.tupleVersion(max_version)
        if tMinVersion and tMaxVersion and (tMinVersion > tMaxVersion):
            self.reason = enVersionCheckResult.WRONGMINMAX.value
            return False, self.reason
        if tCurrentVersion is not None:
            if tMinVersion and not self.bValidateMinVersion(tCurrentVersion, tMinVersion):
                self.reason = enVersionCheckResult.CONFLICTMIN.value
                return False, self.reason
            if tMaxVersion and not self.bValidateMaxVersion(tCurrentVersion, tMaxVersion):
                self.reason = enVersionCheckResult.CONFLICTMAX.value
                return False, self.reason
        return True, self.reason

    @staticmethod
    def bValidateMinVersion(tCurrentVersion, tMinVersion):
        '''
This bValidateMinVersion validates the current version with required minimun version.

**Arguments:**

* ``tCurrentVersion``

  / *Condition*: required / *Type*: tuple /

  Current package version.

* ``tMinVersion``

  / *Condition*: required / *Type*: tuple /

  The minimum version of package.

**Returns:**

* ``True`` or ``False``
        '''
        return tCurrentVersion >= tMinVersion
    
    @staticmethod
    def bValidateMaxVersion(tCurrentVersion, tMaxVersion):
        '''
This bValidateMaxVersion validates the current version with required minimum version.

**Arguments:**

* ``tCurrentVersion``

  / *Condition*: required / *Type*: tuple /

  Current package version.

* ``tMaxVersion``

  / *Condition*: required / *Type*: tuple /

  The maximum version of package.

**Returns:**

* ``True or False``
        '''
        return tCurrentVersion <= tMaxVersion
    
    @staticmethod
    def bValidateSubVersion(sVersion):
        '''
This bValidateSubVersion validates the format of provided sub version and parse
it into sub tuple for version comparision.

**Arguments:**

* ``sVersion``

  / *Condition*: required / *Type*: string /

  The version of package.

**Returns:**

* ``lSubVersion``

  / *Type*: tuple /
        '''
        lSubVersion = [0,0,0]
        oMatch = regex.match(r"^(\d+)(?:-?(a|b|rc)(\d*))?$", sVersion)
        if oMatch:
            lSubVersion[0] = int(oMatch.group(1))
            # a < b < rc < released (without any character)
            if oMatch.group(2):
                if oMatch.group(2) == 'a':
                    lSubVersion[1] = 0
                elif oMatch.group(2) == 'b':
                    lSubVersion[1] = 1
                elif oMatch.group(2) == 'rc':
                    lSubVersion[1] = 2
            else:
                lSubVersion[1] = 3

            if oMatch.group(3):
                lSubVersion[2] = int(oMatch.group(3))
            else:
                lSubVersion[2] = 0

            return tuple(lSubVersion)
        else:
            raise Exception("Wrong format in version information")
        
    @staticmethod
    def tupleVersion(sVersion):
        '''
This tupleVersion returns a tuple which contains the (major, minor, patch) version.

In case minor/patch version is missing, it is set to 0.
E.g: "1" is transformed to "1.0.0" and "1.1" is transformed to "1.1.0"

This tupleVersion also support version which contains Alpha (a), Beta (b) or
Release candidate (rc): E.g: "1.2rc3", "1.2.1b1", ...

**Arguments:**

* ``sVersion``

  / *Condition*: required / *Type*: string /

  The version of package.

**Returns:**

* ``lVersion``

  / *Type*: tuple /

  A tuple which contains the (major, minor, patch) version.


        '''
        lVersion = sVersion.split(".")
        if len(lVersion) == 1:
            lVersion.extend(["0", "0"])
        elif len(lVersion) == 2:
            lVersion.append("0")
        elif len(lVersion) >= 3:
            # Just ignore and remove the remaining
            lVersion = lVersion[:3]
        try:
            # verify the version info is a number
            return tuple(map(lambda x: CVersion.bValidateSubVersion(x), lVersion))
        except Exception as error:
            raise Exception(f"{error} '{sVersion}'")