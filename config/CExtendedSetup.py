# **************************************************************************************************************
#
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
#
# **************************************************************************************************************
#
# CExtendedSetup.py
#
# XC-CT/ECA3-Queckenstedt
#
# Contains all functions to support the extended setup process.
#
# --------------------------------------------------------------------------------------------------------------
#
# 22.02.2022 / XC-CT/ECA3-Queckenstedt
# Added add_htmldoc_to_wheel() to support wheel based distribution
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
        listCmdLineParts.append(f"\"{sPython}\"")
        listCmdLineParts.append(f"\"{sDocumentationBuilder}\"")
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
            print(f"* Deleting '{sSetupBuildFolder}'")
            try:
                shutil.rmtree(sSetupBuildFolder)
            except Exception as ex:
                print()
                printexception(str(ex))
                print()
                return ERROR
        if os.path.isdir(sSetupDistFolder) is True:
            print(f"* Deleting '{sSetupDistFolder}'")
            try:
                shutil.rmtree(sSetupDistFolder)
            except Exception as ex:
                print()
                printexception(str(ex))
                print()
                return ERROR
        if os.path.isdir(sEggInfoFolder) is True:
            print(f"* Deleting '{sEggInfoFolder}'")
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
            print(f"* Deleting '{sInstalledPackageFolder}'")
            try:
                shutil.rmtree(sInstalledPackageFolder)
            except Exception as ex:
                print()
                printexception(str(ex))
                print()
                return ERROR
        sInstalledPackageDocFolder = self.__oRepositoryConfig.Get('sInstalledPackageDocFolder')
        if os.path.isdir(sInstalledPackageDocFolder) is True:
            print(f"* Deleting '{sInstalledPackageDocFolder}'")
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
            printerror(f"Error: Missing html output folder '{sHTMLOutputFolder}'")
            print()
            return ERROR
        shutil.copytree(sHTMLOutputFolder, sInstalledPackageDocFolder)
        if os.path.isdir(sInstalledPackageDocFolder) is False:
            print()
            printerror(f"Error: html documentation not copied to package installation folder '{sInstalledPackageDocFolder}'")
            print()
            return ERROR
        print(COLBY + f"Folder '{sHTMLOutputFolder}'")
        print(COLBY + "copied to")
        print(COLBY + f"'{sInstalledPackageDocFolder}'")
        print()
        return SUCCESS
    # eof def add_htmldoc_to_installation():

    # --------------------------------------------------------------------------------------------------------------

    def add_htmldoc_to_wheel(self):
        """Adds the package documentation in HTML format to the wheel folder inside build
        """
        sHTMLOutputFolder = self.__oRepositoryConfig.Get('sHTMLOutputFolder')
        sSetupBuildFolder = self.__oRepositoryConfig.Get('sSetupBuildFolder')
        sPackageName      = self.__oRepositoryConfig.Get('sPackageName')
        if os.path.isdir(sHTMLOutputFolder) is False:
            print()
            printerror(f"Error: Missing html output folder '{sHTMLOutputFolder}'")
            print()
            return ERROR

        # The desired destination path for the documentation is:
        # <build>\bdist.win-amd64\wheel\<package name>\doc
        # with <build> is already available by 'sSetupBuildFolder' in CConfig.
        # I am not convinced that it's a good idea to have hard coded parts like 'bdist.win-amd64' within a path here.
        # Therefore we search recursively the file system for a subfolder with name 'wheel/<package name>'. And that's it!
        sTargetFolder     = f"wheel/{sPackageName}"
        sWheelDocDestPath = None
        bBreak            = False
        for sRootFolder, listFolders, listFiles in os.walk(sSetupBuildFolder):
            for sFolder in listFolders:
                sPath = os.path.join(sRootFolder, sFolder)
                sPathMod = sPath.replace("\\", "/")
                if sPathMod.endswith(sTargetFolder):
                    sWheelDocDestPath = f"{sPathMod}/doc"
                    bBreak = True
                    break # for sFolder in listFolders:
                # eof if sPathMod.endswith(sTargetFolder):
            # eof for sFolder in listFolders:
            if bBreak is True:
                break # walk
        # eof for sRootFolder, listFolders, listFiles in os.walk(sSetupBuildFolder):

        if sWheelDocDestPath is None:
            print()
            printerror(f"Error: Not able to find '{sTargetFolder}' inside {sSetupBuildFolder}")
            print()
            return ERROR

        shutil.copytree(sHTMLOutputFolder, sWheelDocDestPath)
        if os.path.isdir(sWheelDocDestPath) is False:
            print()
            printerror(f"Error: html documentation not copied to local wheel folder '{sWheelDocDestPath}'")
            print()
            return ERROR

        print(COLBY + f"Folder '{sHTMLOutputFolder}'")
        print(COLBY + "copied to")
        print(COLBY + f"'{sWheelDocDestPath}'")
        print()
        return SUCCESS
    # eof def add_htmldoc_to_wheel():

# eof class CExtendedSetup():

# --------------------------------------------------------------------------------------------------------------

