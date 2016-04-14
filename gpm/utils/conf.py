import yaml
from gpm.utils.console import gets
from gpm.utils.log import Log
from gpm.utils.operation import LocalOperation
from gpm.settings import GPM_YML
from gpm.settings.status import Status

class GPMConf(object):
    def __init__(self):
        self.path = LocalOperation.rel2abs(GPM_YML)
        self.content = {}
        
    def read(self):
        with open(self.path, "r") as stream:
            self.content = yaml.load(stream)

    def write(self, path, data):
        with open(path, "w+") as stream:
            self.content = yaml.dump(data, stream)
        
    @property
    def author(self):
        return self.content.get("author", "")

    @property
    def description(self):
        return self.content.get("description", "")

    @property
    def version(self):
        return self.content.get("version", "")

    @property
    def email(self):
        return self.content.get("email", "")

    @property
    def language(self):
        return self.content.get("language", "")

    @property
    def build(self):
        return self.content.get("build", "")

    @property
    def install(self):
        return self.content.get("install", "")

    @property
    def test(self):
        return self.content.get("test", "")

    @property
    def dep(self):
        return self.content.get("dep", "")

    @property
    def name(self):
        return self.content.get("name", "")

    @property
    def git(self):
        git = self.content.get("git", "")
        if ".git" in git:
            git = "/".join(git.split("/")[:-1])
        return git

    def create_conf(self):
        if LocalOperation.exist(self.path):
            Log.warn(Status["STAT_GPM_CONF_EXIST"])
            return
        content = {}
        sections = [("language",    False),
                    ("author",      False),
                    ("version",     False),
                    ("email",       False),
                    ("description", False),
                    ("name",        True),
                    ("git",         False,)]

        for section in sections:
            while(1):
                content[section[0]] = gets("Input project's %s" % section[0])
                if not content[section[0]]:
                    Log.warn("%s can't empty." % section[0])

        self.write(self.path, content)

#####################################
#                                   #
#          SYS Configure            #
#                                   #
#####################################

class SYSConf(object):
    def __init__(self):
        pass            #TODO implement