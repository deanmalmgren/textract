import pptx


def extract(filename, **kwargs):
    """Extract text from pptx file using python-pptx
    """
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
