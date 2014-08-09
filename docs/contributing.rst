.. _contributing:

Contributing
============

The overarching goal of this project is to make it as easy as possible
to extract raw text from any document for the purposes of most natural
language processing tasks. In practice, this means that this project
should preferentially provide tools that correctly produce output that
has words in the correct order but that whitespace between words,
formatting, etc is totally irrelevant.

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

2. Install `Vagrant <http://vagrantup.com/downloads>`_ and
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

3. On the virtual machine, make sure everything is working by running
   the suite of functional tests:

   .. code-block:: bash

        ./tests/run_functional_tests.sh

   These functional tests are designed to be run on an Ubuntu 12.04
   LTS server, just like the virtual machine and the server that runs
   the travis-ci test suite. There are some other tests that have been
   added along the way in the `Travis configuration
   <https://github.com/deanmalmgren/textract/blob/master/.travis.yml>`_. For your
   convenience, you can run all of these tests with:

   .. code-block:: bash

        ./tests/run.py

   Current build status: |Build Status|

4. Contribute! There are several `open issues
   <https://github.com/deanmalmgren/textract/issues>`_ that provide good
   places to dig in. Check out the `contribution guidelines
   <https://github.com/deanmalmgren/textract/blob/master/CONTRIBUTING.md>`_ and send
   pull requests; your help is greatly appreciated!

.. |Build Status| image:: https://travis-ci.org/deanmalmgren/textract.png
   :target: https://travis-ci.org/deanmalmgren/textract


Style guidelines
----------------

As a general rule of thumb, the goal of this package is to be as
readable as possible to make it easy for novices and experts alike to
contribute to the source code in meaningful ways. Pull requests that
favor cleverness or optimization over readability are less likely to be
incorporated.

To make this notion of "readability" more concrete, here are a few
stylistic guidelines that we recommend:

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
