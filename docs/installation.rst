.. _installation:

Installation
============

One of the main goals of textract is to make it as easy as possible to
start using textract (meaning that installation should be as quick and
painless as possible). This package is built on top of several python
packages and other source libraries. Python packages are installed
automatically when using ``pip`` or ``uv``. The source libraries are a
separate matter though and largely depend on your operating system.

Modern Python tooling options:

.. code-block:: bash

    # One-off execution
    uvx textract path/to/file.pdf

    # Install as tool
    uv tool install textract

Ubuntu / Debian
---------------

First install system packages using apt-get, then install textract from PyPI:

.. code-block:: bash

    apt-get install python-dev libxml2-dev libxslt1-dev libreoffice-writer unrtf poppler-utils ghostscript tesseract-ocr \
    flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev
    pip install textract
    # or with uv
    uv pip install textract

.. note::

    ``libreoffice-writer`` is *optional*: it is only needed to extract legacy
    ``.doc`` (Word 97-2003) files. See :ref:`converting-legacy-doc-files`.

.. note::

    It may also be necessary to install ``zlib1g-dev`` on Docker
    instances of Ubuntu. See `issue #19
    <https://github.com/deanmalmgren/textract/pull/19>`_ for details

macOS
-----

These steps rely on you having `Homebrew <https://brew.sh/>`_ installed.
First install XQuartz and system packages, then install textract from PyPI:

.. code-block:: bash

    brew install --cask xquartz libreoffice
    brew install ghostscript poppler sox tesseract unrtf swig
    pip install textract
    # or with uv
    uv pip install textract

.. note::

    ``libreoffice`` is *optional*: it is only needed to extract legacy
    ``.doc`` (Word 97-2003) files. See :ref:`converting-legacy-doc-files`.

.. note::

    ``ghostscript`` provides ``ps2ascii`` for ``.ps`` file extraction.

.. note::

    Depending on how you have python configured on your system with
    homebrew, you may also need to install the python
    development header files for textract to properly install.

.. note::

    **pocketsphinx and Python 3.14+ on macOS**: No prebuilt wheel exists yet
    for Python 3.14 on macOS ARM64. When installed from source,
    scikit-build-core's post-build steps invalidate the code signature, causing
    macOS to kill the process with ``SIGKILL (Code Signature Invalid)`` when the
    extension loads. If you see a ``RuntimeError`` mentioning an invalid code
    signature when using ``method="sphinx"``, re-sign the extension:

    .. code-block:: bash

        python -c "
        import subprocess
        from pathlib import Path
        import importlib.util
        spec = importlib.util.find_spec('pocketsphinx')
        for loc in (spec.submodule_search_locations or []):
            for so in Path(loc).glob('_pocketsphinx.cpython-*-darwin.so'):
                subprocess.run(['codesign', '-s', '-', '-f', str(so)], check=True)
                print(f'Re-signed: {so}')
        "

    This is a known upstream issue; once a Python 3.14 macOS wheel is published
    to PyPI the workaround will no longer be needed.

Windows
-------

Install `Chocolatey <https://chocolatey.org/install>`_ then install system packages:

.. code-block:: powershell

    choco install tesseract ghostscript sox.portable poppler libreoffice-fresh -y
    pip install textract
    # or with uv
    uv pip install textract

.. note::

    ``libreoffice-fresh`` is *optional*: it is only needed to extract legacy
    ``.doc`` (Word 97-2003) files. See :ref:`converting-legacy-doc-files`.

.. note::

    Two parsers are **not supported on Windows**:

    - ``.mp3`` / ``.ogg``: `sox.portable <https://community.chocolatey.org/packages/sox.portable>`_
      does not include ``libmad``. SoX dynamically loads ``libmad.dll`` for MP3
      decoding but does not ship it due to patent restrictions — see the
      `SoX mailing list discussion <https://sourceforge.net/p/sox/mailman/message/27169341/>`_.
      Use Linux or macOS where ``libsox-fmt-mp3``/``mad`` are available.

    - ``.rtf``: `unrtf <https://www.gnu.org/software/unrtf/>`_ is a GNU project
      with no Windows port and no Chocolatey package. RTF extraction is only
      available on Linux (``apt install unrtf``) and macOS (``brew install unrtf``).

FreeBSD
-------

First install system packages using pkg, then install textract from PyPI:

.. code-block:: bash

    pkg install lang/python38 devel/py-pip textproc/libxml2 textproc/libxslt editors/libreoffice textproc/unrtf \
    graphics/poppler print/pstotext graphics/tesseract audio/flac multimedia/ffmpeg audio/lame audio/sox \
    graphics/jpeg-turbo
    pip install textract
    # or with uv
    uv pip install textract

.. note::

    ``editors/libreoffice`` is *optional*: it is only needed to extract
    legacy ``.doc`` (Word 97-2003) files. See :ref:`converting-legacy-doc-files`.

.. _converting-legacy-doc-files:

Converting legacy ``.doc`` files
--------------------------------

Legacy ``.doc`` (Word 97-2003 binary) files are extracted with LibreOffice,
which is an *optional* runtime dependency: textract only shells out to the
``soffice`` executable when you actually process a ``.doc`` file, and every
other format works without it.

If you would rather not install LibreOffice alongside textract (for example in
a slim container), you can pre-convert your ``.doc`` files to ``.docx`` once,
elsewhere, and hand the results to textract, whose ``.docx`` parser is pure
Python:

.. code-block:: bash

    soffice --headless --convert-to docx --outdir out/ *.doc

Then run ``textract out/whatever.docx`` as usual. This keeps the heavier
converter out of your extraction pipeline while still supporting legacy
documents.

Headless servers and containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On a headless Linux host (a server, CI runner, or container with no
display), LibreOffice occasionally aborts partway through a ``.doc``
conversion with an error like::

    terminate called after throwing an instance of 'com::sun::star::uno::RuntimeException'
    Unspecified Application Error

This is a LibreOffice issue, not a textract bug: its default graphics
plugin expects a display. Force the headless plugin by setting
``SAL_USE_VCLPLUGIN=svp`` in the environment before running textract:

.. code-block:: bash

    export SAL_USE_VCLPLUGIN=svp
    textract whatever.doc

If the crash still appears intermittently, installing the full
``libreoffice`` package (rather than only ``libreoffice-writer``) and
``dbus-x11`` resolves the remaining headless startup failures.

Reference: CI System Dependencies
----------------------------------

The canonical list of system dependencies is maintained in the GitHub Actions
workflow at `.github/actions/setup/action.yml <https://github.com/deanmalmgren/textract/blob/main/.github/actions/setup/action.yml>`_.
This is what CI uses and is kept up-to-date with each platform's requirements.

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

    - `LibreOffice <https://www.libreoffice.org/>`_ (the ``soffice``
      executable) is *optionally* required by the ``.doc`` parser. It is only
      invoked when you extract a legacy ``.doc`` file; if it isn't installed,
      textract raises an error explaining how to install it or pre-convert the
      file. This replaces ``antiword``, which is no longer maintained or
      packaged. See :ref:`converting-legacy-doc-files` for a batch
      pre-conversion alternative.

    - `pdftotext <https://poppler.freedesktop.org/>`_ (part of poppler) is
      *optionally* required by the ``.pdf`` parser (there is a pure python
      fallback that works if pdftotext isn't installed).

    - `ps2ascii <https://www.ghostscript.com/>`_ (part of ghostscript)
      is required by the ``.ps`` parser.

    - `tesseract-ocr <https://tesseract-ocr.github.io/tessdoc/Installation.html>`_
      is required by the ``.jpg``, ``.png`` and ``.gif`` parser.

    - `sox <https://sox.sourceforge.net/>`_
      is required by the ``.mp3`` and ``.ogg`` parser.
      You need to install ffmpeg, lame, libmad0 and libsox-fmt-mp3,
      before building sox, for these filetypes to work.

2. Add a requirements file to the `requirements directory
   <https://github.com/deanmalmgren/textract/tree/master/requirements>`_
   of the project with the lower-cased name of your operating system
   (e.g. ``requirements/windows``) so we can try to keep these things
   up to date in the future.
