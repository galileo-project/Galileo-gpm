from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.package import PackageOpration

class CLITest(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_test"}
    __doc__ = """

    """

    def _test(self, *args, **kwargs):
        po = PackageOpration()
        po.test()

    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLITest