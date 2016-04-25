import os.path
import re

def GitURL2Name(url):
    if not url:
        return None
    elif not "/" in url and not "." in url:
        return url
    else:
        suffix = url.split("/")[-1]
        if not "." in  suffix:
            return suffix
        else:
            return suffix.split(".")[0]


_RE_DEP_URL = re.compile(r"([_\w\d\-@\.]+:[/_\w\d\-\.]+\/[\w\d_\-]+\.git):?([\w\d_\.]*)")
def DepURL2Git(dep):
    ret = _RE_DEP_URL.findall(dep)
    if ret:
        return ret[0]
    else:
        return None

def Path2Dir(path):
    path = os.path.abspath(path)
    return path.split("/")[-1]

#############################
#                           #
#       String verify       #
#                           #
#############################

_RE_NAME = re.compile(r"[_\w\d]+")
def VerifyName(name):
    return not _RE_NAME.match(name) is None

_RE_EMAIL = re.compile(r"[_\w\d]+@[_\w\d]+\.[\w]+")
def VerifyEmail(email):
    return not _RE_EMAIL.match(email) is None

_RE_GIT = re.compile(r"git@[\w\d_\-]+\.[\w]+:[\w\d_\-]+")
def VerifyGit(name):
    return not _RE_GIT.match(name) is None
