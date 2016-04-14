PACKAGE      = "gpm"
NAME         = PACKAGE
DESCRIPTION  = "Package manager base Git"
AUTHOR       = "tor4z"
AUTHOR_EMAIL = "vwenjie@hotmail.com"
URL          = "https://github.com/tor4z/Galileo-gpm"
LICENSE      = "MIT License"
VERSION      = __import__(PACKAGE).__version__

from setuptools import setup, find_packages

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    packages=find_packages(exclude=["test", "script", "resource"]),
)