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
import regex
from enum import Enum

class CVersionCheck(Enum):
    WITHOUTVERSION = "without_version_check"
    WRONGMINMAX    = "wrong_minmax"
    CONFLICTMIN    = "conflict_min"
    CONFLICTMAX    = "conflict_max"

class CVersion():
    '''
Validates a bundle version of an installed package
    '''
    def __init__(self, sBundleName, sMinVersion, sMaxVersion, sCurrentVersion):
        self.sBundleName       = sBundleName
        self.sMaxVersion       = sMaxVersion
        self.sMinVersion       = sMinVersion
        self.sCurrentVersion   = sCurrentVersion
        self.reason            = None

    def verifyVersion(self):
        '''
This verifyVersion validates the current package version with maximum and minimum version.

The package version is the version when this module is installed stand-alone

**Arguments:**

* No input parameter is required

**Returns:**

* No return variable
        '''
        tCurrentVersion = self.tupleVersion(self.sCurrentVersion)

        # Verify format of provided min and max versions then parse to tuples
        tMinVersion = None
        tMaxVersion = None
        if self.sMinVersion.strip() == '' and self.sMaxVersion.strip() == '':
            self.reason = CVersionCheck.WITHOUTVERSION.value
            return
        if self.sMinVersion != '':
            tMinVersion = self.tupleVersion(self.sMinVersion)
        if self.sMaxVersion != '':
            tMaxVersion = self.tupleVersion(self.sMaxVersion)
        if tMinVersion and tMaxVersion and (tMinVersion > tMaxVersion):
            self.reason = CVersionCheck.WRONGMINMAX.value
            return
        if tMinVersion and not self.bValidateMinVersion(tCurrentVersion, tMinVersion):
            self.reason = CVersionCheck.CONFLICTMIN.value
            return
        if tMaxVersion and not self.bValidateMaxVersion(tCurrentVersion, tMaxVersion):
            self.reason = CVersionCheck.CONFLICTMAX.value
            return

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
This bValidateMaxVersion validates the current version with required minimun version.

**Arguments:**

* ``tCurrentVersion``

  / *Condition*: required / *Type*: tuple /

  Current package version.

* ``tMinVersion``

  / *Condition*: required / *Type*: tuple /

  The minimum version of package.

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