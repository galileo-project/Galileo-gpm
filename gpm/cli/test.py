from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.package import PackageOpration
from gpm.utils.log import Log
from gpm.const.status import Status

class CLITest(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_test"}
    __doc__ = """

    """

    def _test(self, *args, **kwargs):
        po = PackageOpration()
        ret = po.test(self.config)
        if not ret:
            Log.fatal(Status["STAT_TEST_ERROR"] % self.config.name)
        else:
            Log.success(Status["STAT_TEST_SUCCESS"] % self.config.name)


    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLITest