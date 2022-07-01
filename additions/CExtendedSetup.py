# **************************************************************************************************************
#
#  Copyright 2020-2022 Robert Bosch GmbH
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
# 10.05.2022
#
# --------------------------------------------------------------------------------------------------------------

import os, sys, platform, shlex, subprocess, shutil
import pypandoc
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

    def genpackagedoc(self):
        """Executes genpackagedoc.py
        """
        sPython = self.__oRepositoryConfig.Get('PYTHON')
        sDocumentationBuilder = self.__oRepositoryConfig.Get('DOCUMENTATIONBUILDER')
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
    # eof def genpackagedoc():

    # --------------------------------------------------------------------------------------------------------------

    def convert_repo_readme(self):
        """Converts the main repository README from 'rst' to 'md' format.
        """

        sReadMe_rst = self.__oRepositoryConfig.Get("README_RST")
        if sReadMe_rst is None:
            print()
            printerror(f"'sReadMe_rst' is None")
            print()
            return ERROR

        sReadMe_md = self.__oRepositoryConfig.Get("README_MD")
        if sReadMe_md is None:
            print()
            printerror(f"'sReadMe_md' is None")
            print()
            return ERROR

        if os.path.isfile(sReadMe_rst) is False:
            print()
            printerror(f"Missing readme file '{sReadMe_rst}'")
            print()
            return ERROR

        sFileContent = pypandoc.convert_file(sReadMe_rst, 'md')
        hFile_md = open(sReadMe_md, "w", encoding="utf-8")
        listFileContent = sFileContent.splitlines()
        for sLine in listFileContent:
            hFile_md.write(sLine + "\n")
        hFile_md.close()

        print(f"File '{sReadMe_rst}'")
        print("converted to")
        print(f"'{sReadMe_md}'")
        print()

        return SUCCESS

    # eof def convert_repo_readme(self):

    # --------------------------------------------------------------------------------------------------------------

    def delete_previous_build(self):
        """Deletes folder containing previous builds of setup.py within the repository
        """
        sSetupBuildFolder = self.__oRepositoryConfig.Get('SETUPBUILDFOLDER')
        sSetupDistFolder  = self.__oRepositoryConfig.Get('SETUPDISTFOLDER')
        sEggInfoFolder    = self.__oRepositoryConfig.Get('EGGINFOFOLDER')
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
        sInstalledPackageFolder = self.__oRepositoryConfig.Get('INSTALLEDPACKAGEFOLDER')
        if os.path.isdir(sInstalledPackageFolder) is True:
            print(f"* Deleting '{sInstalledPackageFolder}'")
            try:
                shutil.rmtree(sInstalledPackageFolder)
            except Exception as ex:
                print()
                printexception(str(ex))
                print()
                return ERROR
        print()
        return SUCCESS

    # eof def delete_previous_installation():

# eof class CExtendedSetup():

# --------------------------------------------------------------------------------------------------------------

