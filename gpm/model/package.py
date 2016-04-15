from gpm.utils.sdb import StaticDB
from gpm.utils.package import PackageOpration
from gpm.const.status import Status

class Packages(StaticDB):
    def __init__(self):
        StaticDB.__init__(self)
        self.__packages = []

    def find(self, key):
        self.__packages = self.gets(key)
        return self.__packages

    def list(self):
        self.__packages = self.all()
        return self.__packages

    def remove(self):
        po = PackageOpration()
        for pkg in self.__packages:
            po.set(pkg)
            ret = po.remove()
            if not ret:
                return ret
            del self[pkg]

        return True

    def install(self, configs):
        po = PackageOpration()
        if not isinstance(configs, list):
            configs = [configs]

        for config in configs:
            po.set(config)
            ret = po.install()
            if not ret:
                return ret
            self[config.name] = config

        return True
