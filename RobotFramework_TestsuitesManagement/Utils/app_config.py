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
# Contains all kind of information belonging to the TestsuitesManagement itself (also the RobotFramework AIO if installed).
#
import os
import json
from jsonschema import validate
from RobotFramework_TestsuitesManagement.version import VERSION as TSM_VERSION
from RobotFramework_TestsuitesManagement.version import VERSION_DATE as TSM_VERSION_DATE
from PythonExtensionsCollection.String.CString import CString

# content check of RobotFramework AIO configuration file 'package_context.json'
PACKAGE_CONTEXT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "installer_location": {"type": "string"},
        "bundle_name": {"type": "string"},
        "bundle_version": {"type": "string"},
        "bundle_version_date": {"type": "string"}
    },
    "required": ["installer_location", "bundle_name", "bundle_version", "bundle_version_date"]
}

class AppConfig:
    """
Configuration class that contains all the information about the application.
    """
    def __init__(self):

        # * tsm_version, tsm_version_date, tsm_app_name, tsm_installer_location
        #   belong to the TestsuitesManagement (this application).
        # * bundle_version, bundle_version_date, bundle_name, bundle_installer_location
        #   belong to the entire bundle (RobotFramework AIO).
        # * reference_version, reference_version_date, reference_app_name, reference_installer_location
        #   belong either to the TestsuitesManagement or to the RobotFramework AIO, depending on the existence
        #   of a certain RobotFramework AIO configuration file (package_context.json).
        #   reference_... is used for the version control.

        # === (1) Information about this application
        self.__tsm_version            = TSM_VERSION
        self.__tsm_version_date       = TSM_VERSION_DATE
        self.__tsm_app_name           = "RobotFramework_TestsuitesManagement"
        self.__tsm_installer_location = "https://github.com/test-fullautomation/robotframework-testsuitesmanagement/releases"
        # default (assumed to be this application = standalone installation of TestsuitesManagement):
        self.__reference_version            = self.__tsm_version
        self.__reference_version_date       = self.__tsm_version_date
        self.__reference_app_name           = self.__tsm_app_name
        self.__reference_installer_location = self.__tsm_installer_location

        # === (2) Information about the entire RobotFramework AIO bundle (if available)
        # Detect if TestsuitesManagement is installed standalone or as part of the RobotFramework AIO.
        # This depends on the existence of a file named 'package_context.json' within the 'Config' folder
        # of the TestsuitesManagement installation.
        self.__bundle_version            = None
        self.__bundle_version_date       = None
        self.__bundle_name               = None
        self.__bundle_installer_location = None
        self.__is_robotframework_aio     = False
        absolute_reference_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        self.__aio_package_context_file = CString.NormalizePath("Config/package_context.json", sReferencePathAbs=absolute_reference_path)
        if os.path.isfile(self.__aio_package_context_file):
            # File indicating a RobotFramework AIO installation found. Reading reference information from there.
            aio_package_context = None
            if os.stat(self.__aio_package_context_file).st_size == 0:
                err_msg = f"The RobotFramework AIO package context file is existing, but completely empty ({self.__aio_package_context_file})."
                raise Exception(f"{err_msg}")
            try:
                with open(self.__aio_package_context_file) as file:
                    aio_package_context = json.load(file)
            except Exception as reason:
                # err_msg = f"Cannot load the RobotFramework AIO package context file '{aio_package_context}' file. Reason: {reason}"
                # or maybe shorter
                err_msg = f"{reason} (file '{self.__aio_package_context_file}')"
                raise Exception(f"{err_msg}")
            try:
                validate(instance=aio_package_context, schema=PACKAGE_CONTEXT_SCHEMA)
            except Exception as reason:
                # err_msg = f"Invalid content of file '{self.__aio_package_context_file}' file. Reason: {reason}"
                # or maybe shorter
                err_msg = f"{reason.message} (file '{self.__aio_package_context_file}')"
                raise Exception(f"{err_msg}")

            if aio_package_context.get('installer_location'):
                self.__bundle_installer_location = aio_package_context['installer_location']
            if aio_package_context.get('bundle_name'):
                self.__bundle_name = aio_package_context['bundle_name']
            if aio_package_context.get('bundle_version'):
                self.__bundle_version = aio_package_context['bundle_version']
            if aio_package_context.get('bundle_version_date'):
                self.__bundle_version_date = aio_package_context['bundle_version_date']

            # paranoia check
            if (self.__bundle_installer_location is None) or (self.__bundle_name is None) or (self.__bundle_version is None) or (self.__bundle_version_date is None):
                # (but already PACKAGE_CONTEXT_SCHEMA should prevent this)
                err_msg = f"Incomplete package context file '{self.__aio_package_context_file}'"
                raise Exception(f"{err_msg}")

            # set the reference to the bundle (because TestsuitesManagement is part of RobotFramework AIO)
            self.__reference_version            = self.__bundle_version
            self.__reference_version_date       = self.__bundle_version_date
            self.__reference_app_name           = self.__bundle_name
            self.__reference_installer_location = self.__bundle_installer_location
            self.__is_robotframework_aio        = True
        else:
            self.__aio_package_context_file = None
        # eof else - if os.path.isfile(self.__aio_package_context_file):

    # eof def __init__(self):

    def is_robotframework_aio(self):
        """
Returns
* ``True``: RobotFramework AIO is installed
* ``False``: RobotFramework AIO is not installed (= standalone installation of TestsuitesManagement)
        """
        return self.__is_robotframework_aio

    def get_package_context_file(self):
        """
Returns path and name of package context file
        """
        return self.__aio_package_context_file

    def get_reference_version(self):
        """
Returns the version number used as reference for version checks. The reference is either the RobotFramework AIO
or the TestsuitesManagement, depending on what is installed.
        """
        return self.__reference_version

    def get_reference_version_date(self):
        """
Returns the version date belonging to the reference. The reference is either the RobotFramework AIO
or the TestsuitesManagement, depending on what is installed.
        """
        return self.__reference_version_date

    def get_reference_app_name(self):
        """
Returns the name of the reference application. The reference is either the RobotFramework AIO
or the TestsuitesManagement, depending on what is installed.
        """
        return self.__reference_app_name

    def get_reference_installer_location(self):
        """
Returns the location of the reference installer. The reference is either the RobotFramework AIO
or the TestsuitesManagement, depending on what is installed.
        """
        return self.__reference_installer_location

    def get_tsm_version(self):
        """
Returns the version of the TestsuitesManagement.
        """
        return self.__tsm_version

    def get_tsm_version_date(self):
        """
Returns the version date of the TestsuitesManagement.
        """
        return self.__tsm_version_date

    def get_tsm_app_name(self):
        """
Returns the application name of the TestsuitesManagement.
        """
        return self.__tsm_app_name

    def get_tsm_installer_location(self):
        """
Returns the location of the TestsuitesManagement installer.
        """
        return self.__tsm_installer_location

    def get_bundle_version(self):
        """
Returns the version of the entire RobotFramework AIO bundle.
        """
        return self.__bundle_version

    def get_bundle_version_date(self):
        """
Returns the version date of the entire RobotFramework AIO bundle.
        """
        return self.__bundle_version_date

    def get_bundle_name(self):
        """
Returns the name of the entire RobotFramework AIO bundle.
        """
        return self.__bundle_name

    def get_bundle_installer_location(self):
        """
Returns the location of the installer of the entire RobotFramework AIO bundle.
        """
        return self.__bundle_installer_location

    # TODO:
    # def dump_app_config(self):
        # all versions, dates, names

# eof class AppConfig:

