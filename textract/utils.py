import imp
import sys


def non_local_import(name, custom_name=None):
    """This function can be used to import modules that are on sys.path
    but have the same name as a module in the local namespace. This
    happens, for example, with docx and pptx files as those parsers
    have the same name.

    http://stackoverflow.com/a/6032023/564709
    """

    custom_name = custom_name or name

    f, pathname, desc = imp.find_module(name, sys.path[1:])
    module = imp.load_module(custom_name, f, pathname, desc)

    return module
