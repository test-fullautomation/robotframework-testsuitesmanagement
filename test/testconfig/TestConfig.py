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
# TestConfig.py
#
# XC-CT/ECA3-Queckenstedt
#
# --------------------------------------------------------------------------------------------------------------
#
# 30.03.2023
#
# --------------------------------------------------------------------------------------------------------------

# "tsm-testfile-01.robot"         # (without variant configuration)
# "tsm-testfile-02.robot"         # (with variant configuration)
# "tsm-testfile-03.robot"         # (with variant configuration and extended logging of parameters from nested configuration files)
# "tsm-testfile-04.robot"         # (with variant configuration and extended logging of parameters from nested configuration files; all relevant datatypes; logging with pretty_print)
# "tsm-testfile-05-err-1.robot"   # (with variant configuration; JSON file contains syntax errors)
# "tsm-testfile-06-err-2.robot"   # (with variant configuration; JSON file contains not existing file and folder)
# "tsm-testfile-07-err-3.robot"   # (with variant configuration; missing "default" variant)
# "tsm-testfile-08-fail.robot"    # (with variant configuration; keyword FAIL)
# "tsm-testfile-09-unknown.robot" # (with variant configuration; keyword UNKNOWN)

# --------------------------------------------------------------------------------------------------------------

listofdictUsecases = []

# the following keys are optional, all other keys are mandatory.
# dictUsecase['HINT']             = None
# dictUsecase['PRESTEP']          = None
# dictUsecase['POSTSTEP']         = None
# dictUsecase['LOGCOMPARE']       = None

# --------------------------------------------------------------------------------------------------------------
#TM***
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0001"
dictUsecase['DESCRIPTION']      = "Without variant configuration file in suite setup of robot file; default config level 4"
dictUsecase['EXPECTATION']      = "Execution with config level 4"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-01.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = None
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0002"
dictUsecase['DESCRIPTION']      = "With variant configuration file in suite setup of robot file; default variant"
dictUsecase['EXPECTATION']      = "Execution with default variant"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = None
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0003"
dictUsecase['DESCRIPTION']      = "With variant name in command line / (variant1)"
dictUsecase['EXPECTATION']      = "Execution with selected variant 1"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0004"
dictUsecase['DESCRIPTION']      = "With variant name in command line / with 4 byte UTF-8 characters inside name"
dictUsecase['EXPECTATION']      = "Execution with selected variant"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"SälfTest.ß.€.考.𠼭.𠼭\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0005"
dictUsecase['DESCRIPTION']      = "With parameter configuration file in command line / (tsm-test_config_variant2.json)"
dictUsecase['EXPECTATION']      = "Execution with selected variant 2"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable config_file:\"./config/tsm-test_config_variant2.json\"" # path relative to position of robot file
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0006"
dictUsecase['DESCRIPTION']      = "With parameter configuration file in command line / with 4 byte UTF-8 characters inside name"
dictUsecase['EXPECTATION']      = "Execution with selected config file for variant"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable config_file:\"./config/tsm-test_config_SälfTest.ß.€.考.𠼭.𠼭.json\"" # path relative to position of robot file
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0007"
dictUsecase['DESCRIPTION']      = "With variant name and single parameter in command line / (variant1; teststring_variant)"
dictUsecase['EXPECTATION']      = "Single command line parameter value overwrites variant 1 configuration value"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\" --variable teststring_variant:\"command line value of teststring_variant\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0008"
dictUsecase['DESCRIPTION']      = "With parameter configuration file and single parameter in command line / (variant2; teststring_variant)"
dictUsecase['EXPECTATION']      = "Single command line parameter value overwrites variant 2 configuration value"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable config_file:\"./config/tsm-test_config_variant2.json\" --variable teststring_variant:\"command line value of teststring_variant\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0009"
dictUsecase['DESCRIPTION']      = "With parameter configuration file taken from local config folder; robot file has same name as configuration file"
dictUsecase['EXPECTATION']      = "Configuration parameters taken from configuration file with same name as the robot file"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "configfoldertests/tsm-cft-testfile-1.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = None
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0010"
dictUsecase['DESCRIPTION']      = "With parameter configuration file taken from local config folder; robot file has another name as configuration file"
dictUsecase['EXPECTATION']      = "Configuration parameters taken from configuration file with predefined default name (robot_config.json)"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "configfoldertests/tsm-cft-testfile-2.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = None
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0050"
dictUsecase['DESCRIPTION']      = "With missing parameter in parameter configuration file"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"missing_param\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0051"
dictUsecase['DESCRIPTION']      = "With syntax error in parameter configuration file"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"syntax_error\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0052"
dictUsecase['DESCRIPTION']      = "With syntax error within imported parameter configuration file"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"syntax_error_within_import\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0053"
dictUsecase['DESCRIPTION']      = "With not existing imported parameter configuration file"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"missing_imported_file\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0054"
dictUsecase['DESCRIPTION']      = "With not existing imported parameter configuration file"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"missing_imported_file\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase

# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0055"
dictUsecase['DESCRIPTION']      = "Command line contains both: variant name and config file"
dictUsecase['EXPECTATION']      = "Both together is not accepted; test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\" --variable config_file:\"./config/tsm-test_config_variant2.json\"" # path relative to position of robot file
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0056"
dictUsecase['DESCRIPTION']      = "Command line contains variant name, but no variant configuration file is given to suite setup"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-01.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0057"
dictUsecase['DESCRIPTION']      = "Command line contains invalid variant name (not allowed characters in variant name)"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"in/va/lid\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0058"
dictUsecase['DESCRIPTION']      = "Command line contains unknown variant name (a variant with this name is not defined in variant configuration file)"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"I_AM_NOT_DEFINED\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0059"
dictUsecase['DESCRIPTION']      = "Command line contains unknown variant configuration file (a file with this name does not exist)"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable config_file:\"./config/I_AM_NOT_EXISTING.json\"" # path relative to position of robot file
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0060"
dictUsecase['DESCRIPTION']      = "Robot file refers to a variant configuration file with syntax errors"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-05-err-1.robot" # (with variant configuration; JSON file contains syntax errors)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = None
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0061"
dictUsecase['DESCRIPTION']      = "Robot file refers to a variant configuration file with not existing parameter file for default variant"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-06-err-2.robot" # (with variant configuration; JSON file contains not existing file and folder)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = None
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0062"
dictUsecase['DESCRIPTION']      = "Robot file refers to a variant configuration file with not existing path for variant1"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-06-err-2.robot" # (with variant configuration; JSON file contains not existing file and folder)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0063"
dictUsecase['DESCRIPTION']      = "Robot file refers to a variant configuration file with with missing 'default' variant; a variant name is not given in command line"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-07-err-3.robot" # (with variant configuration; missing "default" variant)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = None
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0064"
dictUsecase['DESCRIPTION']      = "A local config file is passed to command line parameter config_file"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN; reason: a local config file is not a full configuration file"
dictUsecase['SECTION']          = "VARIANT_HANDLING"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-01.robot" # (without variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable config_file:\"./localconfig/tsm-test_localconfig_bench1.json\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0100"
dictUsecase['DESCRIPTION']      = "With variant1 name and local config file for bench2 given in command line"
dictUsecase['EXPECTATION']      = "Local config value overwrites initial value for parameter 'teststring_bench'"
dictUsecase['SECTION']          = "LOCAL_CONFIG"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\" --variable local_config:\"./localconfig/tsm-test_localconfig_bench2.json\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0101"
dictUsecase['DESCRIPTION']      = "With variant2 configuration file and local config file for bench1 given in command line"
dictUsecase['EXPECTATION']      = "Local config value overwrites initial value for parameter 'teststring_bench'"
dictUsecase['SECTION']          = "LOCAL_CONFIG"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable config_file:\"./config/tsm-test_config_variant2.json\" --variable local_config:\"./localconfig/tsm-test_localconfig_bench1.json\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0102"
dictUsecase['DESCRIPTION']      = "With variant2 configuration file, local config file for bench1 and single parameter given in command line"
dictUsecase['EXPECTATION']      = "Command line value of 'teststring_bench' overwrites all other definitions (the initial one and the local config one)"
dictUsecase['SECTION']          = "LOCAL_CONFIG"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable teststring_bench:\"'teststring_bench' command line value\" --variable config_file:\"./config/tsm-test_config_variant2.json\" --variable local_config:\"./localconfig/tsm-test_localconfig_bench1.json\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0103"
dictUsecase['DESCRIPTION']      = "With variant1 name given in command line and and local config file for bench2 given by environment variable"
dictUsecase['EXPECTATION']      = "Local config value overwrites initial value for parameter 'teststring_bench'"
dictUsecase['SECTION']          = "LOCAL_CONFIG"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['HINT']             = "Temporary change of environment (ROBOT_LOCAL_CONFIG)"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot"
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\""
dictUsecase['PRESTEP']          = "LocalConfigEnvVar_Create"
dictUsecase['POSTSTEP']         = "LocalConfigEnvVar_Delete"
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0150"
dictUsecase['DESCRIPTION']      = "A parameter config file is passed to command line parameter local_config; a variant configuration file is not involved"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "LOCAL_CONFIG"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-01.robot" # (without variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable local_config:\"./config/tsm-test_config_variant1.json\""
dictUsecase['EXPECTEDRETURN']   = 1 # has to be changed later
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0151"
dictUsecase['DESCRIPTION']      = "A parameter config file for variant1 is passed to command line parameter local_config; also variant2 configuration is requested"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN; reason: 'variant' and 'local_config' belog to the same feature, therefore only one of them is allowed in command line"
dictUsecase['SECTION']          = "LOCAL_CONFIG"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant2\" --variable local_config:\"./config/tsm-test_config_variant1.json\""
dictUsecase['EXPECTEDRETURN']   = 1 # has to be changed later
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0200"
dictUsecase['DESCRIPTION']      = "Variant with multiple nested configuration files"
dictUsecase['EXPECTATION']      = "Nested configuration files create new parameters and also overwrite already existing ones. Accordingly to the order of definitions the last definition sets the parameter value."
dictUsecase['SECTION']          = "NESTED_CONFIG"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-03.robot" # (with variant configuration and extended logging of parameters from nested configuration files)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"nested_import_1\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0201"
dictUsecase['DESCRIPTION']      = "Variant with multiple nested configuration files and extended parameter definitions (new and overwritten values; all relevant data types)"
dictUsecase['EXPECTATION']      = "Inside robot files all configuration parameters have proper value and are of proper data type"
dictUsecase['SECTION']          = "NESTED_CONFIG"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-04.robot" # (with variant configuration and extended logging of parameters from nested configuration files; all relevant datatypes; logging with pretty_print)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"nested_import_2\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0250"
dictUsecase['DESCRIPTION']      = "Variant with multiple nested configuration files; cyclic import of JSON file"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN; reason: cyclic import"
dictUsecase['SECTION']          = "NESTED_CONFIG"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-03.robot" # (with variant configuration and extended logging of parameters from nested configuration files)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"cyclic_import\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0350"
dictUsecase['DESCRIPTION']      = "Schema file for JSON configuration files is not available"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "SCHEMA_VALIDATION"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['HINT']             = "Temporary modification of installed schema file"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\""
dictUsecase['PRESTEP']          = "ConfigSchemaFile_Remove"
dictUsecase['POSTSTEP']         = "ConfigSchemaFile_Restore"
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0351"
dictUsecase['DESCRIPTION']      = "Schema file for JSON configuration files is invalid because of a syntax error"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "SCHEMA_VALIDATION"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\""
dictUsecase['PRESTEP']          = "ConfigSchemaFile_MakeInvalid"
dictUsecase['POSTSTEP']         = "ConfigSchemaFile_Restore"
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0400"
dictUsecase['DESCRIPTION']      = "'Maximum_version' and 'Minimum_version' not defined"
dictUsecase['EXPECTATION']      = "Test is executed, because of the version control is optional"
dictUsecase['SECTION']          = "VERSION_CONTROL"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"version_control_01\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0401"
dictUsecase['DESCRIPTION']      = "'Maximum_version' initialized with 'None', 'Minimum_version' initialized with 'null'"
dictUsecase['EXPECTATION']      = "Test is executed, because of the version control is optional"
dictUsecase['SECTION']          = "VERSION_CONTROL"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"version_control_02\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0402"
dictUsecase['DESCRIPTION']      = "Only 'Maximum_version' is defined"
dictUsecase['EXPECTATION']      = "Test is executed, because of the version control is optional"
dictUsecase['SECTION']          = "VERSION_CONTROL"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"version_control_03\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0403"
dictUsecase['DESCRIPTION']      = "Only 'Minimum_version' is defined"
dictUsecase['EXPECTATION']      = "Test is executed, because of the version control is optional"
dictUsecase['SECTION']          = "VERSION_CONTROL"
dictUsecase['SUBSECTION']       = "GOODCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"version_control_04\""
dictUsecase['EXPECTEDRETURN']   = 0
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0450"
dictUsecase['DESCRIPTION']      = "'Maximum_version' is invalid (value is not a version number)"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VERSION_CONTROL"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"version_control_05\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0451"
dictUsecase['DESCRIPTION']      = "'Minimum_version' is invalid (value contains blanks only)"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VERSION_CONTROL"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"version_control_06\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0452"
dictUsecase['DESCRIPTION']      = "'Minimum_version' is bigger than 'Maximum_version'"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VERSION_CONTROL"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"version_control_07\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0453"
dictUsecase['DESCRIPTION']      = "'Maximum_version' is smaller than current version"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VERSION_CONTROL"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"version_control_08\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0454"
dictUsecase['DESCRIPTION']      = "'Minimum_version' is bigger than current version"
dictUsecase['EXPECTATION']      = "Test is not executed; error message; test result is UNKNOWN"
dictUsecase['SECTION']          = "VERSION_CONTROL"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-02.robot" # (with variant configuration)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"version_control_09\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0551"
dictUsecase['DESCRIPTION']      = "Robot file contains keyword FAIL"
dictUsecase['EXPECTATION']      = "Test is executed up to position of keyword FAIL; test result is FAIL"
dictUsecase['SECTION']          = "ROBOT_CODE"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-08-fail.robot" # (with variant configuration; keyword FAIL)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\""
dictUsecase['EXPECTEDRETURN']   = 1
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
dictUsecase = {}
dictUsecase['TESTID']           = "TSM_0552"
dictUsecase['DESCRIPTION']      = "Robot file contains keyword UNKNOWN"
dictUsecase['EXPECTATION']      = "Test is executed up to position of keyword UNKNOWN; test result is UNKNOWN"
dictUsecase['SECTION']          = "ROBOT_CODE"
dictUsecase['SUBSECTION']       = "BADCASE"
dictUsecase['COMMENT']          = "Single file execution"
dictUsecase['TESTFILENAME']     = "tsm-testfile-09-unknown.robot" # (with variant configuration; keyword UNKNOWN)
dictUsecase['TESTFOLDERNAME']   = None
dictUsecase['ADDITIONALPARAMS'] = f"--variable variant:\"variant1\""
dictUsecase['EXPECTEDRETURN']   = 256
listofdictUsecases.append(dictUsecase)
del dictUsecase
# --------------------------------------------------------------------------------------------------------------
