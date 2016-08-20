import os
import unittest
import tempfile
import shutil

from textract.parsers.filetype import detect_filetype


def file_paths():
    """
    Returns a list of paths to test files

    e.g.
    [
        './data/epub/raw_text.epub',
        '.data/epub/standardized_text.epub'
        ...
    ]
    """
    paths = []
    data_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data'
    )
    for root, directories, files in os.walk(data_dir):
        _, folder = os.path.split(root)
        for filename in files:
            _, ext = os.path.splitext(filename)
            ext = ext.strip('.')
            if ext == folder:
                abs_path = os.path.join(root, filename)
                paths.append(abs_path)
    return paths



class DetectFileTypeTestCase(unittest.TestCase):
    """
    Make sure detecting file types works correctly.
    """


    def test_detect_filetype_with_extension(self):
        """
        Make sure we are using the extension when it exists
        """
        files = file_paths()
        for path in files:
            _, ext = os.path.splitext(path)
            ext = ext.strip('.')
            detected = detect_filetype(path)
            self.assertEqual(ext, detected)

    def test_detect_filetype_with_mimetype(self):
        """
        Test detectin filetypes by their mime
        """
        files = file_paths()
        for path in files:
            try:
                # Put in temporary file that has no extension
                _, orig_ext = os.path.splitext(path)
                orig_ext = orig_ext.strip('.')
                handler, temp_path = tempfile.mkstemp()
                shutil.copyfile(path, temp_path)
                detected = detect_filetype(temp_path)
                self.assertEqual(orig_ext, detected)
            finally:
                # clean up temp files, be a good citizen
                os.remove(temp_path)
