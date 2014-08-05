.. textract documentation master file, created by
   sphinx-quickstart on Fri Jul  4 11:09:09 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

textract
================================

As undesireable as it might be, more often than not there is extremely
useful information embedded in Word documents, PowerPoint
presentations, PDFs, etc---so-called "dark data"---that would be
valuable for further textual analysis and visualization. While
:ref:`several packages <supporting>` exist for extracting content from
each of these formats on their own, this package provides a single
interface for extracting content from any type of file, without any
irrelevant markup.

This package provides two primary facilities for doing this, the
:ref:`command line interface <command-line-interface>`

.. code-block:: bash

    textract path/to/file.extension

or the :ref:`python package <python-package>`

.. code-block:: python

    # some python file
    import textract
    text = textract.process("path/to/file.extension")

.. _supporting:

Currently supporting
--------------------

* ``.doc`` via `antiword <http://www.winfield.demon.nl/>`__

* ``.docx`` via `python-docx <https://python-docx.readthedocs.org/en/latest/>`__

* ``.eml`` via python builtins.

* ``.json`` via python builtins.

* ``.html`` via `beautifulsoup4 <http://beautiful-soup-4.readthedocs.org/en/latest/>`__

* ``.pptx`` via `python-pptx <https://python-pptx.readthedocs.org/en/latest/>`__

* ``.pdf`` via `pdftotext <http://poppler.freedesktop.org/>`__ (default) or `pdfminer <https://euske.github.io/pdfminer/>`__

* ``.txt`` via python builtins.

Please recommend other file types by either mentioning them on the
`issue tracker <https://github.com/deanmalmgren/textract/issues>`__ or
by :ref:`contributing <contributing>`

Installation
------------

This package is built on top of several python packages and other
source libraries. In particular, this package has a dependency on lxml
that depends on `some other libraries to be installed
<http://lxml.de/installation.html#requirements>`__. 


Ubuntu/Debian
~~~~~~~~~~~~~

There are two steps required to run this package on
Ubuntu/Debian. First you must install some system packages using the
`apt-get <https://help.ubuntu.com/12.04/serverguide/apt-get.html>`__
package manager before installing textract from pypi.

.. code-block:: bash

    apt-get install python-dev libxml2-dev libxslt1-dev antiword poppler-utils
    pip install textract


OSX
~~~

There are two steps required to run this package on OSX systems. First
you must install some system packages using `homebrew
<http://brew.sh/>`__ (or similar) package manager before installing
textract from pypi.

.. code-block:: bash

    brew install libxml2 libxslt antiword poppler
    brew link libxml2 libxslt
    pip install textract

.. note::

    Depending on how you have python configured on your system with
    homebrew, you may also need to install the python
    development header files for textract to properly install.


Don't see your operating system installation instructions here?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

My appologies! Installing system packages is a bit of a drag and its
hard to anticipate all of the different environments that need to be
accomodated (wouldn't it be awesome if there were a system-agnostic
package manager or, better yet, if python could install these system
dependencies for you?!?!). If you're operating system doesn't have
documenation about how to install the textract dependencies, please
:ref:`contribute a pull request <contributing>` with::

1. A new section in here with the appropriate details about how to
   install things.

2. Add a requirements file to the `requirements directory
   <https://github.com/deanmalmgren/textract/tree/master/requirements>`__
   of the project with the lower-cased name of your operating system
   (e.g. ``requirements/windows``) so we can try to keep these things
   up to date in the future.


Contents:

.. toctree::
   :maxdepth: 2

   command_line_interface
   python_package
   contributing
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

