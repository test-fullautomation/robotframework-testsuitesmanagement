REPOSITORY CONFIGURATION
========================

XC-CI1/ECA3-Queckenstedt

Last change: 31.08.2021

Table of content
----------------

| `Repository content`_
| `Folders`_
| `Files`_
| `Preconditions`_
| `Additional hints`_
| `How to start?`_
| `References`_

Repository content
------------------

* Package code
* Sphinx documentation project files
* Additional source files needed for package documentation
* Application to generate the package documentation
* Application to install the package (including the package documentation)

TOC_


Folders
-------

``atest``
  Contains test files.

``config``
  Contains a ``CConfig`` class storing all repository specific values like
  the name of the package, the name of the author and so on.

  Computes all paths to files and folders inside the repository and inside the
  installation location (usually the ``site-packages`` folder of the Python installation)
  relative to the position of the application that imports ``CConfig``.

  All documentation and setup related scripts need to import this class and need to work with the provided values
  to avoid duplicate definition of common parameter.

``doc``
  Sphinx package documentation project root folder.

  Contains all files related to Sphinx package documentation:

  * Sphinx project files (``conf.py``, ``index.rst``)
  * Additional documentation source files in reStructuredText format (``.rst``), pictures, LaTeX addons, ...
  * The generated package documentation itself (formats: HTML, TEX, PDF)

``doc/_static``
  Do not remove; required by Sphinx.

``doc/_templates``
  Do not remove; required by Sphinx.

``doc/_build/html``
  Sphinx output: HTML version of package documentation.

``doc/_build/latex``
  Sphinx output: LaTeX and PDF version of package documentation.

  The PDF version requires a LaTeX installation under ``%ROBOTLATEXPATH%/miktex/bin/x64/pdflatex.exe``
  together ``with self.__bGenPDFSupported = True`` (default).

  This is defined in ``config/CConfig.py``.

``doc/additional_doc``
  Additional files in reStructuredText format that have to be added to the package documentation
  (additionally to the content of the docstrings of the documented Python modules within the package).

  Files inside this folder have to be listed within ``doc/index.rst``.

``doc/images``
  Images to be added to the package documentation.

  The intention behind this is to have the possibility to add pictures to additional files within ``doc/additional_doc``.

  **Caution:** The links to picture files have to be absolute! The reference is the root path of the Sphinx documentation project (``doc``)
  and not the position of the document that imports the picture!

  Sphinx puts the documentation into ``doc/_build/html`` and ``doc/_build/latex``. These are complete different locations
  than the root folders ``doc/additional_doc`` and ``doc/images``. While generating the documentation Sphinx takes care about a proper conversion of
  all links to imported pictures (also the pictures are copied; the content of ``doc/_build`` is standalone)!

  Example: How to import a picture within an additional rst file:

  ``.. image:: /images/DocTest.jpg``

  Impediment: LaTeX does not support bitmaps (in opposite to HTML). Please use the jpg or png format for imported pictures.

``<package name>``
  The Python package itself

TOC_


Files
-----

``setup.py``
  Extended package installation.

  Includes the call of ``sphinx-makeall.py``.

  Also all destination folders are deleted at the beginning.

  Package installation:

  * ``%ROBOTPYTHONPATH%/Lib/site-packages/<package name>``

  Package documentation installation:

  * ``%ROBOTPYTHONPATH%/Lib/site-packages/<package name>_doc``

``sphinx-makeall.py``
  Generates the package documentation.

  Access:

  * ``doc/_build/html/index.html``
  * ``doc/_build/latex/*.tex``
  * ``doc/_build/latex/*.pdf``

  Previous output is deleted at the beginning.

``config/CConfig.py``
  The repository configuration contains all repository specific information like the name of the Python package and the name of the author,
  and also computes the paths to files and folders needed by ``sphinx-makeall.py`` and ``setup_ext.py``.

``conf.py``
  The configuration file for the Sphinx documentation builder. Contains also repository specific adaptions that must be done manually
  (this file does not use ``config/CConfig.py``).

``index.rst``
  The Sphinx documentation master file.

  Settings to make here:

  * Include additional rst files (if required)
  * List the names of all Python modules of the package (that shall be part of the package documentation)
  * Define the structure of the table of content of the package documentation

TOC_


Preconditions
-------------

* The generation of the package documentation in ``HTML`` format and in ``TEX`` format requires *Sphinx*.

* The generation of a ``PDF`` document out of ``TEX`` sources requires *LaTeX*.

* The conversion between several markdown formats requires *pandoc* and *pypandoc*.

* It is assumed that the repository documentation happens based on the file ``README.rst`` within the repository root folder.

  The ``md`` version of this file (``README.md``) is created automatically with the help of pypandoc (triggered by ``sphinx-makeall.py``;
  output within same folder).

  Therefore the file ``README.md`` must not be edited manually. Manual changes within this file will be overwritten
  with the next call of ``sphinx-makeall.py``.

TOC_


Additional hints
----------------

* Empty lines are a syntax element of markdown. For proper conversion between several markdown formats it is strongly required
  that the source file has proper line endings (**LF** for Linux and **CR+LF** for Windows). If not pandoc creates improper output.

  In case of doubts please check the settings of the editor you use.

* The conversion of ``README.rst`` to ``README.md`` is done with the help of pypandoc. This means that Python code is involved.

  When writing back the converted file content to the output file it is not enough simply to use ``outputfilehandle.write(sFileContent)``,
  because this adds additional blank lines.

  It is an experience that only ``splitlines()`` is able to handle operating system dependend line breaks in a proper way.
  Therefore it is required to go the long winded way:

  | ``sFileContent = pypandoc.convert_file(sFile_rst, 'md')``
  | ``hFile_md = open(sFile_md, "w", encoding="utf-8")``
  | ``listFileContent = sFileContent.splitlines()``
  | ``for sLine in listFileContent:``
  |     ``hFile_md.write(sLine + "\n")``
  | ``hFile_md.close()``
   
* It is possible to add other ``rst`` files to the package documentation. Even in case of they are *standalone* it has to be considered
  that within the package documentation the content of these files *is only a part of a larger document*.

  You may cause conflicts (e.g. *duplicate label* warnings) when inside the additional ``rst`` files you accidently define the same headlines
  or labels than already used by Sphinx for the package documentation.

  In case of doubts please refer to ``index.rst`` in which the main structure of the package documentation is defined.

TOC_


How to start?
-------------

* Prepare docstrings of all Python modules of the package accordingly to reStructuredText syntax
* Add additional files if required
* Adapt ``conf.py`` and ``index.rst``
* Adapt ``config/CConfig.py``
* Give it a try: ``sphinx-makeall.py``

TOC_


References
----------

For further details about documentation please refer to:

https://devguide.python.org/documenting/

https://docutils.sourceforge.io/docs/ref/rst/directives.html

https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html

https://docutils.sourceforge.io/docs/user/rst/quickref.html

https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

https://www.markdownguide.org/basic-syntax/

https://www.sphinx-doc.org/en/master/usage/configuration.html

TOC_



.. _TOC: `Table of content`_
