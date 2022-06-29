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
# CFolder.py
#
# XC-CT/ECA3-Queckenstedt
#
# 28.06.2022
#
# **************************************************************************************************************

# -- import standard Python modules
import os, shutil, time, stat

# -- import Bosch Python modules
from PythonExtensionsCollection.String.CString import CString

# --------------------------------------------------------------------------------------------------------------

# little helper to delete folders containing files that are write protected
def rm_dir_readonly(func, path, excinfo):
   """
Calls ``os.chmod`` in case of ``shutil.rmtree`` (within ``Delete()``) throws an exception (making files writable).
   """
   # print(f"{excinfo}") # debug only
   os.chmod(path, stat.S_IWRITE)
   func(path)

# --------------------------------------------------------------------------------------------------------------

class CFolder(object):
   """
The class ``CFolder`` provides a small set of folder functions with extended parametrization (like switches
defining if a folder is allowed to be overwritten or not).

Most of the functions at least returns ``bSuccess`` and ``sResult``.

* ``bSuccess`` is ``True`` in case of no error occurred.
* ``bSuccess`` is ``False`` in case of an error occurred.
* ``bSuccess`` is ``None`` in case of a very fatal error occurred (exceptions).

* ``sResult`` contains details about what happens during computation.

Every instance of CFolder handles one single folder only and forces exclusive access to this folder.

It is not possible to create an instance of this class with a folder that is already in use by another instance.

The constructor of ``CFolder`` requires the input parameter ``sFolder``, that is the path and the name of a folder
that is handled by the current class instance.
   """
   # --------------------------------------------------------------------------------------------------------------
   # TM***

   def __init__(self, sFolder=None):
      self.__sFolder = CString.NormalizePath(sFolder)

      try:
         CFolder.__listFoldersInUse
      except:
         CFolder.__listFoldersInUse = []

      # exclusive access is required (checked by self.__bIsFreeToUse; relevant for destination in CopyTo and MoveTo)
      if self.__sFolder in CFolder.__listFoldersInUse:
         raise Exception(f"The folder '{self.__sFolder}' is already in use by another CFolder instance.")
      else:
         CFolder.__listFoldersInUse.append(self.__sFolder)

   # eof def __init__(self, sFolder=None):

   def __del__(self):
      if self.__sFolder in CFolder.__listFoldersInUse:
         CFolder.__listFoldersInUse.remove(self.__sFolder)

   # eof def __del__(self):

   # --------------------------------------------------------------------------------------------------------------
   # TM***

   def __bIsFreeToUse(self, sFolder=None):
      """
Checks if the folder ``sFolder`` is free to use, that means: not used by another instance of ``CFolder``.
      """

      bIsFreeToUse = False # init
      if sFolder is None:
         bIsFreeToUse = False # error handling
      else:
         if sFolder in CFolder.__listFoldersInUse:
            bIsFreeToUse = False
         else:
            bIsFreeToUse = True
      return bIsFreeToUse

   # eof def __bIsFreeToUse(self, sFolder=None):

   # --------------------------------------------------------------------------------------------------------------
   # TM***

   def __Delete(self, sFolder=None, bConfirmDelete=True):
      """
Deletes the folder ``sFolder``.

**Arguments:**

* ``sFolder``

  / *Condition*: required / *Type*: str /

  Path and name of folder to be deleted

* ``bConfirmDelete``

  / *Condition*: optional / *Type*: bool / *Default*: True /

  Defines if it will be handled as error if the folder does not exist.

  If ``True``: If the folder does not exist, the method indicates an error (``bSuccess = False``).

  If ``False``: It doesn't matter if the folder exists or not.

**Returns:**

* ``bSuccess``

  / *Type*: bool /

  Indicates if the computation of the method was successful or not.

* ``sResult``

  / *Type*: str /

  The result of the computation of the method.
      """
      sMethod = "CFolder.__Delete"

      if sFolder is None:
         bSuccess = False
         sResult  = "sFolder is None; please provide path and name of a folder when creating a CFolder object."
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      if os.path.isdir(sFolder) is False:
         sResult = f"Nothing to delete. The folder '{sFolder}' does not exist."
         if bConfirmDelete is True:
            bSuccess = False
            sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         else:
            bSuccess = True
         return bSuccess, sResult
      # eof if os.path.isdir(sFolder) is False:

      bSuccess    = False
      sResult     = "UNKNOWN"
      nCntTries   = 1
      nTriesMax   = 4
      nDelay      = 2 # sec
      listResults = []
      while nCntTries <= nTriesMax:
         try:
            print(f"Trying to delete '{sFolder}'")
            print()
            shutil.rmtree(sFolder, ignore_errors=False, onerror=rm_dir_readonly)
         except Exception as reason:
            listResults.append(str(reason))
         if os.path.isdir(sFolder) is True:
            sResult = f"({nCntTries}/{nTriesMax}) Problem with deleting the folder '{sFolder}'. Folder still present."
            listResults.append(sResult)
            time.sleep(nDelay) # delay before next try
         else:
            bSuccess = True
            sResult  = f"Folder '{sFolder}' deleted."
            break
         nCntTries = nCntTries + 1
      # eof while nCntTries <= nTriesMax:

      if bSuccess is False:
         sResult = "\n".join(listResults)
         sResult = CString.FormatResult(sMethod, bSuccess, sResult)

      return bSuccess, sResult

   # eof def __Delete(self, sFolder=None, bConfirmDelete=True):

   # --------------------------------------------------------------------------------------------------------------
   # TM***

   def Delete(self, bConfirmDelete=True):
      """
Deletes the folder the current class instance contains.

**Arguments:**

* ``bConfirmDelete``

  / *Condition*: optional / *Type*: bool / *Default*: True /

  Defines if it will be handled as error if the folder does not exist.

  If ``True``: If the folder does not exist, the method indicates an error (``bSuccess = False``).

  If ``False``: It doesn't matter if the folder exists or not.

**Returns:**

* ``bSuccess``

  / *Type*: bool /

  Indicates if the computation of the method was successful or not.

* ``sResult``

  / *Type*: str /

  The result of the computation of the method.
      """
      sMethod = "CFolder.Delete"
      bSuccess, sResult = self.__Delete(self.__sFolder, bConfirmDelete)
      if bSuccess is not True:
         sResult = CString.FormatResult(sMethod, bSuccess, sResult)
      return bSuccess, sResult

   # eof def Delete(self, bConfirmDelete=True):

   # --------------------------------------------------------------------------------------------------------------
   # TM***

   def Create(self, bOverwrite=False, bRecursive=False):
      """
Creates the current folder ``sFolder``.

**Arguments:**

* ``bOverwrite``

  / *Condition*: optional / *Type*: bool / *Default*: False /

  * In case of the folder already exists and ``bOverwrite`` is ``True``, than the folder will be deleted before creation.
  * In case of the folder already exists and ``bOverwrite`` is ``False`` (default), than the folder will not be touched.

  In both cases the return value ``bSuccess`` is ``True`` - because the folder exists.

* ``bRecursive``

  / *Condition*: optional / *Type*: bool / *Default*: False /

  * In case of ``bRecursive`` is ``True``, than the complete destination path will be created (including all intermediate subfolders).
  * In case of ``bRecursive`` is ``False``, than it is expected that the parent folder of the new folder already exists.

**Returns:**

* ``bSuccess``

  / *Type*: bool /

  Indicates if the computation of the method was successful or not.

* ``sResult``

  / *Type*: str /

  The result of the computation of the method.
      """
      sMethod = "CFolder.Create"

      if self.__sFolder is None:
         bSuccess = False
         sResult  = "self.__sFolder is None; please provide path and name of a folder when creating a CFolder object."
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      bCreateFolder = False
      if os.path.isdir(self.__sFolder) is True:
         if bOverwrite is True:
            bSuccess, sResult = self.Delete()
            if bSuccess is not True:
               sResult = CString.FormatResult(sMethod, bSuccess, sResult)
               return bSuccess, sResult
            bCreateFolder = True
         else:
            bSuccess = True
            sResult  = f"Folder '{self.__sFolder}' already exists."
            return bSuccess, sResult
      else:
         bCreateFolder = True

      bSuccess = False
      sResult  = "UNKNOWN"

      if bCreateFolder is True:
         nCntTries   = 1
         nTriesMax   = 3
         nDelay      = 2 # sec
         listResults = []
         while nCntTries <= nTriesMax:
            try:
               print(f"Trying to create '{self.__sFolder}'")
               print()
               if bRecursive is True:
                  os.makedirs(self.__sFolder)
               else:
                  os.mkdir(self.__sFolder)
            except Exception as reason:
               listResults.append(str(reason))
            if os.path.isdir(self.__sFolder) is False:
               sResult = f"({nCntTries}/{nTriesMax}) Problem with creating the folder '{self.__sFolder}'."
               listResults.append(sResult)
               time.sleep(nDelay) # delay before next try
            else:
               bSuccess = True
               sResult  = f"Folder '{self.__sFolder}' created."
               break
            nCntTries = nCntTries + 1
         # eof while nCntTries <= nTriesMax:

         if bSuccess is False:
            sResult = "\n".join(listResults)
            sResult = CString.FormatResult(sMethod, bSuccess, sResult)

      # eof if bCreateFolder is True:

      return bSuccess, sResult

   # eof def Create(self, bOverwrite=False, bRecursive=False):

   # --------------------------------------------------------------------------------------------------------------
   # TM***

   def CopyTo(self, sDestination=None, bOverwrite=False):
      """
Copies the current folder to ``sDestination``, that has to be a path to a folder **within** the source folder will be copied to
(with it's original name),

In case of the destination folder already exists and ``bOverwrite`` is ``True``, than the destination folder will be overwritten.

In case of the destination folder already exists and ``bOverwrite`` is ``False`` (default), than the destination folder will not be overwritten
and ``CopyTo`` returns ``bSuccess = False``.

**Arguments:**

* ``sDestination``

  / *Condition*: required / *Type*: string /

  The path to destination folder

* ``bOverwrite``

  / *Condition*: optional / *Type*: bool / *Default*: False /

  * In case of the destination folder already exists and ``bOverwrite`` is ``True``, than the destination folder will be overwritten.
  * In case of the destination folder already exists and ``bOverwrite`` is ``False`` (default), than the destination folder will not be overwritten
    and ``CopyTo`` returns ``bSuccess = False``.

**Returns:**

* ``bSuccess``

  / *Type*: bool /

  Indicates if the computation of the method was successful or not.

* ``sResult``

  / *Type*: str /

  The result of the computation of the method.
      """
      sMethod = "CFolder.CopyTo"

      if self.__sFolder is None:
         bSuccess = False
         sResult  = "self.__sFolder is None; please provide path and name of a folder when creating a CFolder object."
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      if os.path.isdir(self.__sFolder) is False:
         bSuccess = False
         sResult  = f"The folder '{self.__sFolder}' does not exist, therefore nothing can be copied."
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      if sDestination is None:
         bSuccess = False
         sResult  = "sDestination is None; please provide a path to a destination folder."
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      sDestination = CString.NormalizePath(sDestination)

      if os.path.isdir(sDestination) is False:
         # the folder to be copied will be created within the destination folder, therefore we expect that the destination folder already exists
         bSuccess = False
         sResult  = f"The destination folder '{sDestination}' does not exist."
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      sSourceFolderName = os.path.basename(self.__sFolder)
      sDestFolder = f"{sDestination}/{sSourceFolderName}"

      if sDestFolder == self.__sFolder:
         bSuccess = False
         sResult  = f"Source folder and destination folder are the same: '{self.__sFolder}'. Therefore nothing to do."
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      if self.__bIsFreeToUse(sDestFolder) is False:
         bSuccess = False
         sResult  = f"The destination folder '{sDestFolder}' is already in use by another CFolder instance."
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
         return bSuccess, sResult

      if os.path.isdir(sDestFolder) is True:
         # destination folder already exists
         if bOverwrite is True:
            bSuccess, sResult = self.__Delete(sDestFolder)
            if bSuccess is not True:
               sResult = CString.FormatResult(sMethod, bSuccess, sResult)
               return bSuccess, sResult
         else:
            bSuccess = False
            sResult  = f"Not allowed to overwrite existing destination folder '{sDestFolder}'. Therefore nothing to do."
            sResult  = CString.FormatResult(sMethod, bSuccess, sResult)
            return bSuccess, sResult
      # eof if os.path.isdir(sDestFolder) is True:

      # analysis and preconditions done, now the action

      try:
         shutil.copytree(self.__sFolder, sDestFolder)
         bSuccess = True
         sResult  = "Folder copied from\n> '" + self.__sFolder + "'\nto\n> '" + sDestFolder + "'"
      except Exception as reason:
         bSuccess = None
         sResult  = str(reason)
         sResult  = CString.FormatResult(sMethod, bSuccess, sResult)

      return bSuccess, sResult

   # eof def CopyTo(self, sDestination=None, bOverwrite=False):

# --------------------------------------------------------------------------------------------------------------


