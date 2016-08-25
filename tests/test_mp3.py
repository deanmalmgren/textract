import unittest

import base


class Mp3TestCase(base.ShellParserTestCase, unittest.TestCase):
    extension = 'mp3'
    print extension

	def test_mp3(self):
        """make sure default audio method output is correct"""
        print 'run test_google'
        self.compare_python_output(self.raw_text_filename)

    def test_mp3_google(self):
        """make sure google api python output is correct"""
        print 'run test_google'
        self.compare_python_output(self.raw_text_filename, method='google')

    def test_mp3_sphinx(self):
        """make sure sphinx python output is correct"""
        print 'run test_sphinx'
        self.compare_python_output(self.raw_text_filename, method='sphinx')
