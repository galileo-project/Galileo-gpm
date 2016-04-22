import yaml
import os
from gpm.utils.console import gets
from gpm.utils.log import Log
from gpm.utils.operation import LocalOperation
from gpm.const import GPM_YML, SYS_CONF
from gpm.const.status import Status

class _Conf(object):
    def __init__(self, path):
        self.__path = path
        self.__content = {}

    def read(self):
        with open(self.__path, "r") as stream:
            self.__content = yaml.load(stream)

    def write(self, path, data):
        LocalOperation.mkdir(os.path.dirname(path))
        with open(path, "w+") as stream:
            yaml.dump(data, stream)

#####################################
#                                   #
#          GPM Configure            #
#                                   #
#####################################

class GPMConf(_Conf):
    def __init__(self, path = None):
        path = LocalOperation.rel2abs(path or GPM_YML)
        _Conf.__init__(self, path)

    @property
    def path(self):
        return self.__path

    @property
    def author(self):
        return self.__content.get("author", "")

    @property
    def description(self):
        return self.__content.get("description", "")

    @property
    def version(self):
        return self.__content.get("version", "")

    @property
    def email(self):
        return self.__content.get("email", "")

    @property
    def language(self):
        return self.__content.get("language", "")

    @property
    def build(self):
        return self.__content.get("build", [])

    @property
    def install(self):
        return self.__content.get("install", [])

    @property
    def remove(self):
        return self.__content.get("remove", [])

    @property
    def test(self):
        return self.__content.get("test", [])

    @property
    def dep(self):
        return self.__content.get("dep", [])

    @property
    def name(self):
        return self.__content.get("name", "")

    @property
    def git_url(self):
        git = self.__content.get("git_url", "")
        if ".git" in git:
            git = "/".join(git.split("/")[:-1])
        return git

    def create_conf(self):
        sysConf = SYSConf()
        if LocalOperation.exist(self.__path):
            self.read()

                      #key          empty   prompt                                    default
        sections = [("language",    False, "project language",                        self.language or None),
                    ("author",      False, "author name",                             self.author or sysConf.author),
                    ("version",     False, "initial version",                         self.version or None),
                    ("email",       False, "author email",                            self.email or sysConf.email),
                    ("description", False, "project description",                     self.description or None),
                    ("name",        True,  "project name",                            self.name or None),
                    ("git_url",     False, "author git url[git@github.com:yourname]", self.git_url or sysConf.git_url)]

        for section in sections:
            while(1):
                self.__content[section[0]] = gets("Input %s" % section[2], section[3])
                if not self.__content[section[0]] and section[1]:
                    Log.warn(Status["STAT_INPUT_EMPTY"] % section[0])
                else:
                    break

        self.write(self.__path, self.__content)

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
        return self.__content.get("author", "")

    @property
    def email(self):
        return self.__content.get("email", "")

    @property
    def git_url(self):
        return self.__content.get("git_url", "")

    def generate(self):
        if LocalOperation.exist(self.__path):
            self.read()

                      #key          empty   prompt                                    default
        sections = [("author",  False, "user name",                             self.author or LocalOperation.user),
                    ("email",   False, "user email",                            self.email),
                    ("git_url", False, "user git url[git@github.com:yourname]", self.git_url)]

        for section in sections:
            while(1):
                self.__content[section[0]] = gets("Input %s" % section[2], section[3])
                if not self.__content[section[0]] and section[1]:
                    Log.warn(Status["STAT_INPUT_EMPTY"] % section[0])
                else:
                    break

        self.write(self.__path, self.__content)