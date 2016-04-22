from gpm.utils.operation import LocalOperation
from gpm.utils.git_client import GitClient
from gpm.utils.conf import GPMConf
from gpm.utils import GitURL2Dir
from gpm.const import GPM_YML, GPM_SRC
from gpm.utils import Path2Dir
from gpm.utils.console import puts
import os

class PackageOpration(object):
    def __init__(self, config = None, path = None):
        self.__config = config
        self.__path   = path or LocalOperation.pwd()

    def set(self, config = None, path = None):
        if config:
            self.__config = config
        if path:
            self.__path = path

    def __save_src(self):
        return LocalOperation.cp(self.__path, GPM_SRC)

    def __remove_src(self):
        return LocalOperation.rm(os.path.join(GPM_SRC, self.__config.name))

    def install(self, config = None):
        self.set(config)
        ret = False
        if not self.__config:
            return False

        cmds = self.__config.install
        for cmd in cmds:
            ret = LocalOperation.run(cmd, path = self.__path)
            if not ret:
                break

        if ret and not self.__save_src():
            ret = False

        return ret

    def remove(self, config = None):
        self.set(config)
        ret = False
        if not self.__config:
            return False

        cmds = self.__config.remove
        for cmd in cmds:
            ret = LocalOperation.run(cmd, path = self.__path)
            if not ret:
                break

        if ret and not self.__remove_src():
            ret = False

        return ret

    def dep(self, config = None):
        self.set(config)
        ret = False
        if not self.__config:
            return False

        gc = GitClient(self.__config)
        deps = self.__config.dep
        for dep in deps:
            ret = gc.clone(dep, GPM_SRC)
            if not ret:
                return ret
            #install dep
            dep_path  = os.path.join(GPM_SRC, GitURL2Dir(dep))
            conf_path = os.path.join(dep_path, GPM_YML)
            conf = GPMConf(conf_path)
            self.set(conf, dep_path)
            ret = self.install()
            if not ret:
                return False
        return ret

    def test(self, config = None):
        self.set(config)
        ret = False
        if not self.__config:
            return False

        cmds = self.__config.test
        for cmd in cmds:
            ret = LocalOperation.run(cmd, path = self.__path)
            if not ret:
                break

        return ret

    @classmethod
    def list(cls):
        ret = LocalOperation.ls(GPM_SRC)
        cls.__show_pkgs(ret)

    @classmethod
    def find(cls, name):
        ret = LocalOperation.find(GPM_SRC, name)
        cls.__show_pkgs(ret)

        if ret:
            conf_path = os.path.join(ret[0], GPM_YML)
            return GPMConf(conf_path)
        return None

    @classmethod
    def __show_pkgs(cls, pkgs):
        if isinstance(pkgs, list):
            pkgs = [pkgs]
        puts("\n".join([Path2Dir(pkg) for pkg in pkgs]))