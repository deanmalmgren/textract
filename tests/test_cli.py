from argcomplete import CompletionFinder

from textract.cli import get_parser


def test_filename_completion(tmp_path):
    """Shell completion of the filename argument lists matching files."""
    document = tmp_path / "document.pdf"
    document.touch()
    finder = CompletionFinder(get_parser())
    completion = finder.rl_complete(str(tmp_path / "doc"), 0)
    assert completion.strip() == str(document)
