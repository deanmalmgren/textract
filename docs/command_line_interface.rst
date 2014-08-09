.. _command-line-interface:

Command line interface
======================

This package ships with the ``textract`` command, which embodies the
entire command line interface for this package. This command can be
run on any supported file by simply running

.. code-block:: bash

    textract path/to/some/file.extension

on any :ref:`supported file type <supporting>`. Full documentation for
the command line interface is available with the ``-h/--help`` command
line option:


.. code-block:: bash

    [terminal]$ textract -h

.. program-output:: ../bin/textract -h


To make the command line interface as usable as possible,
autocompletion of available options with textract is enabled by
@kislyuk's amazing `argcomplete
<https://github.com/kislyuk/argcomplete>`_ package.  Follow
instructions to `enable global autocomplete
<https://github.com/kislyuk/argcomplete#activating-global-completion>`_
and you should be all set. As an example, this is also configured in
the `virtual machine provisioning for this project
<http://github.com/deanmalmgren/textract/blob/master/provision/development.sh#L17>`_. 
