.. _contributing:

Contributing
============

.. note::
   The primary contributor documentation is in `CONTRIBUTING.md <https://github.com/KyleKing/textract-py3/blob/main/CONTRIBUTING.md>`_
   at the repository root. This page provides a summary for the documentation site.

This is a maintained fork of `deanmalmgren/textract <https://github.com/deanmalmgren/textract>`_
focused on minimizing dependencies and supporting modern Python.

The overarching goal is to make it as easy as possible to extract raw text from any document
for natural language processing tasks. In practice, this means prioritizing correct word order
over formatting and supporting multiple extraction methods for each file type.

.. _contributing-quick-start:

Quick start
-----------

1. `Fork <https://github.com/KyleKing/textract-py3/fork>`_ and clone the project:

   .. code-block:: bash

        git clone https://github.com/YOUR-USERNAME/textract-py3.git
        cd textract-py3

2. Install development dependencies using `uv <https://docs.astral.sh/uv/>`_:

   .. code-block:: bash

        uv sync --group dev

3. Make your changes and run the test suite:

   .. code-block:: bash

        uv run pytest

4. Submit a pull request with your changes.

CI is handled by GitHub Actions, which runs tests across multiple Python
versions (3.9-3.14) and operating systems (Ubuntu, macOS, Windows).

System dependencies
~~~~~~~~~~~~~~~~~~~

Some file types require system-level tools. See the :ref:`installation <installation>`
guide for platform-specific installation instructions:

- ``.doc`` requires ``antiword``
- ``.pdf`` requires ``pdftotext`` (from poppler-utils) or uses built-in ``pdfminer``
- ``.jpg``, ``.png`` require ``tesseract`` for OCR
- ``.ps`` requires ``ghostscript``
- ``.rtf`` requires ``unrtf``
- ``.wav`` requires ``sox`` and ``SpeechRecognition``

.. _contributing-release:

Releasing
---------

Publishing is automated via GitHub Actions with `PyPI Trusted Publishers <https://docs.pypi.org/trusted-publishers>`_.
No API tokens needed.

Basic release workflow:

.. code-block:: bash

    # Preview unreleased changes
    mise run changelog:preview

    # Bump version (PATCH, MINOR, or MAJOR)
    mise run release:bump -- --increment MINOR

    # Update changelog
    mise run changelog:update

    # Push to trigger automated publishing
    git push origin main --tags

For detailed release instructions, prerelease workflows, and changelog management options,
see `CONTRIBUTING.md <https://github.com/KyleKing/textract-py3/blob/main/CONTRIBUTING.md#releasing>`_.

Local Testing
-------------

Test GitHub Actions workflows locally using `Act <https://github.com/nektos/act>`_ for
Linux/macOS, or cloud VMs for Windows testing.

For comprehensive local testing documentation including Windows testing options,
see `CONTRIBUTING.md <https://github.com/KyleKing/textract-py3/blob/main/CONTRIBUTING.md#local-ci-testing>`_.

Pull Requests
-------------

When submitting PRs:

- Include tests for new functionality
- Update documentation if adding features or changing behavior
- Follow existing code style (enforced by ruff)
- Use conventional commit messages for changelog generation
- Ensure CI passes on all platforms before requesting review

For more details, see `CONTRIBUTING.md <https://github.com/KyleKing/textract-py3/blob/main/CONTRIBUTING.md>`_.
