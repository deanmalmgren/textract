import unittest
import warnings

from . import base


class XlsxTestCase(base.BaseParserTestCase, unittest.TestCase):
    extension = "xlsx"

    def test_standardized_text_python(self):
        # standardized_text.xlsx carries a Mac Excel 2008 "Page Layout View"
        # (mx:PLV) view-state extension that openpyxl doesn't model and drops
        # on load. It holds no cell data, so the warning is benign here.
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="Unknown extension is not supported and will be removed",
                category=UserWarning,
            )
            super().test_standardized_text_python()
