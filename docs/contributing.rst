.. _contributing:

Contributing
============

.. note::

   See `CONTRIBUTING.md <https://github.com/deanmalmgren/textract/blob/main/CONTRIBUTING.md>`_
   for detailed contributor documentation.

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
   good places to dig in. Check out the `contribution guidelines
   <https://github.com/deanmalmgren/textract/blob/main/CONTRIBUTING.md>`_
   and send pull requests; your help is greatly appreciated!

   Current build status: |Build Status|


.. |Build Status| image:: https://travis-ci.org/deanmalmgren/textract.png
   :target: https://travis-ci.org/deanmalmgren/textract

