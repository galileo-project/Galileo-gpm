from gpm.utils.sdb import StaticDB
from gpm.utils.package import PackageOpration

class Packages(StaticDB):
    def __init__(self):
        StaticDB.__init__(self)
        self.__packages = []

    def find(self, keys):
        if not isinstance(keys, list):
            keys = [keys]
        self.__packages = self.gets(keys)
        return self.__packages

    def list(self):
        self.__packages = self.all()
        return self.__packages

    def remove(self):
        po = PackageOpration()
        for pkg in self.__packages:
            name, config = pkg.popitem()
            ret = po.remove(config)
            if not ret:
                return ret
            del self[name]

        return True

    def install(self, configs):
        po = PackageOpration()
        if not isinstance(configs, list):
            configs = [configs]

        for config in configs:
            ret = po.install(config)
            if not ret:
                return ret
            self[config.name] = config

        return True

    def dep(self, configs):
        po = PackageOpration()
        if not isinstance(configs, list):
            configs = [configs]

        for config in configs:
            ret = self.find(config.dep)
            if not ret:
                ret = po.dpe(config)
                if not ret:
                    return ret
                self[config.name] = config


        return True
