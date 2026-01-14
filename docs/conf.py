from importlib.metadata import version as get_version

project = "textract"
author = "Dean Malmgren, Kyle King"
copyright = "2014, Dean Malmgren; 2024, Kyle King"

release = version = get_version("textract-py3")

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinxarg.ext",
]

templates_path = [".templates"]
source_suffix = ".rst"
master_doc = "index"
exclude_patterns = ["build"]

pygments_style = "sphinx"
html_theme = "sphinx_rtd_theme"
html_static_path = []
htmlhelp_basename = "textractdoc"

latex_elements = {}
latex_documents = [
    ("index", "textract.tex", "textract Documentation", author, "manual"),
]

man_pages = [
    ("index", "textract", "textract Documentation", [author], 1)
]

texinfo_documents = [
    (
        "index",
        "textract",
        "textract Documentation",
        author,
        "textract",
        "Extract text from any document.",
        "Miscellaneous",
    ),
]
