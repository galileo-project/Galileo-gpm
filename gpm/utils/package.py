from gpm.utils.operation import LocalOperation
from gpm.utils.git_client import GitClient
from gpm.utils.conf import GPMConf
from gpm.utils import GitURL2Name, DepURL2Git
from gpm.const import GPM_YML, GPM_SRC
from gpm.utils import Path2Dir
from gpm.utils.console import puts
from gpm.utils.log import Log
from gpm.const.status import Status
import os

class PackageOpration(object):
    def __init__(self, config = None, path = None):
        self.__config = config
        self.__path   = path or LocalOperation.pwd()

    def set(self, config = None, path = None):
        if config:
            self.__config = config
            if not path:
                self.__path = os.path.join(GPM_SRC, self.__config.name)
        if path:
            self.__path = path

    def __save_src(self, save = True):
        if save:
            return LocalOperation.cp(self.__path, GPM_SRC)
        else:
            return True

    def __remove_src(self):
        return LocalOperation.rm(os.path.join(GPM_SRC, self.__config.name))

    def install(self, config = None, save = True):
        self.set(config)
        Log.info(Status["STAT_INSTALLING_PKG"] % self.__config.name)
        ret = False
        if not self.__config:
            return False

        cmds = self.__config.install
        for cmd in cmds:
            Log.info(Status["STAT_RUN_CMD"] % cmd)
            ret = LocalOperation.run(cmd, path = self.__path)
            if not ret:
                break

        if ret and not self.__save_src(save):
            ret = False

        return ret

    def remove(self, config = None):
        self.set(config)
        ret = False
        if not self.__config:
            return False

        if self.find(self.__config.name, show = False):         #pkg exist
            Log.info(Status["STAT_PACKAGE_EXIST"] % self.__config.name)
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
            dep_name  = GitURL2Name(dep)
            Log.info(Status["STAT_INSTALL_DEP"] % dep_name)
            if self.find(dep_name, show = False):         #dep exist
                Log.info(Status["STAT_PACKAGE_EXIST"] % dep_name)
                continue

            dep_url, dep_tag = DepURL2Git(dep)
            ret = gc.clone(dep_url, GPM_SRC, dep_tag)
            if not ret:
                return ret
            #install dep
            dep_path  = os.path.join(GPM_SRC, dep_name)
            conf_path = os.path.join(dep_path, GPM_YML)
            conf = GPMConf(conf_path)

            pkg = PackageOpration()
            pkg.set(conf, dep_path)
            ret = pkg.install(save=False)
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

    def publish(self):
        gc = GitClient(self.__config)
        gc.publish()

    @classmethod
    def list(cls):
        ret = LocalOperation.ls(GPM_SRC)
        cls.__show_pkgs(ret)

    @classmethod
    def find(cls, name, show = True):
        ret = LocalOperation.find(GPM_SRC, name)
        if show:
            cls.__show_pkgs(ret)

        if ret:
            conf_path = os.path.join(ret[0], GPM_YML)
            return GPMConf(conf_path)
        return None

    @classmethod
    def __show_pkgs(cls, pkgs):
        if not isinstance(pkgs, list):
            pkgs = [pkgs]

        puts("\n".join([Path2Dir(pkg) for pkg in pkgs]))