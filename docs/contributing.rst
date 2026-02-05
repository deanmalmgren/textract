.. _contributing:

Contributing
============

The overarching goal of this project is to make it as easy as possible
to extract raw text from any document for the purposes of most natural
language processing tasks. In practice, this means that this project
should preferentially provide tools that correctly produce output that
has words in the correct order but that whitespace between words,
formatting, etc is totally irrelevant. As the various parsers mature,
I fully expect the output to become more readable to support
additional use cases, like `extracting text to appear in web pages
<https://github.com/deanmalmgren/textract/pull/58#issuecomment-53697943>`_.

Importantly, this project is committed to being as agnostic about how
the content is extracted as it is about the means in which the text is
analyzed downstream. This means that ``textract`` should support
multiple modes of extracting text from any document and provide
reasonably good defaults (defaulting to tools that tend to produce the
correct word sequence).

Another important aspect of this project is that we want to have
extremely good documentation. If you notice a type-o, error, confusing
statement etc, please fix it!


.. _contributing-quick-start:

Quick start
-----------

1. `Fork <https://github.com/deanmalmgren/textract/fork>`_ and clone the
   project:

   .. code-block:: bash

        git clone https://github.com/YOUR-USERNAME/textract.git

2. Install dependencies and run tests:

   .. code-block:: bash

        uv sync --group dev
        uv run pytest

3. Install system dependencies for your platform. See the
   :ref:`installation <installation>` guide for platform-specific
   instructions (macOS, Ubuntu/Debian, Windows, FreeBSD).

4. Contribute! There are several `open issues
   <https://github.com/deanmalmgren/textract/issues>`_ that provide
   good places to dig in and send pull requests; your help is greatly
   appreciated!

   Current build status: |Build Status|


.. |Build Status| image:: https://travis-ci.org/deanmalmgren/textract.png
   :target: https://travis-ci.org/deanmalmgren/textract


Contribution workflow
---------------------

Any and all contributions are welcome and appreciated. To make it easy
to keep things organized, this project uses the
`general guidelines <https://guides.github.com/introduction/flow/>`_
for the fork-branch-pull request model for github. Briefly, this means:

1. Make sure your fork's ``master`` branch is up to date:

   .. code-block:: bash

        git remote add deanmalmgren https://github.com/deanmalmgren/textract.git
        git checkout master
        git pull deanmalmgren/master

2. Start a feature branch with a descriptive name about what you're
   trying to accomplish:

   .. code-block:: bash

        git checkout -b csv-support

3. Make commits to this feature branch (``csv-support``, in this case)
   in a way that other people can understand with good commit messages
   to explain the changes you've made:

   .. code-block:: bash

        emacs textract/parsers/csv_parser.py
        git add textract/parsers/csv_parser.py
        git commit -m 'added csv_parser'

4. If an issue already exists for the code you're contributing, use
   `issue2pr <http://issue2pr.herokuapp.com/>`_ to attach your code to
   that issue:

   .. code-block:: bash

        git push origin csv-support
        chrome http://issue2pr.herokuapp.com
        # enter the issue URL, HEAD=yourusername:csv-support, Base=master

   If the issue doesn't already exist, just send a pull
   request in the usual way:

   .. code-block:: bash

        git push origin csv-support
        chrome http://github.com/deanmalmgren/textract/compare


Common contributions: support for new file type
------------------------------------------------

This project has really taken off, much more so than I would have
thought (thanks everybody!). To help new contributors, I thought I'd
jot down some notes for one of the more common contributions---how to
add support for hitherto unsupported file type ``.abc123``:

* write a ``Parser`` class in ``textract/parsers/abc123_parser.py`` that
  inherits from ``textract.parsers.utils.BaseParser`` or
  ``textract.parsers.utils.ShellParser`` and implements the
  ``extract(self, filename, **kwargs)`` method.

* add a test file in ``tests/abc123/raw_text.abc123``, run textract on
  it like this:

  .. code-block:: shell

     textract tests/abc123/raw_text.abc123 > tests/abc123/raw_text.txt

  and add the basic test suite by creating
  a file called ``tests/test_abc123.py`` with content that looks
  something like this:

  .. code-block:: python

     # tests/test_abc123.py
     import unittest

     import base


     class Abc123TestCase(unittest.TestCase, base.BaseParserTestCase):
         extension = 'abc123'

  now you should be able to run tests on your parser with ``uv run pytest
  tests/test_abc123.py`` or the tests for every parser with ``uv run pytest``.

* if your package relies on any external sources, be sure to add them
  in ``pyproject.toml`` (for python packages) or document system
  dependencies and update the installation documentation accordingly in
  ``docs/installation.rst``.

* add documentation about the awesome new file format this is being
  supported in ``docs/index.rst``

* finally, make sure the entire test suite passes by running
  ``uv run pytest`` and fix any lingering problems.


Style guidelines
----------------

As a general rule of thumb, the goal of this package is to be as
readable as possible to make it easy for novices and experts alike to
contribute to the source code in meaningful ways. Pull requests that
favor cleverness or optimization over readability are less likely to be
incorporated.

To make this notion of "readability" more concrete, here are a few
stylistic guidelines that are inspired by other projects and we
generally recommend:

-  write functions and methods that can `fit on a screen or two of a
   standard
   terminal <https://www.kernel.org/doc/Documentation/CodingStyle>`_
   --- no more than approximately 40 lines.

-  unless it makes code less readable, adhere to `PEP
   8 <http://legacy.python.org/dev/peps/pep-0008/>`_ style
   recommendations --- use an appropriate amount of whitespace.

-  `code comments should be about *what* is being done, not *how* it is
   being done <https://www.kernel.org/doc/Documentation/CodingStyle>`_
   --- that should be self-evident from the code itself.


Development Setup
-----------------

Install dependencies::

    uv sync

Install system dependencies (macOS)::

    brew install antiword tesseract ghostscript poppler sox unrtf

Install system dependencies (Ubuntu/Debian)::

    apt-get install antiword tesseract-ocr ghostscript poppler-utils sox libsox-fmt-mp3 unrtf

Install system dependencies (Windows)::

    choco install tesseract ghostscript sox.portable poppler -y

.. note::

   The canonical list of system dependencies is in `.github/actions/setup/action.yml
   <https://github.com/deanmalmgren/textract/blob/main/.github/actions/setup/action.yml>`_.


Releasing
---------

Releases are handled via GitHub Actions with manual triggering:

1. Push conventional commits (``feat:``, ``fix:``, etc.) to ``main``
2. Manually trigger the ``Bump Version`` workflow from GitHub Actions tab
3. The workflow analyzes commits, bumps version, updates changelog, and creates release
4. The ``ci_pipeline.yml`` workflow automatically publishes to PyPI on tag creation

To preview what version would be bumped::

    uv run cz bump --dry-run

