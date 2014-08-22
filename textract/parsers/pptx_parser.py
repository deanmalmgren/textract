import pptx

from .utils import BaseParser


class Parser(BaseParser):
    """Extract text from pptx file using python-pptx
    """

    def extract(self, filename, **kwargs):
        presentation = pptx.Presentation(filename)
        text_runs = []
        for slide in presentation.slides:
            for shape in slide.shapes:
                if not shape.has_textframe:
                    continue
                for paragraph in shape.textframe.paragraphs:
                    for run in paragraph.runs:
                        text_runs.append(run.text)
        return '\n\n'.join(text_runs)
