import pptx

from .utils import BaseParser, _call_with_kwargs


class Parser(BaseParser):
    """Extract text from pptx file using python-pptx
    """

    def extract(self, filename, **kwargs):
        presentation = _call_with_kwargs(pptx.Presentation, filename, **kwargs)
        text_runs = []
        for slide in presentation.slides:
            for shape in slide.shapes:
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        text_runs.append(run.text)
        return '\n\n'.join(text_runs)
