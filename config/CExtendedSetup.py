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

# -*- coding: utf-8 -*-

# **************************************************************************************************************
#
# CExtendedSetup.py
#
# CM-CI1/ECA3-Queckenstedt
#
# Contains all functions to support the extended setup process.
#
# --------------------------------------------------------------------------------------------------------------
#
# 30.09.2021 / XC-CI1/ECA3-Queckenstedt
# Added wrapper for error messages
# 
# Initial version 08/2021
#
# --------------------------------------------------------------------------------------------------------------

import os, sys, platform, shlex, subprocess, shutil
import colorama as col

col.init(autoreset=True)

COLBR = col.Style.BRIGHT + col.Fore.RED
COLBY = col.Style.BRIGHT + col.Fore.YELLOW
COLBG = col.Style.BRIGHT + col.Fore.GREEN

SUCCESS = 0
ERROR   = 1

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg):
    sys.stderr.write(COLBR + f"Error: {sMsg}!\n")

def printexception(sMsg):
    sys.stderr.write(COLBR + f"Exception: {sMsg}!\n")

# --------------------------------------------------------------------------------------------------------------

class CExtendedSetup():

    def __init__(self, oRepositoryConfig=None):
        if oRepositoryConfig is None:
            raise Exception("oRepositoryConfig is None")
        self.__oRepositoryConfig = oRepositoryConfig

    # --------------------------------------------------------------------------------------------------------------

    def __del__(self):
        pass

    # --------------------------------------------------------------------------------------------------------------

    def gen_doc(self):
        """Executes sphinx-makeall.py
        """
        sPython = self.__oRepositoryConfig.Get('sPython')
        sDocumentationBuilder = self.__oRepositoryConfig.Get('sDocumentationBuilder')
        listCmdLineParts = []
        listCmdLineParts.append("\"" + str(sPython) + "\"")
        listCmdLineParts.append("\"" + str(sDocumentationBuilder) + "\"")
        sCmdLine = " ".join(listCmdLineParts)
        del listCmdLineParts
        listCmdLineParts = shlex.split(sCmdLine)
        # -- debug
        sCmdLine = " ".join(listCmdLineParts)
        print()
        print("Now executing command line:\n" + sCmdLine)
        print()
        nReturn = ERROR
        try:
            nReturn = subprocess.call(listCmdLineParts)
        except Exception as ex:
            print()
            printexception(str(ex))
            print()
            return ERROR
        print()
        return nReturn
    # eof def gen_doc():

    # --------------------------------------------------------------------------------------------------------------

    def delete_previous_build(self):
        """Deletes folder containing previous builds of setup.py within the repository
        """
        sSetupBuildFolder = self.__oRepositoryConfig.Get('sSetupBuildFolder')
        sSetupDistFolder  = self.__oRepositoryConfig.Get('sSetupDistFolder')
        sEggInfoFolder    = self.__oRepositoryConfig.Get('sEggInfoFolder')
        if os.path.isdir(sSetupBuildFolder) is True:
            print("* Deleting '" + sSetupBuildFolder + "'")
            try:
                shutil.rmtree(sSetupBuildFolder)
            except Exception as ex:
                print()
                printexception(str(ex))
                print()
                return ERROR
        if os.path.isdir(sSetupDistFolder) is True:
            print("* Deleting '" + sSetupDistFolder + "'")
            try:
                shutil.rmtree(sSetupDistFolder)
            except Exception as ex:
                print()
                printexception(str(ex))
                print()
                return ERROR
        if os.path.isdir(sEggInfoFolder) is True:
            print("* Deleting '" + sEggInfoFolder + "'")
            try:
                shutil.rmtree(sEggInfoFolder)
            except Exception as ex:
                print()
                printexception(str(ex))
                print()
                return ERROR
        return SUCCESS
    # eof def delete_previous_build():

    # --------------------------------------------------------------------------------------------------------------

    def delete_previous_installation(self):
        """Deletes previous package installation folder within the Python installation
        """
        sInstalledPackageFolder = self.__oRepositoryConfig.Get('sInstalledPackageFolder')
        if os.path.isdir(sInstalledPackageFolder) is True:
            print("* Deleting '" + sInstalledPackageFolder + "'")
            try:
                shutil.rmtree(sInstalledPackageFolder)
            except Exception as ex:
                print()
                printexception(str(ex))
                print()
                return ERROR
        sInstalledPackageDocFolder = self.__oRepositoryConfig.Get('sInstalledPackageDocFolder')
        if os.path.isdir(sInstalledPackageDocFolder) is True:
            print("* Deleting '" + sInstalledPackageDocFolder + "'")
            try:
                shutil.rmtree(sInstalledPackageDocFolder)
            except Exception as ex:
                print()
                printexception(str(ex))
                print()
                return ERROR
        print()
        return SUCCESS

    # eof def delete_previous_installation():

    # --------------------------------------------------------------------------------------------------------------

    def add_htmldoc_to_installation(self):
        """Adds the package documentation in HTML format to the Python onstallation
        """
        sHTMLOutputFolder          = self.__oRepositoryConfig.Get('sHTMLOutputFolder')
        sInstalledPackageDocFolder = self.__oRepositoryConfig.Get('sInstalledPackageDocFolder')
        if os.path.isdir(sHTMLOutputFolder) is False:
            print()
            printerror("Error: Missing html output folder '" + sHTMLOutputFolder + "'")
            print()
            return ERROR
        shutil.copytree(sHTMLOutputFolder, sInstalledPackageDocFolder)
        if os.path.isdir(sInstalledPackageDocFolder) is False:
            print()
            printerror("Error: html documentation not copied to package installation folder '" + sInstalledPackageDocFolder + "'")
            print()
            return ERROR
        print(COLBY + "Folder '" + sHTMLOutputFolder + "'")
        print(COLBY + "copied to")
        print(COLBY + "'" + sInstalledPackageDocFolder + "'")
        print()
        return SUCCESS
    # eof def add_htmldoc_to_installation():

# eof class CExtendedSetup():

# --------------------------------------------------------------------------------------------------------------

