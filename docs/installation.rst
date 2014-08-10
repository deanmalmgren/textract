.. _installation:

Installation
============

One of the main goals of textract is to make it as easy as possible to
start using textract (meaning that installation should be as quick and
painless as possible). This package is built on top of several python
packages and other source libraries. Assuming you are using ``pip`` or
``easy_install`` to install textract, the `python packages
<https://github.com/deanmalmgren/textract/blob/master/requirements/python>`__
are all installed by default with textract. The source libraries are a
separate matter though and largely depend on your operating system.

Ubuntu / Debian
---------------

There are two steps required to run this package on
Ubuntu/Debian. First you must install some system packages using the
`apt-get <https://help.ubuntu.com/12.04/serverguide/apt-get.html>`__
package manager before installing textract from pypi.

.. code-block:: bash

    apt-get install python-dev libxml2-dev libxslt1-dev antiword poppler-utils
    pip install textract

.. note::

    It may also be necessary to install ``zlib1g-dev`` on Docker
    instances of Ubuntu. See `issue #19
    <https://github.com/deanmalmgren/textract/pull/19>`_ for details

OSX
---

There are three steps required to run this package on OSX
systems. First you must install some system packages using `homebrew
<http://brew.sh/>`__ (or similar) package manager before linking the
source code with homebrew and installing textract from pypi.

.. code-block:: bash

    brew install libxml2 libxslt antiword poppler
    brew link libxml2 libxslt
    pip install textract

.. note::

    Depending on how you have python configured on your system with
    homebrew, you may also need to install the python
    development header files for textract to properly install.


Don't see your operating system installation instructions here?
---------------------------------------------------------------

My appologies! Installing system packages is a bit of a drag and its
hard to anticipate all of the different environments that need to be
accomodated (wouldn't it be awesome if there were a system-agnostic
package manager or, better yet, if python could install these system
dependencies for you?!?!). If you're operating system doesn't have
documenation about how to install the textract dependencies, please
:ref:`contribute a pull request <contributing>` with:

1. A new section in here with the appropriate details about how to
   install things. In particular, please give instructions for how to
   install the following libraries before running ``pip install
   textract``:

    - `libxml2 2.6.21 or later <http://xmlsoft.org/downloads.html>`__
      is required by the ``.docx`` parser which uses `lxml
      <http://lxml.de/installation.html#requirements>`__ via
      python-docx.

    - `libxslt 1.1.15 or later
      <http://xmlsoft.org/XSLT/downloads.html>`__ is required by the
      ``.docx`` parser which users `lxml
      <http://lxml.de/installation.html#requirements>`__ via
      python-docx.

    - python header files are required for building lxml.

    - `antiword <http://www.winfield.demon.nl/>`__ is required by the
      ``.doc`` parser.

    - `pdftotext <http://poppler.freedesktop.org/>`__ is *optionally*
      required by the ``.pdf`` parser (there is a pure python fallback
      that works if pdftotext isn't installed).

2. Add a requirements file to the `requirements directory
   <https://github.com/deanmalmgren/textract/tree/master/requirements>`__
   of the project with the lower-cased name of your operating system
   (e.g. ``requirements/windows``) so we can try to keep these things
   up to date in the future.
