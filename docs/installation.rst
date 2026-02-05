.. _installation:

Installation
============

One of the main goals of textract is to make it as easy as possible to
start using textract (meaning that installation should be as quick and
painless as possible). This package is built on top of several python
packages and other source libraries. Assuming you are using ``pip`` or
``easy_install`` to install textract, the `python packages
<https://github.com/deanmalmgren/textract/blob/master/requirements/python>`_
are all installed by default with textract. The source libraries are a
separate matter though and largely depend on your operating system.

Ubuntu / Debian
---------------

There are two steps required to run this package on
Ubuntu/Debian. First you must install some system packages using the
`apt-get <https://help.ubuntu.com/14.04/serverguide/apt-get.html>`_
package manager before installing textract from pypi.

.. code-block:: bash

    apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
    flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev
    pip install textract

.. note::

    It may also be necessary to install ``zlib1g-dev`` on Docker
    instances of Ubuntu. See `issue #19
    <https://github.com/deanmalmgren/textract/pull/19>`_ for details

OSX
---

These steps rely on you having `homebrew <http://brew.sh/>`_ installed
as well as the `cask <http://caskroom.io/>`_ plugin (``brew tap caskroom/cask``). The basic idea is to first install
`XQuartz <https://xquartz.macosforge.org/landing/>`_ before
installing a bunch of system packages before installing textract from
pypi.

.. code-block:: bash

    brew install --cask xquartz
    brew install poppler antiword unrtf tesseract swig
    pip install textract

..     brew install libxml2 libxslt antiword poppler tesseract
..     brew link libxml2 libxslt

.. note::

    `pstotext <http://pages.cs.wisc.edu/~ghost/doc/pstotext.htm>`_ is
    not currently a part of homebrew so ``.ps`` extraction must be
    enabled by manually installing from source.

.. note::

    Depending on how you have python configured on your system with
    homebrew, you may also need to install the python
    development header files for textract to properly install.

FreeBSD
-------

Setting up this package on FreeBSD pretty much follows the steps for
Ubuntu / Debian while using ``pkg`` as package manager.

.. code-block:: bash

    pkg install lang/python38 devel/py-pip textproc/libxml2 textproc/libxslt textproc/antiword textproc/unrtf \
    graphics/poppler print/pstotext graphics/tesseract audio/flac multimedia/ffmpeg audio/lame audio/sox \
    graphics/jpeg-turbo
    pip install textract

Don't see your operating system installation instructions here?
---------------------------------------------------------------

My apologies! Installing system packages is a bit of a drag and its
hard to anticipate all of the different environments that need to be
accommodated (wouldn't it be awesome if there were a system-agnostic
package manager or, better yet, if python could install these system
dependencies for you?!?!). If you're operating system doesn't have
documentation about how to install the textract dependencies, please
:ref:`contribute a pull request <contributing>` with:

1. A new section in here with the appropriate details about how to
   install things. In particular, please give instructions for how to
   install the following libraries before running ``pip install
   textract``:

    - `libxml2 2.6.21 or later <http://xmlsoft.org/downloads.html>`_
      is required by the ``.docx`` parser which uses `lxml
      <http://lxml.de/installation.html#requirements>`_ via
      python-docx.

    - `libxslt 1.1.15 or later
      <http://xmlsoft.org/XSLT/downloads.html>`_ is required by the
      ``.docx`` parser which users `lxml
      <http://lxml.de/installation.html#requirements>`_ via
      python-docx.

    - python header files are required for building lxml.

    - `antiword <http://www.winfield.demon.nl/>`_ is required by the
      ``.doc`` parser.

    - `pdftotext <http://poppler.freedesktop.org/>`_ is *optionally*
      required by the ``.pdf`` parser (there is a pure python fallback
      that works if pdftotext isn't installed).

    - `pstotext <http://pages.cs.wisc.edu/~ghost/doc/pstotext.htm>`_
      is required by the ``.ps`` parser.

    - `tesseract-ocr <https://code.google.com/p/tesseract-ocr/>`_
      is required by the ``.jpg``, ``.png`` and ``.gif`` parser.

    - `sox <http://sox.sourceforge.net/>`_
      is required by the ``.mp3`` and ``.ogg`` parser.
      You need to install ffmpeg, lame, libmad0 and libsox-fmt-mp3,
      before building sox, for these filetypes to work.

2. Add a requirements file to the `requirements directory
   <https://github.com/deanmalmgren/textract/tree/master/requirements>`_
   of the project with the lower-cased name of your operating system
   (e.g. ``requirements/windows``) so we can try to keep these things
   up to date in the future.
