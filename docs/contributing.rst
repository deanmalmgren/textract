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

3. Contribute! There are several `open issues
   <https://github.com/deanmalmgren/textract/issues>`_ that provide
   good places to dig in. Check out the `contribution guidelines
   <https://github.com/deanmalmgren/textract/blob/main/CONTRIBUTING.md>`_
   and send pull requests; your help is greatly appreciated!

Depending on your development preferences, there are lots of ways to
get started developing with textract:

Developing in a native Ubuntu environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. Install all the necessary system packages:

   .. code-block:: bash

       ./provision/travis-mock.sh
       ./provision/debian.sh

       # optionally run some of the steps in these scripts, but you
       # may want to be selective about what you do as they alter global
       # environment states
       ./provision/python.sh
       ./provision/development.sh

.. _run-ubuntu-tests:

5. Make sure everything is working by running the suite of functional tests:

   .. code-block:: bash

        uv run pytest

   These functional tests are designed to be run on Ubuntu/Debian
   systems. You can run all tests with:

   .. code-block:: bash

        uv run pytest

   Current build status: |Build Status|


Developing with Vagrant virtual machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. Install `Vagrant <http://vagrantup.com/downloads>`_ and
   `Virtualbox <https://www.virtualbox.org/wiki/Downloads>`_ and launch
   the development virtual machine:

   .. code-block:: bash

        vagrant plugin install iniparse
        vagrant up && vagrant provision

   On ``vagrant ssh``\ ing to the virtual machine, note that the
   ``PYTHONPATH`` and ``PATH`` `environment variables have been
   altered in this virtual machine
   <https://github.com/deanmalmgren/textract/blob/master/provision/development.sh>`_
   so that any changes you make to textract in development are
   automatically incorporated into the command.

5. Make sure everything is working by running the test suite:

   .. code-block:: bash

        uv run pytest

   Current build status: |Build Status|



Developing with Docker container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. Go to the `Docker
   documentation <http://docs.docker.com/installation/ubuntulinux/>`_
   and follow the instructions under "If you'd like to try the latest
   version of Docker" to install Docker.

5. Just run ``tests/run_docker_tests.sh`` to run the full test suite.
   Current build status: |Build Status|


.. |Build Status| image:: https://travis-ci.org/deanmalmgren/textract.png
   :target: https://travis-ci.org/deanmalmgren/textract

