import unittest
from uuid import uuid4

from textract.parsers import utils
from textract.parsers import exceptions


class UtilsTestCase(unittest.TestCase):
    def test_shell_parser_run(self):
        parser = utils.ShellParser()
        try:
            # There shouldn't be a command on the path matching a random uuid
            parser.run([str(uuid4())])
        except exceptions.ShellError as e:
            self.assertTrue(e.is_not_installed())
        else:
            self.assertTrue(False, "Expected ShellError")
