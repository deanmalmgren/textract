import glob
import os
import sys
from setuptools import setup

import textract

# get all of the scripts
scripts = glob.glob("bin/*")

# read in the description from README
with open("README.rst") as stream:
    long_description = stream.read()

github_url = 'https://github.com/deanmalmgren/textract'

# read in the dependencies from the virtualenv requirements file
dependencies, dependency_links = [], []
filename = os.path.join("requirements", "python")
with open(filename, 'r') as stream:
    for line in stream:
        line = line.strip()
        if line.startswith("http"):
            dependency_links.append(line)
        else:
            package = line.split('#')[0]
            if package:
                dependencies.append(package)


setup(
    name=textract.__name__,
    version="1.6.0",
    description="extract text from any document. no muss. no fuss.",
    long_description=long_description,
    url=github_url,
    download_url="%s/archives/master" % github_url,
    author='Dean Malmgren',
    author_email='dean.malmgren@datascopeanalytics.com',
    license='MIT',
    scripts=scripts,
    packages=[
        'textract',
        'textract.parsers',
    ],
    install_requires=dependencies,
    dependency_links=dependency_links,
    zip_safe=False,
)
