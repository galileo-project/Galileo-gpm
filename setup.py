PACKAGE      = "gpm"
NAME         = PACKAGE
DESCRIPTION  = "Package manager base Git"
AUTHOR       = "tor4z"
AUTHOR_EMAIL = "vwenjie@hotmail.com"
URL          = "https://github.com/tor4z/Galileo-gpm"
LICENSE      = "MIT License"
VERSION      = __import__(PACKAGE).__version__

import os
import codecs
from setuptools import setup, find_packages

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    packages=find_packages(exclude=["test", "script", "resource"]),
    zip_safe=False,
)