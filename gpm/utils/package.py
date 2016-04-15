from gpm.utils.operation import LocalOperation
from gpm.const.status import Status

class PackageOpration(object):
    def __init__(self, config = None):
        self.__confg = config

    def set(self, config):
        self.__confg = config

    def install(self):
        ret = False
        if not self.__confg:
            raise Exception(Status["STAT_NOT_CONF"])
        cmds = self.__confg.install
        for cmd in cmds:
            ret = LocalOperation.run(cmd)

        return ret

    def remove(self):
        ret = False
        if not self.__confg:
            raise Exception(Status["STAT_NOT_CONF"])
        cmds = self.__confg.remove
        for cmd in cmds:
            ret = LocalOperation.run(cmd)

        return ret

    def update(self):
        pass

    def test(self):
        pass