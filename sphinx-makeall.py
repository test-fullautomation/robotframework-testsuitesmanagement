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
# sphinx-makeall.py
#
# XC-CT/ECA3-Queckenstedt
#
# Uses the Python documentation tool Sphinx to generate the documentation of Python modules
# - based on the docstrings inside the Python modules and
# - based on additionally included separate text files (containing usually more common information
#   than the docstrings of the Python modules).
#
# The docstrings and the additionally included text files have to be written in reStructureText syntax.
# The output is available in HTML format and in LaTeX format (.tex), optionally also in PDF.
#
# Preconditions:
# - Sphinx available as part of the Python installation.
# - Sphinx documentation project files already created and adapted to the local repository
#   (see conf.py and index.rst).
# - LaTeX compiler (in case of output in PDF format is wanted)
# - pandoc and pypandoc for conversions between markdown formats
#
# Known issues:
# - LaTeX compiler throws some warnings when computing Sphinx output.
#
# --------------------------------------------------------------------------------------------------------------
#
# 02.11.2021 / XC-CT/ECA3-Queckenstedt
# gen_doc_pdf called twice (to get also a table of content added to PDF file)
# 
# 30.09.2021 / XC-CI1/ECA3-Queckenstedt
# Added wrapper for error messages
# 
# Initial version 08/2021
#
# --------------------------------------------------------------------------------------------------------------

import os, sys, platform, shlex, subprocess

import pypandoc

from config.CConfig import CConfig # providing repository and environment specific information

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

def convert_repo_readme(oRepositoryConfig=None):
    """Converts the main repository README from 'rst' to 'md' format.
    """

    if oRepositoryConfig is None:
        print()
        printerror("oRepositoryConfig is None")
        print()
        return ERROR

    sReadMe_rst = oRepositoryConfig.Get("sReadMe_rst")
    if sReadMe_rst is None:
        return ERROR

    sReadMe_md = oRepositoryConfig.Get("sReadMe_md")
    if sReadMe_md is None:
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

    print()
    print(COLBY + f"File '{sReadMe_rst}'")
    print(COLBY + "converted to")
    print(COLBY + f"'{sReadMe_md}'")
    print()

    return SUCCESS

# eof def convert_repo_readme(oRepositoryConfig=None):

# --------------------------------------------------------------------------------------------------------------

def sphinx_build(sFormat=None, oRepositoryConfig=None):
    """Executes Sphinx to generate the documentation in format 'sFormat'.
    """

    if sFormat is None:
        print()
        printerror("sFormat is None")
        print()
        return ERROR

    if oRepositoryConfig is None:
        print()
        printerror("oRepositoryConfig is None")
        print()
        return ERROR

    SPHINXBUILD = oRepositoryConfig.Get("SPHINXBUILD")
    if SPHINXBUILD is None:
        return ERROR

    SOURCEDIR = oRepositoryConfig.Get("SOURCEDIR")
    if SOURCEDIR is None:
        return ERROR

    BUILDDIR = oRepositoryConfig.Get("BUILDDIR")
    if BUILDDIR is None:
        return ERROR

    sPython = oRepositoryConfig.Get("sPython")
    if sPython is None:
        return ERROR

    listCmdLineParts = []
    listCmdLineParts.append(f"\"{sPython}\"")
    listCmdLineParts.append(f"\"{SPHINXBUILD}\"")
    listCmdLineParts.append(f"-M {sFormat}")
    listCmdLineParts.append(f"\"{SOURCEDIR}\"")
    listCmdLineParts.append(f"\"{BUILDDIR}\"")

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
        printexception(str(ex))
        print()
        return ERROR

    print()

    return nReturn

# eof def sphinx_build(sFormat=None, oRepositoryConfig=None):

# --------------------------------------------------------------------------------------------------------------

