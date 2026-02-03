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
# CRepositoryConfig.py
#
# XC-HWP/ESW3-Queckenstedt
#
# Purpose:
# - Compute and store all repository specific information, like the repository name,
#   paths to repository subfolder, paths to interpreter and so on ...
#
# - All paths to subfolder depends on the repository root path that has to be provided
#   to constructor of CRepositoryConfig
#
# --------------------------------------------------------------------------------------------------------------
#
# 03.02.2026
#
# --------------------------------------------------------------------------------------------------------------

import os, sys, platform, shlex, subprocess, json
import colorama as col
import tomllib

from PythonExtensionsCollection.String.CString import CString

# because of partially same names for packace constants and meta information constants we do a mapping here
from RobotFramework_TestsuitesManagement.version import VERSION as PACKAGEVERSION
from RobotFramework_TestsuitesManagement.version import VERSION_DATE as PACKAGEVERSIONDATE

col.init(autoreset=True)
COLBR = col.Style.BRIGHT + col.Fore.RED
COLBG = col.Style.BRIGHT + col.Fore.GREEN

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg):
    sys.stderr.write(COLBR + f"Error: {sMsg}!\n")

def printexception(sMsg):
    sys.stderr.write(COLBR + f"Exception: {sMsg}!\n")

# --------------------------------------------------------------------------------------------------------------

