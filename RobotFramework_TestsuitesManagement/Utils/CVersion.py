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
# Validates the current package version with maximum and minimum versions
#
import os
import regex
import json
from enum import Enum
from jsonschema import validate
# # # from RobotFramework_TestsuitesManagement.version import VERSION as TSM_VERSION
# # # from RobotFramework_TestsuitesManagement.version import VERSION_DATE as TSM_VERSION_DATE

import logging # use logger independent from Robot Framework (like defined in app_logger_config)
from RobotFramework_TestsuitesManagement.Utils import app_logger_config
from RobotFramework_TestsuitesManagement.Utils.app_config import AppConfig
from PythonExtensionsCollection.String.CString import CString

# initialize default version logger
applogger = logging.getLogger(__name__)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Unfortunately these global variables are imported several times from outside.
# Therefore, we need to provide them here (but this should be a temporary solution only).
# !!! TODO: Content and usage urgently need to be reworked !!!
BUNDLE_NAME         = None
BUNDLE_VERSION      = None
BUNDLE_VERSION_DATE = None
INSTALLER_LOCATION  = None
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# # # INSTALLER_LOCATION = "https://github.com/test-fullautomation/robotframework-testsuitesmanagement/releases"
# # # BUNDLE_NAME = "RobotFramework_TestsuitesManagement"
# # # BUNDLE_VERSION = TSM_VERSION
# # # BUNDLE_VERSION_DATE = TSM_VERSION_DATE

# # # # Load package context file to get the bundle version
# # # context_filename = "package_context.json"
# # # context_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"Config/{context_filename}")
# # # context_config = None

# # # if os.path.isfile(context_filepath):
    # # # if os.stat(context_filepath).st_size == 0:
        # # # applogger.warn(f"The '{context_filepath}' file is existing but empty.")
    # # # else:
        # # # package_context_schema = {
            # # # "type": "object",
            # # # "additionalProperties": False,
            # # # "properties": {
                # # # "installer_location": {"type": "string"},
                # # # "bundle_name": {"type": "string"},
                # # # "bundle_version": {"type": "string"},
                # # # "bundle_version_date": {"type": "string"}
            # # # },
            # # # "required": ["bundle_name", "bundle_version", "bundle_version_date"]
        # # # }
        # # # try:
            # # # with open(context_filepath) as f:
                # # # context_config = json.load(f)
        # # # except Exception as reason:
            # # # err_msg = f"Cannot load the '{context_filepath}' file. Reason: {reason}"
            # # # applogger.error(err_msg)
            # # # raise Exception(err_msg)
        
        # # # try:
            # # # validate(instance=context_config, schema=package_context_schema)
        # # # except Exception as reason:
            # # # err_msg = f"Invalid '{context_filepath}' file. Reason: {reason}"
            # # # applogger.error(err_msg)
            # # # raise Exception(err_msg)

        # # # if ('installer_location' in context_config) and context_config['installer_location']:
            # # # INSTALLER_LOCATION = context_config['installer_location']
        # # # if ('bundle_name' in context_config) and context_config['bundle_name']:
            # # # BUNDLE_NAME = context_config['bundle_name']
        # # # if ('bundle_version' in context_config) and context_config['bundle_version']:
            # # # BUNDLE_VERSION = context_config['bundle_version']
        # # # if ('bundle_version_date' in context_config) and context_config['bundle_version_date']:
            # # # BUNDLE_VERSION_DATE = context_config['bundle_version_date']


# # # def bundle_version():
   # # # '''
# # # This function prints out the package version which is:

# # # - RobotFramework_TestsuitesManagement version when this module is installed
# # # stand-alone (via `pip` or directly from sourcecode)

# # # - RobotFramework AIO version when this module is bundled with RobotFramework AIO
# # # package

# # # **Arguments:**

# # # * No input parameter is required

# # # **Returns:**

# # # * No return variable
   # # # '''
   # # # print(f"{BUNDLE_VERSION}")


class enVersionCheckResult(Enum):
    """
Defines different states that identify the result of the version check
    """
    # min_version and max_version set to None
    CHECK_NOT_EXECUTED       = "CHECK_NOT_EXECUTED"
    # version check passed
    CHECK_PASSED             = "CHECK_PASSED"
    # version is not valid
    CONFLICT_MIN             = "CONFLICT_MIN"
    CONFLICT_MAX             = "CONFLICT_MAX"
    # internal errors
    WRONG_MINMAX_RELATION    = "WRONG_MINMAX_RELATION"
    FORMAT_ERROR             = "FORMAT_ERROR"
    BUNDLE_CONFIG_FILE_ERROR = "BUNDLE_CONFIG_FILE_ERROR"
    INTERNAL_ERROR           = "INTERNAL_ERROR"

class StatusMessages:
    """
Dictionary wrapper for status messages of version check. Needs to use the same keys like defined in enVersionCheckResult
    """
    def __init__(self):
        self._messages = {
            "CHECK_NOT_EXECUTED"       : "Version check is skipped because both 'min_version' and 'max_version' are set to None",
            "CHECK_PASSED"             : "Version check passed",
            "CONFLICT_MIN"             : "The test execution requires the minimum version '<min_version>', but the reference version '<reference_version>' is older",
            "CONFLICT_MAX"             : "The test execution requires the maximum version '<max_version>', but the reference version '<reference_version>' is younger",
            "WRONG_MINMAX_RELATION"    : "Mismatch of minimum version and maximum version: The minimum version '<min_version>' is younger than the maximum version '<max_version>'",
            "FORMAT_ERROR"             : "A version number has an invalid format: <invalid_format_reason>",
            "BUNDLE_CONFIG_FILE_ERROR" : "A syntax error occurred while accessing or parsing the bundle configuration file",
            "INTERNAL_ERROR"           : "Version could not be verified because of an internal error. Please contact the AIO team"
        }

    def get(self, key, default=None):
        """
Get a status message by key.
        """
        return self._messages.get(key, default)

    def set(self, key, value):
        """
Set a status message.
        """
        self._messages[key] = value

    def __getitem__(self, key):
        """
Allow dict-style access: messages['VALID']
        """
        return self._messages[key]

    def __setitem__(self, key, value):
        """
Allow dict-style assignment: messages['VALID'] = 'text'
        """
        self._messages[key] = value

class CVersion:
    """
Validate a user-defined version against a reference version.

The reference is either:
* the version of the TestsuitesManagement (in case of a stand-alone installation)
* the version of the RobotFramework AIO (TestsuitesManagement is part of a bundle)
    """
    def __init__(self):
        # contains the version number that has an invalid format
        self.__version_number_invalid_format = None
        self.__last_error = None

    # LOW LEVEL
    def verifyVersion(self, min_version=None, max_version=None, reference_version=None):
        """
This method executes the version check, min_version and max_version are checked against the reference_version.

Users can define own reference versions. But if reference_version is None, the internally 
defined bundle_version (either RobotFramework AIO or TestsuitesManagement) will be used as reference.

**Arguments:**

* ``min_version``

   / *Condition*: optional / *Type*: string /

* ``max_version``

   / *Condition*: optional / *Type*: string /

* ``reference_version``

   / *Condition*: optional / *Type*: string /

**Returns:**

* ``result``

  / *Type*: String /

  A token string indicating the result of the vesion check.
        """
        # reinit some flags
        self.__version_number_invalid_format = None
        self.__last_error = None
        app_config = None

        # access to application configuration
        # [] CConfig / [] CKeywords / [X] verifyVersion / [] checkVersion
        try:
            app_config = AppConfig()
        except Exception as ex:
            self.__last_error = f"[verifyVersion]: {ex}"
            applogger.error(self.__last_error)
            return enVersionCheckResult.BUNDLE_CONFIG_FILE_ERROR.value

        # !!! TODO: remove this workaround !!!
        # !!! DOWNWARD COMPATIBILITY ONLY !!!
        global BUNDLE_NAME
        global BUNDLE_VERSION
        global BUNDLE_VERSION_DATE
        global INSTALLER_LOCATION
        BUNDLE_NAME         = app_config.get_bundle_name()
        BUNDLE_VERSION      = app_config.get_bundle_version()
        BUNDLE_VERSION_DATE = app_config.get_bundle_version_date()
        INSTALLER_LOCATION  = app_config.get_bundle_installer_location()
        # !!! DOWNWARD COMPATIBILITY ONLY !!!

        if not reference_version:
            reference_version = app_config.get_reference_version()

        # additional check of possible users input
        if not isinstance(reference_version, str):
            self.__last_error = f"[verifyVersion]: reference_version '{reference_version}' is not of expected format 'str'"
            return enVersionCheckResult.FORMAT_ERROR.value

        # time object variables
        tMinVersion       = None
        tMaxVersion       = None
        tReferenceVersion = None # previously tCurrentVersion
        try:
            tReferenceVersion = self.tupleVersion(reference_version)
        except Exception as ex:
            self.__last_error = f"[verifyVersion]: {ex}"
            return enVersionCheckResult.FORMAT_ERROR.value

        if min_version is None and max_version is None:
            return enVersionCheckResult.CHECK_NOT_EXECUTED.value
        if min_version is not None:
            if not isinstance(min_version, str):
                self.__last_error = f"[verifyVersion]: min_version '{min_version}' is not of expected format 'str'"
                return enVersionCheckResult.FORMAT_ERROR.value
            elif len(min_version.split('.'))>3:
                self.__last_error = f"[verifyVersion]: min_version '{min_version}' contains too many parts (expected is: major.minor.patch)"
                self.__version_number_invalid_format = min_version
                return enVersionCheckResult.FORMAT_ERROR.value
            else:
                try:
                    tMinVersion = self.tupleVersion(min_version)
                except Exception as ex:
                    self.__last_error = f"[verifyVersion]: {ex}"
                    return enVersionCheckResult.FORMAT_ERROR.value
        if max_version is not None:
            if not isinstance(max_version, str):
                self.__last_error = f"[verifyVersion]: max_version '{max_version}' is not of expected format 'str'"
                return enVersionCheckResult.FORMAT_ERROR.value
            elif len(max_version.split('.'))>3:
                self.__last_error = f"[verifyVersion]: max_version '{max_version}' contains too many parts (expected is: major.minor.patch)"
                self.__version_number_invalid_format = max_version
                return enVersionCheckResult.FORMAT_ERROR.value
            else:
                try:
                    tMaxVersion = self.tupleVersion(max_version)
                except Exception as ex:
                    self.__last_error = f"[verifyVersion]: {ex}"
                    return enVersionCheckResult.FORMAT_ERROR.value
        if tMinVersion and tMaxVersion and (tMinVersion > tMaxVersion):
            self.__last_error = "[verifyVersion]: WRONG_MINMAX_RELATION"
            return enVersionCheckResult.WRONG_MINMAX_RELATION.value
        if tMinVersion and not self.bValidateMinVersion(tReferenceVersion, tMinVersion):
            self.__last_error = "[verifyVersion]: CONFLICT_MIN"
            return enVersionCheckResult.CONFLICT_MIN.value
        if tMaxVersion and not self.bValidateMaxVersion(tReferenceVersion, tMaxVersion):
            self.__last_error = "[verifyVersion]: CONFLICT_MAX"
            return enVersionCheckResult.CONFLICT_MAX.value
        return enVersionCheckResult.CHECK_PASSED.value

    # HIGH LEVEL
    def checkVersion(self, min_version=None, max_version=None, reference_version=None, ext_logger=None, status_messages=None):
        '''
This method executes the version check, min_version and max_version are checked against the reference_version.

Users can define own reference versions. But if reference_version is None, the internally defined 
bundle_version will be used as reference.

**Arguments:**

* ``min_version``

   / *Condition*: optional / *Type*: string /

* ``max_version``

   / *Condition*: optional / *Type*: string /

* ``reference_version``

   / *Condition*: optional / *Type*: string /

* ``ext_logger``

   / *Condition*: optional / *Type*: object /

* ``status_messages``

   / *Condition*: optional / *Type*: dict /

**Returns:**

* ``True``

  / *Type*: boolean /

  Executed version check passed or check not executed.

* ``False``

  / *Type*: boolean /

  Executed version check failed.
        '''
        # Caution: Python logger         : logger.warning
        #     But: Robot Framework logger: logger.warn
        # Because of this deviation (and because it is not really required), warning/warn is not used here.
        # Either we use here level 'error' or we raise an exception!
        logger = applogger # default
        if ext_logger:
            # user want to use own logger
            logger = ext_logger

        # either use predefined status messages or user defined status messages
        if not status_messages:
            status_messages = StatusMessages()

        # access to application configuration
        # [] CConfig / [] CKeywords / [] verifyVersion / [X] checkVersion
        try:
            app_config = AppConfig()
        except Exception as ex:
            logger.error(f"[checkVersion]: {ex}")
            raise Exception(f"Execution will be aborted because it's not possible to load the application configuration")

        # get and log the result of the version check
        result = self.verifyVersion(min_version, max_version, reference_version)
        status_message = status_messages[result]

        # apply current calues
        if min_version:
            status_message = status_message.replace('<min_version>', min_version)
        if max_version:
            status_message = status_message.replace('<max_version>', max_version)
        if self.__last_error:
            status_message = status_message.replace('<invalid_format_reason>', self.__last_error)
        else:
            status_message = status_message.replace('<invalid_format_reason>', "reason not available")

        # add app specific information
        if reference_version:
            # reference_version is set by user (as checkVersion parameter)
            reference_app_name = None # if reference_version is set by user, we do not have a corresponding name for an application
        else:
            # get the reference version and reference app name from app config
            reference_version = app_config.get_reference_version()
            reference_app_name = app_config.get_reference_app_name()
        status_message = status_message.replace('<reference_version>', reference_version)
        if reference_app_name:
            # add the name of the applictaion used as reference
            status_message = f"{status_message} ({reference_app_name})"

        # Mapping between the result of the version check and the reaction on this result
        # 1. premature end of execution because of errors
        if result in (enVersionCheckResult.WRONG_MINMAX_RELATION.value,
                      enVersionCheckResult.FORMAT_ERROR.value,
                      enVersionCheckResult.INTERNAL_ERROR.value):
            logger.error(f"{status_message}")
            raise Exception("Execution will be aborted because of a critical version number issue")
        elif result in (enVersionCheckResult.CONFLICT_MIN.value,
                        enVersionCheckResult.CONFLICT_MAX.value):
            logger.error(f"Version check failed: {status_message}")
            raise Exception("Execution will be aborted because of a failed version check")

        # 2. the good case
        logger.info(f"{status_message}")
        return True # belongs to remaining states: "CHECK_NOT_EXECUTED" and "CHECK_PASSED" (positive result that allows the test execution to continue)


    def get_last_error(self):
        """
Returns the most recently occurred error (during execution of low level method verifyVersion)
        """
        return self.__last_error

    def get_version_number_invalid_format(self):
        # TODO: currently used in versionCheck of CConfig.
        #       better solution needed; this method should be removed later
        """
Returns the version number with invalid format
        """
        return self.__version_number_invalid_format


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
            raise Exception(f"Invalid version format '{sVersion}'")
        
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
            raise Exception(f"{error} (within '{sVersion}')")