def gen_doc_pdf(oRepositoryConfig=None):
    """Executes LaTeX to generate the documentation in PDF format (based on previously generated LaTeX format).
    """

    if oRepositoryConfig is None:
        print()
        printerror("oRepositoryConfig is None")
        print()
        return ERROR

    print() # empty line after Sphinx console output - for better readibility

    BUILDDIR = oRepositoryConfig.Get("BUILDDIR")
    if BUILDDIR is None:
        return ERROR

    sLaTeXInterpreter = oRepositoryConfig.Get("sLaTeXInterpreter")
    if sLaTeXInterpreter is None:
        return ERROR

    # LaTeX sources are placed by Sphinx within subfolder 'latex' of folder 'BUILDDIR'
    sLaTeXRoot = os.path.normpath(f"{BUILDDIR}/latex")        # not part of oRepositoryConfig; only needed here!
    if os.path.isdir(sLaTeXRoot) is False:
        print()
        printerror(f"Missing LaTeX documentation folder '{sLaTeXRoot}'")
        print()
        return ERROR

    # Not really sure which name of main tex file we can expect here; therefore scanning for tex files and compute all of them
    # (but usually only one tex file is expected)
    listTeXFiles = []
    for root, dirs, files in os.walk(sLaTeXRoot):
        for name in files:
            if name.lower().endswith(".tex"):
                sTeXFile = os.path.join(root, name)
                listTeXFiles.append(sTeXFile)

    if len(listTeXFiles) == 0:
        print()
        printerror(f"Missing LaTeX source files (.tex) within '{sLaTeXRoot}'")
        print()
        return ERROR

    for sTeXFile in listTeXFiles:
        print(COLBY + f"* Rendering file '{sTeXFile}'")
        print()

        listCmdLineParts = []
        listCmdLineParts.append(f"\"{sLaTeXInterpreter}\"")
        listCmdLineParts.append(f"\"{sTeXFile}\"")

        sCmdLine = " ".join(listCmdLineParts)
        del listCmdLineParts
        listCmdLineParts = shlex.split(sCmdLine)

        # -- debug
        # sCmdLine = " ".join(listCmdLineParts)
        # print("Now executing command line:\n" + sCmdLine)
        # print()

        nReturn = ERROR
        cwd = os.getcwd() # we have to save cwd because later we have to change
        try:
            os.chdir(sLaTeXRoot) # otherwise LaTeX compiler is not able to find files inside
            nReturn = subprocess.call(listCmdLineParts)
            print()
            print(f"LaTeX compiler returned {nReturn}")
            print()
            os.chdir(cwd) # restore original value
        except Exception as ex:
            printexception(str(ex))
            print()
            os.chdir(cwd) # restore original value
            return ERROR

        if nReturn != SUCCESS:
            printerror(f"LaTeX compiler not returned expected value {SUCCESS}")
            print()
            return nReturn

        # finally let's see what has been generated
        for root, dirs, files in os.walk(sLaTeXRoot):
            for name in files:
                if name.lower().endswith(".pdf"):
                    sPDFFile = os.path.join(root, name)
                    print(COLBY + f"* Created '{sPDFFile}'")
        print()

    return nReturn

# eof def gen_doc_pdf(oRepositoryConfig=None):

# --------------------------------------------------------------------------------------------------------------

# -- setting up the repository configuration (relative to the path of this script)
oRepositoryConfig = None
sReferencePath = os.path.dirname(os.path.abspath(sys.argv[0]))
try:
    oRepositoryConfig = CConfig(sReferencePath)
except Exception as ex:
    print()
    printexception(str(ex))
    print()
    sys.exit(ERROR)

# -- converting the main repository README from 'rst' to 'md' format
nReturn = convert_repo_readme(oRepositoryConfig)
if nReturn != SUCCESS:
    printerror("convert_repo_readme with 'README.rst' failed")
    print()
    sys.exit(nReturn)

# -- removing previous output in documentation build folder
nReturn = sphinx_build("clean", oRepositoryConfig)
if nReturn != SUCCESS:
    printerror("sphinx_build 'clean' failed")
    print()
    sys.exit(nReturn)

# -- generating new documentation in HTML format
nReturn = sphinx_build("html", oRepositoryConfig)
if nReturn != SUCCESS:
    printerror("sphinx_build 'html' failed")
    print()
    sys.exit(nReturn)

# -- generating new documentation in LaTeX format
nReturn = sphinx_build("latex", oRepositoryConfig)
if nReturn != SUCCESS:
    printerror("sphinx_build 'latex' failed")
    print()
    sys.exit(nReturn)

# -- generating new documentation in PDF format (requires configured LaTeX)
sLaTeXInterpreter = oRepositoryConfig.Get('sLaTeXInterpreter')
if sLaTeXInterpreter is not None:
    print("Calling LaTeX PDF renderer (1/2)")
    nReturn = gen_doc_pdf(oRepositoryConfig)
    if nReturn != SUCCESS:
        printerror("PDF generation failed")
        print()
        sys.exit(nReturn)
    print("Calling LaTeX PDF renderer (2/2) - to get referencs and table of content updated")
    nReturn = gen_doc_pdf(oRepositoryConfig)
    if nReturn != SUCCESS:
        printerror("PDF generation failed")
        print()
        sys.exit(nReturn)

# --------------------------------------------------------------------------------------------------------------

print(COLBG + "sphinx-makeall done")
print()
sys.exit(SUCCESS)

# --------------------------------------------------------------------------------------------------------------