class CRepositoryConfig():

    def __init__(self, sCalledBy=None):
        pass
        # TODO: error handling sCalledBy=None
        sCalledBy = CString.NormalizePath(sCalledBy)
        self.__sReferencePath = os.path.dirname(sCalledBy)

        self.__dictRepositoryConfig = None # initialized below by json.load()

        # load static configuration values (name of json file is fix)
        sRepositoryConfigurationFile = CString.NormalizePath(f"{self.__sReferencePath}/config/repository_config.json")
        hRepositoryConfigurationFile = open(sRepositoryConfigurationFile, encoding="utf-8")
        self.__dictRepositoryConfig = json.load(hRepositoryConfigurationFile)
        hRepositoryConfigurationFile.close()

        # add further infos
        # (to have the possibility to print out all values with help of 'PrintConfig()')
        self.__dictRepositoryConfig['CALLEDBY']                    = sCalledBy
        self.__dictRepositoryConfig['CWD']                         = os.getcwd()
        self.__dictRepositoryConfig['REFERENCEPATH']               = self.__sReferencePath
        self.__dictRepositoryConfig['REPOSITORYCONFIGURATIONFILE'] = sRepositoryConfigurationFile

        # add version and date of the package this repository configuration belongs to
        self.__dictRepositoryConfig['PACKAGEVERSION'] = PACKAGEVERSION
        self.__dictRepositoryConfig['PACKAGEDATE']    = PACKAGEVERSIONDATE

        # make absolute path to package documentation
        self.__dictRepositoryConfig['PACKAGEDOC'] = CString.NormalizePath(sPath=self.__dictRepositoryConfig['PACKAGEDOC'], sReferencePathAbs=self.__sReferencePath)

        # read additional values from TOML configuration file
        toml_data = None
        toml_file = f"{self.__sReferencePath}/pyproject.toml"
        self.__dictRepositoryConfig['TOMLCONFIGURATIONFILE'] = toml_file
        with open(toml_file, "rb") as f:
            toml_data = tomllib.load(f)
        authors = toml_data["project"]["authors"]
        author = authors[0] if authors else "(not found)"
        self.__dictRepositoryConfig['AUTHOR'] = author['name']
        self.__dictRepositoryConfig['AUTHOREMAIL'] = author['email']
        self.__dictRepositoryConfig['PACKAGENAME'] = toml_data["project"]["name"]
        self.__dictRepositoryConfig['DESCRIPTION'] = toml_data["project"]["description"]
        self.__dictRepositoryConfig['BUILDREQUIRES'] = toml_data["build-system"]["requires"]
        self.__dictRepositoryConfig['EXECUTIONREQUIRES'] = toml_data["project"]["dependencies"]
        self.__dictRepositoryConfig['PYTHON_REQUIRED'] = toml_data["project"]["requires-python"]
        self.__dictRepositoryConfig['LICENSE'] = toml_data["project"]["license"]
        self.__dictRepositoryConfig['KEYWORDS'] = toml_data["project"]["keywords"]
        # currently skipped because too much content for nice console output:
        # self.__dictRepositoryConfig['classifiers'] = toml_data["project"]["classifiers"]
        self.__dictRepositoryConfig['DYNAMIC_VALUES'] = toml_data["project"]["dynamic"]
        # save access to optional values
        project = toml_data.get("project", {})
        optional_dependencies = project.get("optional-dependencies", {})
        self.__dictRepositoryConfig['OPTIONAL_DEPENDENCIES'] = optional_dependencies.get("dev", {})
        self.__dictRepositoryConfig['DOC_DEPENDENCIES'] = optional_dependencies.get("docs", {})
        urls = project.get("urls", {})
        self.__dictRepositoryConfig['URL_HOMEPAGE'] = urls.get("Homepage", {})
        self.__dictRepositoryConfig['URL_DOCUMENTATION'] = urls.get("Documentation", {})
        self.__dictRepositoryConfig['URL_README'] = urls.get("Readme", {})
        self.__dictRepositoryConfig['URL_REPOSITORY'] = urls.get("Repository", {})
        self.__dictRepositoryConfig['URL'] = urls.get("Repository", {}) # !!! downward compatibility to older version of GenpackageDoc / to be removed later
        self.__dictRepositoryConfig['URL_ISSUES'] = urls.get("Issues", {})
        tool = toml_data.get("tool", {})
        setuptools = tool.get("setuptools", {})
        package_data = setuptools.get("package-data", {})
        self.__dictRepositoryConfig['PACKAGE_DATA'] = package_data.get(self.__dictRepositoryConfig['PACKAGENAME'], {})

        # compute dynamic configuration values
        bSuccess, sResult = self.__InitConfig()
        if bSuccess != True:
            raise Exception(sResult)
        print(COLBG + sResult)
        print()


    def __del__(self):
        del self.__dictRepositoryConfig


    def __InitConfig(self):

        sOSName         = os.name
        sPlatformSystem = platform.system()
        sPythonPath     = CString.NormalizePath(os.path.dirname(sys.executable))
        sPython         = CString.NormalizePath(sys.executable)
        sPythonVersion  = sys.version

        sInstalledPackageFolder = None

        if sPlatformSystem == "Windows":
            sInstalledPackageFolder = f"{sPythonPath}/Lib/site-packages/" + self.__dictRepositoryConfig['PACKAGENAME']
        elif sPlatformSystem == "Linux":
            sInstalledPackageFolder = f"{sPythonPath}/../lib/python3.9/site-packages/" + self.__dictRepositoryConfig['PACKAGENAME']
        else:
            bSuccess = False
            sResult  = f"Operating system {sPlatformSystem} ({sOSName}) not supported"
            return bSuccess, sResult

        self.__dictRepositoryConfig['OSNAME']                 = sOSName
        self.__dictRepositoryConfig['PLATFORMSYSTEM']         = sPlatformSystem
        self.__dictRepositoryConfig['PYTHON']                 = sPython
        self.__dictRepositoryConfig['PYTHONVERSION']          = sPythonVersion
        self.__dictRepositoryConfig['INSTALLEDPACKAGEFOLDER'] = sInstalledPackageFolder

        # ---- paths relative to repository root folder (where the scripts are located that use this module)

        # ====== 1. documentation

        # The following key doesn't matter in case of the documentation builder itself is using this CRepositoryConfig.
        # But if the documentation builder is called by other apps like setup.py, they need to know where to find.
        self.__dictRepositoryConfig['DOCUMENTATIONBUILDER'] = CString.NormalizePath(f"{self.__sReferencePath}/genpackagedoc.py")

        # - folder containing the package source files (will also contain the PDF documentation)
        self.__dictRepositoryConfig['PACKAGESOURCEFOLDER'] = CString.NormalizePath(f"{self.__sReferencePath}/{self.__dictRepositoryConfig['PACKAGENAME']}")

        # ====== 2. PIP/TOML/setuptools

        self.__dictRepositoryConfig['SETUPBUILDFOLDER']           = CString.NormalizePath(f"{self.__sReferencePath}/build")
        # TODO: check if still required: self.__dictRepositoryConfig['SETUPBUILDLIBFOLDER']        = CString.NormalizePath(f"{self.__sReferencePath}/build/lib")
        # TODO: check if still required: self.__dictRepositoryConfig['SETUPBUILDLIBPACKAGEFOLDER'] = CString.NormalizePath(f"{self.__sReferencePath}/build/lib/{self.__dictRepositoryConfig['PACKAGENAME']}")
        # deprecated: self.__dictRepositoryConfig['SETUPDISTFOLDER']            = CString.NormalizePath(f"{self.__sReferencePath}/dist")
        EGGINFOFOLDER = self.__dictRepositoryConfig['PACKAGENAME'].replace('-', '_')
        self.__dictRepositoryConfig['EGGINFOFOLDER']              = CString.NormalizePath(f"{self.__sReferencePath}/{EGGINFOFOLDER}.egg-info")

        print()
        print(f"Running under {sPlatformSystem} ({sOSName})")
        self.PrintConfig()

        bSuccess = True
        sResult  = "Repository setup done"
        return bSuccess, sResult

    # eof def __InitConfig(self):


    def PrintConfig(self):
        # -- printing configuration to console
        nJust = 30
        print()
        for sKey in self.__dictRepositoryConfig:
            print(sKey.rjust(nJust, ' ') + " : " + str(self.__dictRepositoryConfig[sKey]))
        print()
    # eof def PrintConfig(self):


    def Get(self, sName=None):
        if ( (sName is None) or (sName not in self.__dictRepositoryConfig) ):
            print()
            printerror(f"Error: Configuration parameter '{sName}' not existing!")
            # from here it's standard output:
            print("Use instead one of:")
            self.PrintConfig()
            return None # returning 'None' in case of key is not existing !!!
        else:
            return self.__dictRepositoryConfig[sName]
    # eof def Get(self, sName=None):


    def GetConfig(self):
       return self.__dictRepositoryConfig
    # eof def GetConfig(self):

# eof class CRepositoryConfig():

# --------------------------------------------------------------------------------------------------------------
