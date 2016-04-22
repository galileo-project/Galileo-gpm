import yaml
import os
from gpm.utils.console import gets
from gpm.utils.log import Log
from gpm.utils.operation import LocalOperation
from gpm.const import GPM_YML, SYS_CONF
from gpm.const.status import Status
from gpm.utils import VerifyName, VerifyEmail, VerifyGit

class _Conf(object):
    def __init__(self, path):
        self._path = path
        self._content = {}
        self.read()

    def read(self):
        if LocalOperation.exist(self._path):
            with open(self._path, "r") as stream:
                self._content = yaml.load(stream)

    def write(self, path, data):
        LocalOperation.mkdir(os.path.dirname(path))
        with open(path, "w+") as stream:
            yaml.dump(data, stream, allow_unicode=True, default_flow_style=False)

#####################################
#                                   #
#          GPM Configure            #
#                                   #
#####################################

class GPMConf(_Conf):
    def __init__(self, path = None):
        if path and not GPM_YML in path:
            path = os.path.join(path, GPM_YML)
        path = LocalOperation.rel2abs(path or GPM_YML)
        _Conf.__init__(self, path)

    @property
    def path(self):
        return self._path

    @property
    def author(self):
        return self._content.get("author", "")

    @property
    def description(self):
        return self._content.get("description", "")

    @property
    def version(self):
        return self._content.get("version", "")

    @property
    def email(self):
        return self._content.get("email", "")

    @property
    def language(self):
        return self._content.get("language", "")

    @property
    def build(self):
        return self._content.get("build", [])

    @property
    def install(self):
        return self._content.get("install", [])

    @property
    def remove(self):
        return self._content.get("remove", [])

    @property
    def test(self):
        return self._content.get("test", [])

    @property
    def dep(self):
        return self._content.get("dep", [])

    @property
    def name(self):
        return self._content.get("name", "")

    @property
    def git_url(self):
        git = self._content.get("git_url", "")
        if ".git" in git:
            git = "/".join(git.split("/")[:-1])
        return git

    def generate(self):
        sysConf = SYSConf()
        if self.path and LocalOperation.exist(self.path):
            Log.fatal(Status["STAT_GPM_CONF_EXIST"])

                      #key            prompt                         default                          verify
        sections = [("name",        "project name",                 self.name or None,               VerifyName),
                    ("language",    "project language",             self.language or None,           VerifyName),
                    ("author",      "author name",                  self.author or sysConf.author,   None),
                    ("version",     "initial version",              self.version or None,            None),
                    ("email",       "author email",                 self.email or sysConf.email,     VerifyEmail),
                    ("description", "project description",          self.description or None,        None),
                    ("git_url",     "git url[git@github.com:name]", self.git_url or sysConf.git_url, None)]

        for section in sections:
            while(1):
                self._content[section[0]] = gets("Input %s" % section[1], section[2])
                if section[3] and not self._content[section[0]]:
                    Log.warn(Status["STAT_INPUT_EMPTY"] % section[0])
                    continue
                elif section[3] and not VerifyName(self._content[section[0]]):
                    Log.warn(Status["STAT_INPUT_INVALID"] % section[0])
                    continue
                else:
                    break

        pkg_path    = os.path.join(LocalOperation.pwd(), self.name)
        self._path = os.path.join(pkg_path, GPM_YML)
        self.write(self._path, self._content)

#####################################
#                                   #
#          SYS Configure            #
#                                   #
#####################################

class SYSConf(_Conf):
    def __init__(self, path = None):
        path = LocalOperation.rel2abs(path or SYS_CONF)
        _Conf.__init__(self, path)

    @property
    def author(self):
        return self._content.get("author", "")

    @property
    def email(self):
        return self._content.get("email", "")

    @property
    def git_url(self):
        return self._content.get("git_url", "")

    def generate(self):
                      #key         prompt                                    default                        verify
        sections = [("author",  "user name",                    self.author or LocalOperation.get_user(), VerifyName),
                    ("email",   "user email",                   self.email,                               VerifyEmail),
                    ("git_url", "git url[git@github.com:name]", self.git_url,                             VerifyGit)]

        for section in sections:
            while(1):
                self._content[section[0]] = gets("Input %s" % section[1], section[2])
                if section[3] and not self._content[section[0]]:
                    Log.warn(Status["STAT_INPUT_EMPTY"] % section[0])
                    continue
                elif section[3] and not section[3](self._content[section[0]]):
                    Log.warn(Status["STAT_INPUT_INVALID"] % section[0])
                    continue
                else:
                    break

        self.write(self._path, self._content)