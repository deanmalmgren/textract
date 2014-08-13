#-*- encoding: utf-8 -*-

import difflib
import os
import tempfile
import unittest as ut

from textract.parsers import pdf_parser

class PdfTests(ut.TestCase):

    def testPdfWithRawText(self):
        self._testCompressedSample('pdf/raw_text.zip')

    def testPdfWithUnicodeText(self):
        self._testCompressedSample('pdf/unicode.zip', threshold=0.02)

    def _testCompressedSample(self, sampleFileName, threshold=.0):
        def extractZip(path):
            import zipfile
            inputZip = zipfile.ZipFile(path)
            return {n: inputZip.read(n) for n in inputZip.namelist()}

        files = extractZip(sampleFileName)
        if 'sample.pdf' not in files or 'expected.txt' not in files:
            raise RuntimeError(
                'Couldn\'t find either sample.pdf or expected.txt in tested ZIP file: {}'.format(sampleFileName))

        tempFileHandle, tempFilePath = tempfile.mkstemp('…textract…')
        with os.fdopen(tempFileHandle, 'wb') as fp:
            fp.write(files['sample.pdf'])

        self._compare(pdf_parser.extract(tempFilePath), files['expected.txt'], threshold)

    def _compare(self, extractedText, expectedText, threshold):
        def clear(text):
            return text.replace('\r', '').replace('\n', '').replace('\t', '').strip()
        a = clear(extractedText).replace(' ', '')
        b = clear(expectedText).replace(' ', '')
        self.assertLessEqual(1.0 - threshold, difflib.SequenceMatcher(None, a, b).ratio())

