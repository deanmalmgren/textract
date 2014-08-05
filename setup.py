import glob
import os
from setuptools import setup

import textract

# get all of the scripts
scripts = glob.glob("bin/*")

# read in the description from README
with open("README.rst") as stream:
    long_description = stream.read()

github_url='https://github.com/deanmalmgren/textract'

# read in the dependencies from the virtualenv requirements file
dependencies = []
filename = os.path.join("requirements", "python")
with open(filename, 'r') as stream:
    for line in stream:
        package = line.strip().split('#')[0]
        if package:
            dependencies.append(package)

setup(
    name=textract.__name__,
    version=textract.VERSION,
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
    zip_safe=False,
)
