from ..utils import non_local_import


def extract(filename):
    """Extract text from pptx file with inspiration from
    https://python-pptx.readthedocs.org/en/latest/user/quickstart.html#extract-all-text-from-slides-in-presentation
    """
    pptx = non_local_import('pptx')
    presentation = pptx.Presentation(filename)
    text_runs = []
    for slide in presentation.slides:
        for shape in slide.shapes:
            if not shape.has_textframe:
                continue
            for paragraph in shape.textframe.paragraphs:
                for run in paragraph.runs:
                    text_runs.append(run.text.encode('utf-8'))
    return '\n\n'.join(text_runs)
