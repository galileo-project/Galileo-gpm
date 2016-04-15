from gpm.utils.operation import LocalOperation
from gpm.utils.git import GitClient
from gpm.utils.conf import GPMConf
from gpm.utils import GitURL2Dir
from gpm.const import GPM_YML
from gpm.const.status import Status
import os

class PackageOpration(object):
    def __init__(self, config = None):
        self.__config = config

    def set(self, config):
        if not config:
            self.__config = config

    def install(self, config = None):
        self.set(config)
        ret = False
        if not self.__config:
            return False
        cmds = self.__config.install
        for cmd in cmds:
            ret = LocalOperation.run(cmd)

        return ret

    def remove(self, config = None):
        self.set(config)
        ret = False
        if not self.__config:
            return False
        cmds = self.__config.remove
        for cmd in cmds:
            ret = LocalOperation.run(cmd)

        return ret

    def dpe(self, config):
        self.set(config)
        ret = False
        if not self.__config:
            return False

        gc = GitClient(self.__config)
        deps = self.__config.dep
        for dep in deps:
            ret = gc.clone(dep)
            if not ret:
                return ret
            #install dep
            conf = GPMConf(os.path.join(GitURL2Dir(dep), GPM_YML))
            ret = self.install(conf)
            if not ret:
                return False
        return ret

    def update(self):
        pass

    def test(self):
        pass