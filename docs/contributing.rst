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


.. _contributing-release:

Releasing
---------

This project uses `commitizen <https://commitizen-tools.github.io/commitizen/>`_
for version management and `PyPI Trusted Publishers <https://docs.pypi.org/trusted-publishers>`_
for secure, token-free publishing from GitHub Actions. Commitizen automatically
updates version numbers in ``pyproject.toml`` and ``textract/__init__.py``.

Initial Setup (One-time)
~~~~~~~~~~~~~~~~~~~~~~~~~

Before publishing for the first time, configure Trusted Publishing on PyPI:

1. Go to your project's page on PyPI: ``https://pypi.org/manage/project/textract-py3/settings/publishing/``

   - If the project doesn't exist yet, go to `PyPI's publishing page <https://pypi.org/manage/account/publishing>`_ to add a "pending" publisher

2. Add a new Trusted Publisher with these settings:

   - **PyPI Project Name**: ``textract-py3``
   - **Owner**: ``KyleKing``
   - **Repository name**: ``textract-py3``
   - **Workflow name**: ``ci_pipeline.yml`` (``.github/workflows/ci_pipeline.yml``)
   - **Environment name**: ``pypi``

3. Configure the GitHub Environment:

   - Go to your repository's ``Settings`` → ``Environments``
   - Create an environment named ``pypi``
   - (Recommended) Enable "Required reviewers" for production safety

Publishing a Release
~~~~~~~~~~~~~~~~~~~~~

Use commitizen to bump versions and create tags. You can use either ``mise`` tasks
or run ``uv`` commands directly:

.. code-block:: bash

    # Show current version
    uv run cz version --project

    # Preview unreleased changes
    mise run changelog:preview
    # Or: uv run cz changelog --dry-run | head -50

    # Bump version
    mise run release:bump -- --increment MINOR  # or PATCH, MAJOR
    # Or: uv run cz bump --increment MINOR

    # Update changelog (semi-automated via mise task)
    mise run changelog:update
    # This runs scripts/prepend-changelog.sh

    # Preview without committing
    uv run cz bump --dry-run --yes

The ``cz bump`` command automatically:

- Updates version numbers in ``pyproject.toml`` and ``textract/__init__.py``
- Creates a git commit with the changes
- Creates a git tag (format: ``v2.1.2``)

After bumping, push the commit and tag to trigger the GitHub Action:

.. code-block:: bash

    # Push the commit and tag
    git push origin main --tags

The GitHub Action will automatically:

- Run tests across multiple Python versions and operating systems
- Build the package with ``uv build``
- Publish to PyPI using Trusted Publishers (no API tokens needed)
- Generate a changelog from commit messages using commitizen
- Create a GitHub Release with the changelog

**Note:** The changelog in ``docs/changelog.rst`` is currently maintained manually
to preserve the existing format and historical entries. The GitHub Action generates
release notes automatically, but the manual changelog remains for documentation purposes.

Changelog Management
~~~~~~~~~~~~~~~~~~~~

The project maintains a manual changelog in ``docs/changelog.rst``. You have
three options for managing changelog updates:

**Option 1: Semi-Automated (Recommended)**

Use the ``scripts/prepend-changelog.sh`` script to generate and prepend new
entries non-destructively:

.. code-block:: bash

    # Preview unreleased changes before bumping
    mise run changelog:preview
    # Or: ./scripts/prepend-changelog.sh --preview

    # After running `cz bump`, update the changelog
    mise run changelog:update
    # Or: ./scripts/prepend-changelog.sh

    # Review and commit the changes
    diff docs/changelog.rst.backup docs/changelog.rst
    git add docs/changelog.rst
    rm docs/changelog.rst.backup

This approach generates new entries from conventional commits and prepends them
to the existing changelog without destroying historical entries.

**Option 2: Manual Updates**

After bumping versions, manually add entries under the "latest changes in
development for next release" section in ``docs/changelog.rst``.

**Option 3: Full Auto-Generation**

Commitizen can generate a complete changelog from git commit messages:

.. code-block:: bash

    # Preview auto-generated changelog (RST format)
    uv run cz changelog --dry-run

    # Generate complete changelog (overwrites docs/changelog.rst)
    uv run cz changelog

    # Generate for specific version range
    uv run cz changelog 2.1.0..2.2.0 --dry-run

**Warning:** Running ``uv run cz changelog`` without ``--dry-run`` will overwrite
the existing changelog file. The auto-generated format differs from the current
manual format. Review the dry-run output before committing to this approach.

To enable automatic changelog updates on version bumps, set
``update_changelog_on_bump = true`` in the ``[tool.commitizen]`` section of
``pyproject.toml``. This requires migrating the existing changelog to
commitizen's format first.

**Changelog Format:** For auto-generated changelogs to categorize commits properly,
use conventional commit prefixes like ``feat:``, ``fix:``, ``refactor:``,
``docs:``, ``test:``, ``ci:``, etc. in commit messages.
