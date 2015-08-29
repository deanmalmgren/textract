.. _command-line-interface:

Command line interface
======================

textract
--------

.. argparse::
   :module: textract.cli
   :func: get_parser
   :prog: textract

.. note:: 

    To make the command line interface as usable as possible,
    autocompletion of available options with textract is enabled by
    @kislyuk's amazing `argcomplete
    <https://github.com/kislyuk/argcomplete>`_ package.  Follow
    instructions to `enable global autocomplete
    <https://github.com/kislyuk/argcomplete#activating-global-completion>`_
    and you should be all set. As an example, this is also configured
    in the `virtual machine provisioning for this project
    <http://github.com/deanmalmgren/textract/blob/master/provision/development.sh#L17>`_.
