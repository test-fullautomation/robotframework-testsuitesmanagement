import os
import site
import sys
import importlib.util


if os.environ.get("COVERAGE_PROCESS_START"):
   for sSitePackagePath in site.getsitepackages():
      sCoverageInit = os.path.join(sSitePackagePath, "coverage", "__init__.py")
      if os.path.isfile(sCoverageInit):
         oCoverageSpec = importlib.util.spec_from_file_location(
            "coverage",
            sCoverageInit,
            submodule_search_locations=[os.path.dirname(sCoverageInit)],
         )
         oCoverageModule = importlib.util.module_from_spec(oCoverageSpec)
         sys.modules["coverage"] = oCoverageModule
         oCoverageSpec.loader.exec_module(oCoverageModule)
         oCoverageModule.process_startup()
         break