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
extremely good documentation. If you notice a typo, error, confusing
statement etc, please fix it!


.. _contributing-quick-start:

Quick start
-----------

1. `Fork <https://github.com/KyleKing/textract-py3/fork>`_ and clone the
   project:

   .. code-block:: bash

        git clone https://github.com/YOUR-USERNAME/textract-py3.git

2. Install development dependencies using `uv <https://docs.astral.sh/uv/>`_:

   .. code-block:: bash

        uv sync --group dev

3. Make your changes and run the test suite:

   .. code-block:: bash

        uv run pytest

4. Submit a pull request with your changes.

CI is handled by GitHub Actions, which runs tests across multiple Python
versions and operating systems.


System dependencies
~~~~~~~~~~~~~~~~~~~

Some parsers require system-level dependencies. See the
:ref:`installation <installation>` guide for details on installing
these for your operating system.
